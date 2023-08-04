import aiohttp
from bs4 import BeautifulSoup


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_hub(hub_url: str):
    html = await fetch(hub_url)

    soup = BeautifulSoup(html, 'html.parser')

    error_div = soup.find('div', class_='tm-error-message')

    if error_div:
        return None

    hub_links = soup.find_all('a', class_='tm-hub__title')

    return [{'name': link.find('span').text.strip(), 'url': f"https://habr.com{link['href']}"} for link in hub_links]


async def parse_hub_page(hub_url: str, hub_id: int, semaphore):
    async with semaphore:
        html = await fetch(hub_url)

    soup = BeautifulSoup(html, 'html.parser')

    article_links = soup.find_all('a', {'data-test-id': 'article-snippet-title-link'})

    return [(f"https://habr.com{link['href']}", hub_id) for link in article_links]
