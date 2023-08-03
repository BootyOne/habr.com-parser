import aiohttp
from bs4 import BeautifulSoup


async def parse_article_page(article_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(article_url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    error_div = soup.find('div', class_='tm-error-message')

    if error_div:
        return {
            'title': '',
            'date': '',
            'url': article_url,
            'author': '',
            'author_url': ''
        }

    title = soup.select_one('.tm-title_h1').text
    date = soup.find('time').get('title')
    author = soup.select_one('.tm-user-info__username').text.strip()
    author_url = f"https://habr.com{soup.select_one('.tm-user-info__username').get('href')}"

    return {
        'title': title,
        'date': date,
        'url': article_url,
        'author': author,
        'author_url': author_url
    }
