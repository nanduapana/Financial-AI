"""
Author: Nandkumar Patil
Project: Financial-AI Project
Description: This script does preprocessign of the news article data.

"""

import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords  # Import stopwords for removal
from nltk.tokenize import word_tokenize  # Import for tokenization

# To download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_data(data_path, output_path):
    # To read the CSV data
    df = pd.read_csv(data_path)

    # To debug: Print the columns of the DataFrame
    print(f"Columns in the DataFrame: {df.columns.tolist()}")

    # To ensure the 'content' column exists before proceeding
    if 'content' not in df.columns:
        raise KeyError("The 'content' column is missing from the DataFrame")

    # 1. Remove duplicate records based on 'url'
    df.drop_duplicates(subset=['url'], inplace=True)

    # 2. Remove records where 'content' is missing
    df.dropna(subset=['content'], inplace=True)

    # Convert the date column to datetime & Add the latest date to rows with missing 'date'
    df['date'] = df['date'].str.strip()
    df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y / %H:%M', errors='coerce').dt.date
    print(df['date'])
    df['date'] = df['date'].replace(['NA', ''], pd.NA)
    df['date'] = df['date'].bfill()

    # 5. Preprocessing steps for the 'content' column
    df['content'] = df['content'].apply(preprocess_text)

    # To Save the preprocessed data
    df.to_csv(output_path, index=False)
    print(df)
    return df

def preprocess_text(text):
    # 6. Lowercase conversion
    text = text.lower()

    # 7. Remove hyperlinks
    text = re.sub(r'http\S+', '', text)

    # 8. Remove URLs
    text = re.sub(r'www\S+', '', text)

    # 9. Remove hashtags
    text = re.sub(r'#\w+', '', text)

    # 10. Tokenize and remove stopwords
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # 11. Remove content in abbreviations in round brackets
    text = re.sub(r'\(.*?\)', '', text)

    # 12. Remove punctuations
    text = re.sub(r'[^\w\s]', '', ' '.join(tokens))

    return text

# Data directory path
data_dir = r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data'

# To get all CSV files in the raw data folder
raw_data_folder = os.path.join(data_dir, "raw")
raw_csv_file = [f for f in os.listdir(raw_data_folder) if f.endswith(".csv") and f.startswith("content_data_")]
data_path = os.path.join(raw_data_folder, raw_csv_file[0] )

# Create the processed_data folder if it doesn't exist
processed_data_folder = os.path.join(data_dir, "processed_data")
os.makedirs(processed_data_folder, exist_ok=True)  # Create processed_data folder if needed

output_path = os.path.join(processed_data_folder, f"pd_{raw_csv_file[0]}")

df = preprocess_data(data_path, output_path)
print(f"Processed data saved to: {output_path}")