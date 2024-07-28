import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords  # Import stopwords for removal
from nltk.tokenize import word_tokenize  # Import for tokenization

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_data(data_path, output_path):
    # Read the CSV data
    df = pd.read_csv(data_path)

    # Debug: Print the columns of the DataFrame
    print(f"Columns in the DataFrame: {df.columns.tolist()}")

    # Ensure the 'content' column exists before proceeding
    if 'content' not in df.columns:
        raise KeyError("The 'content' column is missing from the DataFrame")

    # 1. Remove duplicate records based on 'url'
    df.drop_duplicates(subset=['url'], inplace=True)

    # 2. Remove records where 'content' is missing
    df.dropna(subset=['content'], inplace=True)

    # 3. Parse the 'date' column with the specified format
    df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y %I:%M %p', errors='coerce')

    # 4. Add the latest date to rows with missing 'date'
    latest_date = df['date'].max()
    df['date'] = df['date'].fillna(latest_date)

    # 5. Preprocessing steps for the 'content' column
    df['content'] = df['content'].apply(preprocess_text)

    # Save the preprocessed data
    df.to_csv(output_path, index=False)

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
data_dir = r"C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data"

# Get all CSV files in the raw data folder
raw_data_folder = os.path.join(data_dir, "raw")
csv_files = [f for f in os.listdir(raw_data_folder) if f.endswith(".csv") and f.startswith("content_data_")]

# Process each CSV file
for filename in csv_files:
    # Construct data paths
    data_path = os.path.join(raw_data_folder, filename)
    processed_data_folder = os.path.join(data_dir, "processed_data")  # Create processed_data folder if it doesn't exist
    os.makedirs(processed_data_folder, exist_ok=True)  # Create processed_data folder if needed

    # Define the output path with the new naming convention
    output_path = os.path.join(processed_data_folder, f"processed_data_{filename}")

    # Preprocess and save the data
    df = preprocess_data(data_path, output_path)
    print(f"Processed data saved to: {output_path}")
