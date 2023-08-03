import asyncio
from parser.hub_parser import parse_hub_page
from parser.article_parser import parse_article_page


MAX_CONCURRENT_REQUESTS = 5


async def main():
    hubs = ['https://habr.com/ru/hub/python/', 'https://habr.com/ru/hub/machine_learning/']

    while True:
        article_urls = []
        for hub_url in hubs:
            article_urls.extend(await parse_hub_page(hub_url))

        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

        tasks = [process_article(semaphore, article_url) for article_url in article_urls]
        await asyncio.gather(*tasks)

        print("Обход всех хабов завершен. Ожидание следующего обхода...")
        await asyncio.sleep(600)


async def process_article(semaphore, article_url):
    async with semaphore:
        article_data = await parse_article_page(article_url)
        print(f"Сохранено: {article_data}")


if __name__ == '__main__':
    asyncio.run(main())
