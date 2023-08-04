from typing import Optional
from datetime import datetime
from parser.fetch import fetch

from bs4 import BeautifulSoup


async def parse_article_page(article_url: str) -> Optional[dict]:
    html = await fetch(article_url)

    soup = BeautifulSoup(html, 'html.parser')

    error_div = soup.find('div', class_='tm-error-message')

    if error_div:
        return None

    title = soup.select_one('.tm-title_h1').text
    text = soup.find('div', class_='tm-article-body').get_text()
    date = datetime.fromisoformat(soup.find('time').get('datetime').replace('Z', '+00:00'))
    if article_url.split('/')[4] == 'specials':
        author = ''
        author_url = ''
    else:
        author = soup.select_one('.tm-user-info__username').text.strip()
        author_url = f"https://habr.com{soup.select_one('.tm-user-info__username').get('href')}"

    return {
        'title': title,
        'text': text,
        'publication_date': date,
        'link': article_url,
        'author_name': author,
        'author_link': author_url
    }
