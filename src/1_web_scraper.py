"""
Author: Nandkumar Patil
Project: Financial-AI Project
Description: This script does data collection of news articles from news website by web scrapping method.

"""

import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from datetime import datetime, timedelta
from transformers import pipeline

BASE_URL = 'https://www.moneycontrol.com'
DAYS = 1
OUTPUT_DIR = r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\raw'

def extract_header_and_url(anchors, category="general"):
    header_urls = []
    for anchor in anchors:
        if type(anchor)==dict:
            header_urls.append({"title": anchor["anchor"]["title"],
                                "url": anchor["anchor"]["href"],
                                "type": category,
                                "date": anchor["date"]
                                })
        else:
            header_urls.append({"title":anchor["title"],
                                "url":anchor["href"],
                                "type":category,
                                "date":"NA"
                                })
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
                print(category_list, "<<<<category_list")
                if category_list:
                    lis = category_list.find_all("li", {"class":"clearfix"})
                    anchors=[]
                    for li in lis:

                        anchor_url = li.find("a")
                        
                        if anchor_url and anchor_url["href"].startswith(BASE_URL):
                            content, article_date = fetch_content(anchor_url['href'])

                            if article_date and content:
                                content = ' '.join(p.get_text() for p in content)

                                anchors.append({
                                    "title": li.find("a")['title'],
                                    "url": li.find("a")['href'],
                                    "type": news_category,
                                    "date": article_date,
                                    "content" : content,
                                })
                            else:
                                paginate = False
                                print(article_date, "====", paginate, "<<<paginate")

                    categorical_news = categorical_news + anchors 
                    page_number+=1
                    print(page_number, "<<<page_number")
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
    print(content_url)
    response = requests.get(content_url)
    print(response.status_code)
    if response:
        soup = BeautifulSoup(response.content, "html.parser")
        content_data = soup.find(id="contentdata")

        article_date = soup.find("div", {"class": "clearfix articlename_join_follow"})
        if article_date and content_data:
            article_date = article_date.find("div", {"class": "article_schedule"})
            article_date = article_date.get_text().replace("IST", "")
            article_date = check_delta(article_date)
            paras = content_data.find_all("p")
            return paras, article_date
        return None, None
    return None, None

def check_delta(date_str):
    # oodate = datetime.strptime(date_str, '%B %d, %Y %I:%M %p %Z')  # .strftime('%Y-%m-%d')
    oodate = datetime.strptime(date_str.strip(), '%B %d, %Y / %H:%M')  # .strftime('%Y-%m-%d')
    delta = datetime.now() - oodate
    if delta.days > DAYS:
        return None
    return date_str

def create_csv_file(content, name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    date = datetime.now().strftime('%Y-%m-%d')
    df = pd.DataFrame(content)
    df.to_csv(os.path.join(OUTPUT_DIR, f'{name}_{date}.csv'), index=False)

def remove_duplicates(file_name):
    df = pd.read_csv(file_name)
    df.drop_duplicates("title", inplace=True)
    df.reset_index(inplace=True)

    return df

def validate_data_frame(df):
    df = df[df.date!="NA"]
    df = df[df["url"].str.startswith!="https://www.moneycontrol.com/"]
    df.to_csv("removing_duplictes.csv")


# July 22, 2024 11:47 AM IST
# %B %d, %Y %I:% %p %Z
categories, anchors = general_news(BASE_URL)
content_data=[]
for anchor in anchors:
    if anchor["url"].startswith(BASE_URL):
        content, article_date = fetch_content(anchor["url"])
        if content:
            content = ' '.join(p.get_text() for p in content)
            anchor["content"]=content
            anchor["date"]=article_date
            content_data.append(anchor)

categorial_news = category_news(categories)
final_news_urls = anchors + categorial_news

create_csv_file(final_news_urls, "content_data")
