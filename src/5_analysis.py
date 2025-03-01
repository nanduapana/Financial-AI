"""
Author: Nandkumar Patil
Project: Financial-AI Project
Description: This script does sentiment analysis and text summarization.

"""

import os
import pandas as pd
from transformers import pipeline, AutoTokenizer
from datetime import datetime

# Get today's date in 'YYYY-MM-DD' format
today_date = datetime.now().strftime('%Y-%m-%d')

# Construct the filename with today's date
input_file_name = f'pd_content_data_{today_date}.csv'
input_file_path = os.path.join(r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\processed_data', input_file_name)

# # Load the CSV file
# csv_path = "C:/Users/nandk/Documents/Project Documentation/Financial-AI/src/data/processed_data/pd_content_data_2024-09-12.csv"
df = pd.read_csv(input_file_path)

# Initialize sentiment analysis model (siebert/sentiment-roberta-large-english)
sentiment_pipeline = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english", max_length=512, truncation=True)

# Initialize summarization model (using facebook/bart-large-cnn)
summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn",  max_length=512, truncation=True)

# Initialize tokenizer for handling token limits
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

# Function to perform sentiment analysis
def analyze_sentiment(text):
    try:
        return sentiment_pipeline(text)[0]['label']
    except:
        return "Error"

# Function to perform text summarization
def summarize_text(text, max_token_length=500):
    try:
        # Tokenize the input text to handle token limits
        tokens = tokenizer(text, truncation=True, padding='max_length', max_length=max_token_length, return_tensors="pt")
        # Decode tokens back to text for summarization
        truncated_text = tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True)
        # Summarize the truncated text
        summary = summarization_pipeline(truncated_text, max_length=200, min_length=30, do_sample=False, clean_up_tokenization_spaces=True)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error: {e}")
        return "Error"

# Apply the sentiment analysis and summarization to the content
df['Sentiment'] = df['content'].apply(analyze_sentiment)
df['Summary'] = df['content'].apply(summarize_text)

# Save the result back to the CSV
# output_csv_path = "C:/Users/nandk/Documents/Project Documentation/Financial-AI/src/data/processed_data/pd_content_data_2024-09-12_updated.csv"
df.to_csv(input_file_path , index=False)

print(f"Sentiment analysis and summarization complete. Updated CSV saved to {input_file_path}.")
