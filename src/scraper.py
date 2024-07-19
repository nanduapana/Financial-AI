import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from datetime import datetime, timedelta

def fetch_news_urls(base_url, days):
    news_urls = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        url = f"{base_url}/news/{date}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                if '/news/' in a_tag['href']:
                    news_urls.append(a_tag['href'])
    return news_urls

def fetch_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').get_text()
        content = ' '.join(p.get_text() for p in soup.find_all('p'))
        return title, content
    return None, None

def scrape_news(base_url, days, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    news_urls = fetch_news_urls(base_url, days)
    articles = []

    for url in news_urls:
        title, content = fetch_article(url)
        if title and content:
            articles.append({'title': title, 'content': content, 'url': url})

    df = pd.DataFrame(articles)
    df.to_csv(os.path.join(output_dir, 'news_articles.csv'), index=False)

if __name__ == "__main__":
    BASE_URL = 'https://www.moneycontrol.com'
    DAYS = 30
    OUTPUT_DIR = 'data/raw'
    scrape_news(BASE_URL, DAYS, OUTPUT_DIR)
