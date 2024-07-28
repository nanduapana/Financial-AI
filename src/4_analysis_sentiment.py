import os
import pandas as pd
from datetime import datetime
from transformers import pipeline

sentiment_analyzer = pipeline('sentiment-analysis', max_length=512, truncation=True)
INPUT_DIR = 'data/raw'
OUTPUT_DIR = 'data/analyzed'

def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]['label']

def create_csv_file(content, name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    date = datetime.now().strftime('%Y-%m-%d')
    df = pd.DataFrame(content)
    df.to_csv(os.path.join(OUTPUT_DIR, f'{name}_{date}.csv'), index=False)

if __name__ == "__main__":
    input_file = os.path.join(INPUT_DIR, f'content_urls_{datetime.now().strftime("%Y-%m-%d")}.csv')
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} not found. Ensure you have run web_scraping.py first.")

    df = pd.read_csv(input_file)
    content_data = []

    for _, row in df.iterrows():
        url = row["url"]
        response = requests.get(url)
        if response:
            soup = BeautifulSoup(response.content, "html.parser")
            content_data_elem = soup.find(id="contentdata")
            if content_data_elem:
                content = ' '.join(p.get_text() for p in content_data_elem.find_all("p"))
                sentiment = analyze_sentiment(content)
                row["content"] = content
                row["sentiment"] = sentiment
                content_data.append(row)

    create_csv_file(content_data, "content_data")
