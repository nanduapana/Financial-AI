import openai
import pandas as pd

# Load the data
df = pd.read_csv(r'C:\Users\nandk\Documents\Project Documentation\Financial-AI\article_csv.csv')

# Set your OpenAI API key
openai.api_key = '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'

# Function to perform sentiment analysis using ChatGPT
def analyze_sentiment(content, stock):
    prompt = f"Analyze the following news article for sentiment with respect to the stock '{stock}'. Provide sentiment as Positive, Negative, or Neutral and explain the reasoning: \n\n{content}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial analyst specialized in stock market sentiment analysis."},
            {"role": "user", "content": prompt}
        ]
    )
    
    sentiment = response['choices'][0]['message']['content'].strip()
    return sentiment

# Apply sentiment analysis to each article's content and map it to the stock
results = []
for index, row in df.iterrows():
    stock_map = row['stock_map']
    content = row['content']
    sentiment_result = analyze_sentiment(content, stock_map)
    results.append({'stock': stock_map, 'sentiment': sentiment_result})

# Convert results to DataFrame
sentiment_df = pd.DataFrame(results)

# Display results grouped by stock
stock_results = sentiment_df.groupby('stock').apply(lambda x: x[['sentiment']])
print(stock_results)
