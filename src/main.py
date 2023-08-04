import itertools
import asyncio
from database.models import Article, Hub
from parser.hub_parser import parse_hub, parse_hub_page
from parser.article_parser import parse_article_page
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


MAX_CONCURRENT_REQUESTS = 3
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DB_URL)


async def main():
    while True:
        all_hub_data = []
        idx = 1
        hubs_on_page = True
        while hubs_on_page:
            hub_data = await parse_hub(f'https://habr.com/ru/hubs/page{idx}/')
            idx += 1
            if hub_data is None:
                hubs_on_page = False
            else:
                all_hub_data.extend(hub_data)

        with Session(engine) as session:
            hub_ids = {}
            for hub_info in all_hub_data:
                existing_hub = session.query(Hub).filter_by(url=hub_info['url']).first()
                if existing_hub:
                    hub_ids[hub_info['url']] = existing_hub.id
                else:
                    hub = Hub(**hub_info)
                    session.add(hub)
                    session.commit()
                    session.refresh(hub)
                    hub_ids[hub_info['url']] = hub.id

        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

        tasks = [parse_hub_page(hub_info['url'], hub_ids[hub_info['url']], semaphore) for hub_info in all_hub_data]
        article_urls = await asyncio.gather(*tasks)
        all_article_urls = list(itertools.chain.from_iterable(article_urls))

        tasks = [process_article(semaphore, article_url[0], article_url[1]) for article_url in all_article_urls]
        await asyncio.gather(*tasks)

        print("Обход всех хабов завершен. Ожидание следующего обхода...")
        await asyncio.sleep(600)


async def process_article(semaphore, article_url, hub_id):
    async with semaphore:
        article_data = await parse_article_page(article_url)

        if article_data is not None:
            article_data['hub_id'] = hub_id
            with Session(engine) as session:
                if not session.query(Article).filter(Article.link == article_data['link']).first():
                    new_article = Article(**article_data)
                    session.add(new_article)
                    session.commit()
                    print(f"Сохранено: {article_data['title']}")
                else:
                    print("Статья уже существует в базе данных. Ничего не сохранено.")
        else:
            print(f'Произошла ошибка, страница не найдена :(')


if __name__ == '__main__':
    asyncio.run(main())
