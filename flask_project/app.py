from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__,template_folder='template')

# Directory where the CSV files are located
CSV_DIRECTORY = "C:/Users/nandk/Documents/Project Documentation/Financial-AI/src/data/processed_data/"

# Function to find the latest CSV file
def get_latest_csv(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    if not csv_files:
        raise FileNotFoundError("No CSV files found in the directory.")
    
    # Sort the files by name (assuming the file name contains a date like '2024-09-12')
    csv_files.sort(reverse=True)
    return os.path.join(directory, csv_files[0])

# Function to get matching data based on stock name
def get_stock_data(stock_name):
    latest_csv_file = get_latest_csv(CSV_DIRECTORY)
    
    # Read the CSV file
    try:
        df = pd.read_csv(latest_csv_file)
    except Exception as e:
        return f"Error reading the CSV file: {e}"

    # Filter data based on the stock name (case insensitive)
    filtered_df = df[df['Stock_Names'].str.contains(stock_name, case=False, na=False)]
    
    if filtered_df.empty:
        return None

    # Return the required columns
    return filtered_df[['date', 'Sentiment', 'Summary']].to_dict(orient='records')

def count_sentiment(stock_data):
    # Initialize counters
    total_sentiments = 0
    positive_sentiments = 0
    negative_sentiments = 0

    # Loop through the articles
    for article in stock_data:
        sentiment = article['Sentiment']
        total_sentiments += 1  # Increment total sentiment count
        if sentiment == 'POSITIVE':
            positive_sentiments += 1
        elif sentiment == 'NEGATIVE':
            negative_sentiments += 1

    return total_sentiments,positive_sentiments,negative_sentiments


@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    stock_name = ""
    total_sentiments = 0
    positive_sentiments = 0
    negative_sentiments = 0

    if request.method == 'POST':

        stock_name = request.form.get('stock_name')  # Get the stock name from the form

        if stock_name:
            stock_data = get_stock_data(stock_name)  # Get stock data if name is provided
            print(stock_data)
            total_sentiments,positive_sentiments,negative_sentiments=count_sentiment(stock_data)
    
    return render_template('index.html', stock_name=stock_name, stock_data=stock_data, TOTAL=total_sentiments, POSITIVE=positive_sentiments, NEGATIVE=negative_sentiments)

if __name__ == '__main__':
    app.run(debug=True)
