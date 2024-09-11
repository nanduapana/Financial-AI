# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
from transformers import pipeline
import glob
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Load transformer models for sentiment analysis and summarization
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
summarization_model = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to find the latest CSV file in the directory based on date in the filename
def get_latest_csv_file():
    folder_path = r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\processed_data'
    file_pattern = os.path.join(folder_path, 'processed_data_content_data_*.csv')
    
    # Get all files that match the pattern
    files = glob.glob(file_pattern)
    
    if not files:
        return None
    
    # Extract the date from the file names and find the latest one
    files_with_dates = []
    for file in files:
        try:
            date_str = file.split('_')[-1].split('.csv')[0]
            file_date = datetime.strptime(date_str, '%Y-%m-%d')
            files_with_dates.append((file_date, file))
        except ValueError:
            continue
    
    if files_with_dates:
        latest_file = max(files_with_dates, key=lambda x: x[0])[1]
        return latest_file
    else:
        return None

# Function to analyze sentiment using the transformer model
def analyze_sentiment(content):
    try:
        result = sentiment_model(content[:512])  # Limit to 512 characters due to model constraints
        return result[0]['label']  # Return the sentiment label (Positive/Negative)
    except Exception as e:
        return "Error in sentiment analysis"

# Function to summarize the content using the transformer model
def summarize_content(content):
    try:
        summary = summarization_model(content[:1024], max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return "Error in summarization"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    stock_name = request.form['stock_name'].lower()
    csv_file = get_latest_csv_file()
    
    if not csv_file:
        return jsonify({"message": "No data files found in the specified directory."}), 404
    
    df = pd.read_csv(csv_file)
    filtered_df = df[df['stock_map'].str.contains(stock_name, case=False, na=False)]

    if filtered_df.empty:
        return jsonify({"message": "No data found for the specified stock."}), 404

    filtered_df['Sentiment'] = filtered_df['content'].apply(analyze_sentiment)
    filtered_df['Summary'] = filtered_df['content'].apply(summarize_content)
    
    filtered_data = filtered_df[['date', 'Summary', 'Sentiment']].to_dict(orient='records')

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
