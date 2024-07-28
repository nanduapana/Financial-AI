import pandas as pd
import os
import re
import nltk
from nltk.corpus import stopwords  # Import stopwords for removal
from nltk.tokenize import word_tokenize  # Import for tokenization
from nltk.stem import PorterStemmer  # Import for stemming (optional)

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_data(data_path, output_path):
    # Read the CSV data
    df = pd.read_csv(data_path)

    # Get the text column 'content'
    text_column = 'content'  

    # Preprocessing steps for the text column:
    df[text_column] = df[text_column].apply(lambda text: preprocess_text(text))

    # Save the preprocessed data
    df.to_csv(output_path, index=False)

    return df

def preprocess_text(text):
    # Lowercase conversion
    text = text.lower()

    # Remove punctuation (consider keeping emoticons if relevant)
    text = re.sub(r'[^\w\s]', '', text)  # Replace with a more granular approach if needed

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords (consider keeping financial terms if relevant)
    stop_words = set(stopwords.words('english'))  # Download stopwords if needed
    tokens = [word for word in tokens if word not in stop_words]

    # Optional: Stemming or lemmatization (consider for consistency)
    # stemmer = PorterStemmer()  # You can choose PorterStemmer or WordNetLemmatizer
    # tokens = [stemmer.stem(word) for word in tokens]

    # Join tokens back to a single string
    cleaned_text = ' '.join(tokens)

    return cleaned_text

# Data directory path
data_dir = r"C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data"

# Get all CSV files in the raw data folder
raw_data_folder = os.path.join(data_dir, "raw")
csv_files = [f for f in os.listdir(raw_data_folder) if f.endswith(".csv")]

# Process each CSV file
for filename in csv_files:
    # Construct data paths
    data_path = os.path.join(raw_data_folder, filename)
    processed_data_folder = os.path.join(data_dir, "processed_data")  # Create processed_data folder if it doesn't exist
    os.makedirs(processed_data_folder, exist_ok=True)  # Create processed_data folder if needed
    output_path = os.path.join(processed_data_folder, filename)

    # Preprocess and save the data
    df = preprocess_data(data_path, output_path)
    print(f"Processed data saved to: {output_path}")

