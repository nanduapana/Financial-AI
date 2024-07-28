import requests
import time
import csv
import os

os.makedirs('data/raw', exist_ok=True)

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
session = requests.Session()

nse_index={
    "Broad Market Indices": [
        "NIFTY 50",
        "NIFTY NEXT 50",
        "NIFTY MIDCAP 50",
        "NIFTY MIDCAP 100",
        "NIFTY MIDCAP 150",
        "NIFTY SMALLCAP 50",
        "NIFTY SMALLCAP 100",
        "NIFTY SMALLCAP 250",
        "NIFTY MIDSMALLCAP 400",
        "NIFTY 100",
        "NIFTY 200",
        "NIFTY500 MULTICAP 50:25:25",
        "NIFTY LARGEMIDCAP 250",
        "NIFTY MIDCAP SELECT",
        "NIFTY TOTAL MARKET",
        "NIFTY MICROCAP 250",
        "NIFTY 500"
    ],
    "Sectoral Indices": [
        "NIFTY AUTO",
        "NIFTY BANK",
        "NIFTY ENERGY",
        "NIFTY FINANCIAL SERVICES",
        "NIFTY FINANCIAL SERVICES 25/50",
        "NIFTY FMCG",
        "NIFTY IT",
        "NIFTY MEDIA",
        "NIFTY METAL",
        "NIFTY PHARMA",
        "NIFTY PSU BANK",
        "NIFTY REALTY",
        "NIFTY PRIVATE BANK",
        "NIFTY HEALTHCARE INDEX",
        "NIFTY CONSUMER DURABLES",
        "NIFTY OIL & GAS",
        "NIFTY MIDSMALL HEALTHCARE"
    ],
    "Thematic Indices": [
        "NIFTY COMMODITIES",
        "NIFTY INDIA CONSUMPTION",
        "NIFTY CPSE",
        "NIFTY INFRASTRUCTURE",
        "NIFTY MNC",
        "NIFTY GROWTH SECTORS 15",
        "NIFTY PSE",
        "NIFTY SERVICES SECTOR",
        "NIFTY100 LIQUID 15",
        "NIFTY MIDCAP LIQUID 15",
        "NIFTY INDIA DIGITAL",
        "NIFTY100 ESG",
        "NIFTY INDIA MANUFACTURING",
        "NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP",
        "NIFTY500 MULTICAP INDIA MANUFACTURING 50:30:20",
        "NIFTY500 MULTICAP INFRASTRUCTURE 50:30:20"
    ],
    "Strategy Indices": [
        "NIFTY DIVIDEND OPPORTUNITIES 50",
        "NIFTY50 VALUE 20",
        "NIFTY100 QUALITY 30",
        "NIFTY50 EQUAL WEIGHT",
        "NIFTY100 EQUAL WEIGHT",
        "NIFTY100 LOW VOLATILITY 30",
        "NIFTY ALPHA 50",
        "NIFTY200 QUALITY 30",
        "NIFTY ALPHA LOW-VOLATILITY 30",
        "NIFTY200 MOMENTUM 30",
        "NIFTY MIDCAP150 QUALITY 50",
        "NIFTY200 ALPHA 30",
        "NIFTY MIDCAP150 MOMENTUM 50"
    ],
    "Others": [
        "Securities in F&O",
        "Permitted to Trade"
    ]
}

with open('data/raw/nse_indices.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Index key', 'Indice', 'symbol', 'identifier', 'companyName', 'industry'])  # Write the header row

    for indice in nse_index.keys():
        for index in (nse_index[indice]):
            url=f"https://www.nseindia.com/api/equity-stockIndices?index={index}"
            try:
                response = session.get(url, headers=headers, timeout=5)
                response.raise_for_status()  # Raise an error for bad status codes
                data = response.json()  # Try to parse JSON response

                for stock in data.get('data', []):
                    meta = stock.get('meta', {})
                    company_name = meta.get('companyName', 'N/A')
                    industry = meta.get('industry', 'N/A')  # Assuming industry is nested similarly
                    
                    writer.writerow([
                        indice,
                        index,
                        stock.get('symbol'),
                        stock.get('identifier'),
                        company_name,
                        industry
                    ])

            except requests.exceptions.RequestException as e:
                print(f"Request error for {url}: {e}")
            except ValueError as e:
                print(f"JSON decode error for {url}: {e}")
            
            time.sleep(2)