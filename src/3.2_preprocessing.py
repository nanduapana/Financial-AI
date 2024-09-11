import pandas as pd
import re
import os
from datetime import datetime

# Get today's date in 'YYYY-MM-DD' format
today_date = datetime.now().strftime('%Y-%m-%d')

# Construct the filename with today's date
input_file_name = f'nse_indices_{today_date}.csv'
input_file_path = os.path.join(r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\raw', input_file_name)

# Check if the file exists
if os.path.isfile(input_file_path):
    # Load the CSV file
    df = pd.read_csv(input_file_path)

    # 1. Remove duplicate data based on 'ISIN'
    df.drop_duplicates(subset='ISIN', inplace=True)

    # 2, 3, and 4. Clean the 'Company' names by:
    # - Converting to lower case
    # - Removing stop words and other specific words
    def clean_company_name(name):
        # Convert to lower case
        name = name.lower()

        stop_words = ['limited', 'service', 'private', 'general', 'insurance', 'company']

        # Remove unwanted words
        name = re.sub(r'\b(?:' + '|'.join(stop_words) + r')\b', '', name)

        # Remove special characters (keep only alphanumeric and spaces)
        name = re.sub(r'[^a-zA-Z0-9\s]', '', name)

        # Remove text inside round and square brackets
        name = re.sub(r'\(.*?\)|\[.*?\]', '', name)

        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    # Create a new column 'Processed_Company' with cleaned company names
    df['Processed_Company'] = df['Company'].apply(clean_company_name)

    # Save the cleaned data to a new CSV file with prefix 'pd_nse_indices_' and today's date
    output_file_name = f'pd_nse_indices_{today_date}.csv'
    output_file_path = os.path.join(r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\processed_data', output_file_name)
    df.to_csv(output_file_path, index=False)

    print(f"Preprocessed file saved to: {output_file_path}")

else:
    print(f"File not found: {input_file_path}")
