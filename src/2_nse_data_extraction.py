import requests
import time
import csv
import os
import pandas as pd
from datetime import datetime

# To define the directory for saving the CSV file
csv_directory = r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\raw'

# To ensure the directory exists
os.makedirs(csv_directory, exist_ok=True)

# Get the current date and format it as YYYY-MM-DD
current_date = datetime.now().strftime("%Y-%m-%d")

# Define the CSV file name with the current date
csv_file_name = f"nse_indices_{current_date}.csv"
csv_file_path = os.path.join(csv_directory, csv_file_name)

# To define the NSE indices data
nse_index = [
    "NIFTY 50", "NIFTY NEXT 50", "NIFTY MIDCAP 50", "NIFTY MIDCAP 100", "NIFTY MIDCAP 150", 
    "NIFTY SMALLCAP 50", "NIFTY SMALLCAP 100", "NIFTY SMALLCAP 250", "NIFTY MIDSMALLCAP 400", 
    "NIFTY 100", "NIFTY 200", "NIFTY500 MULTICAP 50:25:25", "NIFTY LARGEMIDCAP 250", 
    "NIFTY MIDCAP SELECT", "NIFTY TOTAL MARKET", "NIFTY MICROCAP 250", "NIFTY 500", 
    "NIFTY AUTO", "NIFTY BANK", "NIFTY ENERGY", "NIFTY FINANCIAL SERVICES", 
    "NIFTY FINANCIAL SERVICES 25/50", "NIFTY FMCG", "NIFTY IT", "NIFTY MEDIA", 
    "NIFTY METAL", "NIFTY PHARMA", "NIFTY PSU BANK", "NIFTY REALTY", "NIFTY PRIVATE BANK", 
    "NIFTY HEALTHCARE INDEX", "NIFTY CONSUMER DURABLES", "NIFTY OIL & GAS", 
    "NIFTY MIDSMALL HEALTHCARE", "NIFTY COMMODITIES", "NIFTY INDIA CONSUMPTION", 
    "NIFTY CPSE", "NIFTY INFRASTRUCTURE", "NIFTY MNC", "NIFTY GROWTH SECTORS 15", 
    "NIFTY PSE", "NIFTY SERVICES SECTOR", "NIFTY100 LIQUID 15", "NIFTY MIDCAP LIQUID 15", 
    "NIFTY INDIA DIGITAL", "NIFTY100 ESG", "NIFTY INDIA MANUFACTURING", 
    "NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP", 
    "NIFTY500 MULTICAP INDIA MANUFACTURING 50:30:20", 
    "NIFTY500 MULTICAP INFRASTRUCTURE 50:30:20", "NIFTY DIVIDEND OPPORTUNITIES 50", 
    "NIFTY50 VALUE 20", "NIFTY100 QUALITY 30", "NIFTY50 EQUAL WEIGHT", "NIFTY100 EQUAL WEIGHT", 
    "NIFTY100 LOW VOLATILITY 30", "NIFTY ALPHA 50", "NIFTY200 QUALITY 30", 
    "NIFTY ALPHA LOW-VOLATILITY 30", "NIFTY200 MOMENTUM 30", "NIFTY MIDCAP150 QUALITY 50", 
    "NIFTY200 ALPHA 30", "NIFTY MIDCAP150 MOMENTUM 50"
]

# To define headers for the API request
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}

# Start session to persist connection
session = requests.Session()
session.headers.update(headers)
session.get("https://www.nseindia.com")

nse_data = []

# Fetching data for each index
for index in nse_index:
    url = f"https://www.nseindia.com/api/equity-stockIndices"
    
    response = session.get(url, params={'index': index})
    print(response.status_code)

    if response.status_code != 200:
        print(f"Failed to retrieve data for index: {index}")
    else:
        index_response = response.json()

        # Skip the first element (if you need to)
        index_response = index_response['data'][1:]

        for equity in index_response:
            nse_data.append({
                'Symbol': equity['symbol'],
                'Identifier': equity['identifier'],
                'Company': equity['meta']['companyName'],
                'ISIN': equity['meta']['isin'],
                'Sector': index
            })

        print(f"Data fetched for {index}")
    time.sleep(3)  # To avoid too many requests in a short time

# Convert list of dictionaries to DataFrame and save to CSV
df = pd.json_normalize(nse_data)
df.to_csv(csv_file_path, index=False)

print(f"Data saved to {csv_file_path}")
