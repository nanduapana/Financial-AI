import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase
    return text

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return ' '.join(filtered_text)

def preprocess_data(input_file, output_file):
    df = pd.read_csv(input_file)
    df['clean_content'] = df['content'].apply(clean_text).apply(remove_stopwords)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    INPUT_FILE = 'data/raw/news_articles.csv'
    OUTPUT_FILE = 'data/processed/news_articles_clean.csv'
    preprocess_data(INPUT_FILE, OUTPUT_FILE)
