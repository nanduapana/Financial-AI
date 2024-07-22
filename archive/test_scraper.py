import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from datetime import datetime, timedelta
from transformers import pipeline

sentiment_analyzer = pipeline('sentiment-analysis',max_length=1024)
BASE_URL = 'https://www.moneycontrol.com'
DAYS = 2
OUTPUT_DIR = 'data/raw'

def extract_header_and_url(anchors, category="general"):
    header_urls = []
    for anchor in anchors:
        header_urls.append({"title":anchor["title"],
                            "url":anchor["href"],
                            "type":category})
    return header_urls


def category_news(categorical_type_news):
    categorical_news = []
    for news in categorical_type_news:
        news_category = list(news.keys())[0]
        if news_category!="Startups":
            news_url = news[news_category]
            response = requests.get(news_url)
            soup=BeautifulSoup(response.content, 'html.parser')
            category_list = soup.find(id="cagetory")

            lis = category_list.find_all("li", {"class":"clearfix"})
            anchors = [li.find("a") for li in lis]
            categorical_news = categorical_news + extract_header_and_url(anchors, news_category)
    return categorical_news

def general_news(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    bizs = soup.find_all("div", {"class":"bx"})
    left_content = soup.find("section", {"class":"main-left"})

    main_headers = left_content.find("div", {"class":"mob-hide"})
    more_news = left_content.find("div", {"class":"clearfix MT20 mob-hide"})


    main_headers = main_headers.find("div", {"class":"clearfix"})
    left_panel = main_headers.find("div", {"class":"sub-col-left"})
    right_panel = main_headers.find("div", {"class": "sub-col-rht"})

    left_panel_news = left_panel.find("div", {"class":"clearfix ltsnewsbx"})
    left_panel_news_headers = left_panel_news.find_all("a")
    right_panel_news = right_panel.find("div", {"class":"clearfix listed_newsec"})
    right_panel_news_headers = right_panel_news.find_all("a")

    left_news_data = extract_header_and_url(left_panel_news_headers)
    right_news_data = extract_header_and_url(right_panel_news_headers)


    more_news_left_section = more_news.find(id="keynwstb1")

    more_news_data = more_news_left_section.find_all("a")
    more_news_data = extract_header_and_url(more_news_data)
    main_news_data = left_news_data + right_news_data + more_news_data

    categories=[]
    for biz in bizs:
        category = biz.find("h2").find("a")
        category_name = category.get_text()
        category_url = category["href"]
        categories.append({category_name:category_url})
    return categories, main_news_data

# def fetch_news_urls(base_url, days):
#     news_urls = []
#     for i in range(days):
#         date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
#         url = f"{base_url}/news/{date}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             for a_tag in soup.find_all('a', href=True):
#                 if '/news/' in a_tag['href']:
#                     news_urls.append(a_tag['href'])
#     return news_urls

def fetch_content(content_url):
    response = requests.get(content_url)
    if response:
        soup = BeautifulSoup(response.content, "html.parser")
        content_data = soup.find(id="contentdata")
        if content_data:
            # Money Control stock price from article
            # if content_data.find("div", {"class": "stockwidget"}):
            #     stockwidget = content_data.find("ul")
            #     stock_name = stockwidget.find_all("li")[0].find("a").get_text()
            #     print(stock_name)

            paras = content_data.find_all("p")
            return paras
        return None
    return None

# def fetch_article(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         title_tag = soup.find('h1')
#         if title_tag:
#             title = title_tag.get_text()
#             if not title_tag.find("a"):
#                 return None, None
#             header_url = title_tag.find("a")["href"]
#             if title_tag and header_url and title_tag.find("a"):
#                 content = fetch_content(header_url)
#                 content = ' '.join(p.get_text() for p in content)
#                 return title, content
#
#             else:
#                 print(f"No <h1> tag found in {url}")
#     return None, None

def analyze_sentiment(text):
    print(text)
    result = sentiment_analyzer(text)
    print(result)
    return result[0]['label']

def create_csv_file(content, name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    date = datetime.now().strftime('%Y-%m-%d')
    df = pd.DataFrame(content)
    df.to_csv(os.path.join(OUTPUT_DIR, f'{name}_{date}.csv'), index=False)

# def scrape_news(base_url, days, output_dir):
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     for i in range(days):
#         date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
#         news_urls = fetch_news_urls(base_url, 1)  # Fetch URLs for one day at a time
#         articles = []
#         for url in news_urls:
#             title, content = fetch_article(url)
#             # if title and content:
#             #     sentiment = analyze_sentiment(content[0:200])
#             #     articles.append({'title': title, 'content': content, 'url': url, 'sentiment': sentiment})
#
#
#         # df = pd.DataFrame(articles)
#         # df.to_csv(os.path.join(output_dir, f'news_articles_{date}.csv'), index=False)



# scrape_news(BASE_URL, DAYS, OUTPUT_DIR)
# categories, anchors = general_news(BASE_URL)
# categorial_news = category_news(categories)

# final_news_urls = anchors + categorial_news
# create_csv_file(final_news_urls, "content_urls")
# content_data=[]

# print(len(final_news_urls))
# counter=1
# for article_url in final_news_urls:
#     print(counter)
#     if article_url["url"].startswith("https://www.moneycontrol.com"):
#         content = fetch_content(article_url["url"])
#         if content:
#             content = ' '.join(p.get_text() for p in content)
#             article_url["content"]=content
#             content_data.append(article_url)
#     counter+=1

# create_csv_file(content_data, "content_data")


content = fetch_content("https://www.moneycontrol.com/news/world/joe-biden-pulls-out-of-us-presidential-race-12774097.html")

if content:
    content = ' '.join(p.get_text() for p in content)
    analyze_sentiment(content)