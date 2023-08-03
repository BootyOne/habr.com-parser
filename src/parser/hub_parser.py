import aiohttp
from bs4 import BeautifulSoup


async def parse_hub_page(hub_url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(hub_url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    article_links = soup.find_all('a', {'data-test-id': 'article-snippet-title-link'})

    return [f"https://habr.com{link['href']}" for link in article_links]
