import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from datetime import datetime, timedelta
from transformers import pipeline

sentiment_analyzer = pipeline('sentiment-analysis', max_length=512, truncation=True)
BASE_URL = 'https://www.moneycontrol.com'
DAYS = 7
OUTPUT_DIR = 'data/raw'

def extract_header_and_url(anchors, category="general"):
    header_urls = []
    for anchor in anchors:
        if type(anchor)==dict:
            header_urls.append({"title": anchor["anchor"]["title"],
                                "url": anchor["anchor"]["href"],
                                "type": category,
                                "date": anchor["date"]})
        else:
            header_urls.append({"title":anchor["title"],
                                "url":anchor["href"],
                                "type":category,
                                "date":"NA"})
    return header_urls

def category_news(categorical_type_news):
    categorical_news = []
    paginated_news=[]
    for news in categorical_type_news:
        news_category = list(news.keys())[0]
        page_number=1
        if news_category!="Startups":
            paginate = True
            while paginate:
                news_url = f"{news[news_category]}/page-{page_number}/"
                response = requests.get(news_url)
                soup=BeautifulSoup(response.content, 'html.parser')
                category_list = soup.find(id="cagetory")

                lis = category_list.find_all("li", {"class":"clearfix"})
                anchors=[]
                for li in lis:
                    article_date = li.find("span").get_text()
                    article_date = article_date.split(" ")  #Modified for windows time format TIMEZONE issue
                    article_date=' '.join(article_date[0:len(article_date)-1])
                    oodate = datetime.strptime(article_date, '%B %d, %Y %I:%M %p')  # .strftime('%Y-%m-%d')
                    delta = datetime.now() - oodate
                    if delta.days > DAYS:
                        paginate = False

                    anchors.append({
                        "anchor":li.find("a"),
                        "date":article_date
                    })
                categorical_news = categorical_news + extract_header_and_url(anchors, news_category)
                page_number+=1
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


def fetch_content(content_url):
    response = requests.get(content_url)
    if response:
        soup = BeautifulSoup(response.content, "html.parser")
        content_data = soup.find(id="contentdata")
        if content_data:
            paras = content_data.find_all("p")
            return paras
        return None
    return None

def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]['label']

def create_csv_file(content, name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    date = datetime.now().strftime('%Y-%m-%d')
    df = pd.DataFrame(content)
    df.to_csv(os.path.join(OUTPUT_DIR, f'{name}_{date}.csv'), index=False)

# July 22, 2024 11:47 AM IST
# %B %d, %Y %I:% %p %Z
categories, anchors = general_news(BASE_URL)
categorial_news = category_news(categories)

final_news_urls = anchors + categorial_news
create_csv_file(final_news_urls, "content_urls")
content_data=[]
for article_url in final_news_urls:
    if article_url["url"].startswith("https://www.moneycontrol.com"):
        print(article_url["url"])
        content = fetch_content(article_url["url"])
        if content:
            # sentiment = avg_sentiment(content)
            content = ' '.join(p.get_text() for p in content)
            sentiment = analyze_sentiment(content)
            article_url["content"]=content
            article_url["sentiment"]=sentiment
            # article_url["date"]=article_date
            content_data.append(article_url)
create_csv_file(content_data, "content_data")
