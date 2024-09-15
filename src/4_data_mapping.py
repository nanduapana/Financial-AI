"""
Author: Nandkumar Patil
Project: Financial-AI Project
Description: This script does mapping of stock against the news articles.

"""
import pandas as pd
import re
from datetime import datetime
import json

# Step 1: Get the current date in the format YYYY-MM-DD
current_date = datetime.now().strftime('%Y-%m-%d')

# Step 2: Build the file path for the article content CSV file
article_file_name = f'pd_content_data_{current_date}.csv'
article_file_path = rf'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\processed_data\{article_file_name}'
print(article_file_path)

# Path to the NSE indices CSV file
stock_file_name = f'pd_nse_indices_{current_date}.csv'
stock_file_path = rf'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\processed_data\{stock_file_name}'
print(stock_file_path)

# Step 3: Define a function to map companies to articles
# def map_stocks():
#     article_df = pd.read_csv(article_file_path)
#     article_json = article_df.to_json(orient='records')
#     article_json = json.loads(article_json)

#     stocks_df = pd.read_csv(stock_file_path)

#     Company_Name = stocks_df["Processed_Company"]
#     mapped_stocks = []
#     for art in article_json:
#         searched_stocks = []

#         for sym in Company_Name:
#             if type(sym) == str and type(art["content"]) == str:
#                 aa = re.search(rf'\b{sym}\b', art["content"].lower())
#                 if aa:
#                     searched_stocks.append(aa.group(0))

#         if len(searched_stocks) > 0:
#             art["stock_map"] = ",".join(searched_stocks)
#         else:
#             art["stock_map"] = "NA"
#     outputFile = open("article_json.json", "w")
#     json.dump(article_json, outputFile, indent=6)
#     outputFile.close()
#     df = pd.read_json("article_json.json")
#     df.to_csv("article_csv.csv")
#     pass

# map_stocks()

content_df = pd.read_csv(article_file_path)
stock_df = pd.read_csv(stock_file_path)
stock_names = stock_df['Processed_Company'].tolist()

def find_stocks_in_content(content, stocks):
    found_stocks = [stock for stock in stocks if stock.lower() in content.lower()]
    return ', '.join(found_stocks) if found_stocks else 'NA'

content_df['Stock_Names'] = content_df['content'].apply(lambda x: find_stocks_in_content(x, stock_names))

content_df.to_csv(article_file_path, index=False)