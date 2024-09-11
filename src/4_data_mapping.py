import pandas as pd
import re

# Step 1: Load the data from the CSV files
# Path to the article content CSV file
article_file_path = r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\processed_data\processed_data_content_data_2024-07-28.csv'

# Path to the NSE indices CSV file
nse_file_path = r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\processed_data\nse_indices.csv'

# Load the articles data
news_df = pd.read_csv(article_file_path)

# Load the stock company list
stocks_df = pd.read_csv(nse_file_path)

# Step 2: Clean and preprocess stock names
# Convert stock company names to lowercase and strip extra whitespace for consistency
stocks_df['Company'] = stocks_df['Company'].str.lower().str.strip()

# Step 3: Define a function to map companies to articles
def map_stocks_to_article(article_text, stock_names):
    # Clean and lowercase the article text for matching
    article_text_cleaned = article_text.lower()
    
    # Find all companies mentioned in the article content
    matched_companies = [company for company in stock_names if re.search(r'\b' + re.escape(company) + r'\b', article_text_cleaned)]
    
    # Return a comma-separated list of matched companies if any are found
    return ', '.join(matched_companies) if matched_companies else None

# Step 4: Apply the mapping logic to map stocks to each article
# Assuming the news articles dataset has a 'content' column containing the article's main text
news_df['MappedCompanies'] = news_df['content'].apply(lambda x: map_stocks_to_article(x, stocks_df['Company'].tolist()))

# Step 5: Save the updated dataset with mapped companies
output_file_path = r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\src\data\processed_data\mapped_news_articles_2024-07-28.csv'
news_df.to_csv(output_file_path, index=False)

print(f'Mapping completed. Mapped articles saved to {output_file_path}')
