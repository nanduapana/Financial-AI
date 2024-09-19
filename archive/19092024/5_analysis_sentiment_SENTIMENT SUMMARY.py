from transformers import pipeline
import pandas as pd

# Load the sentiment analysis pipeline
sentiment_analyzer = pipeline("text-classification", model="siebert/sentiment-roberta-large-english")

# Function to get sentiment for content based on stock names
def get_sentiment_roberta(content):
    # Tokenize the content and break it into chunks of 512 tokens
    max_length = 512  # Maximum number of tokens for RoBERTa

    # Split content into chunks based on the model's maximum input length
    chunks = [content[i:i + max_length] for i in range(0, len(content), max_length)]

    # Process each chunk and aggregate the results
    sentiments = []
    for chunk in chunks:
        sentiment_result = sentiment_analyzer(chunk)
        sentiments.append(sentiment_result[0]['label'])

    # Combine the sentiments for all chunks
    return ', '.join(sentiments)

# Load your CSV file
csv_path = "C:/Users/nandk/Documents/Project Documentation/Financial-AI/src/data/processed_data/pd_content_data_2024-09-12.csv"
df = pd.read_csv(csv_path)

# Function to analyze sentiment for each row based on stock names
def analyze_sentiment(row):
    content = row['content']
    sentiment = get_sentiment_roberta(content)
    return sentiment

# Apply sentiment analysis to each row in the DataFrame
df['Sentiments'] = df.apply(analyze_sentiment, axis=1)

# Save the results to a new CSV
# output_path = "C:/Users/nandk/Documents/Project Documentation/Financial-AI/src/data/processed_data/sentiment_output.csv"
df.to_csv(csv_path, index=False)

print("Sentiment analysis completed and saved to:", csv_path)
