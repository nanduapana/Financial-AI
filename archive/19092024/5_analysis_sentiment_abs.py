from transformers import pipeline, RobertaTokenizer
import pandas as pd
import re

# Load the sentiment analysis pipeline and tokenizer
sentiment_analyzer = pipeline("text-classification", model="siebert/sentiment-roberta-large-english", max_length=512, truncation=True)
tokenizer = RobertaTokenizer.from_pretrained("siebert/sentiment-roberta-large-english")

def extract_aspect_sentences(text, aspects):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    aspect_sentences = {aspect: [] for aspect in aspects}
    print(aspect_sentences)
    for sentence in sentences:
        for aspect in aspects:
            if aspect.lower() in sentence.lower():
                aspect_sentences[aspect].append(sentence)
    return aspect_sentences

def get_aspect_sentiments(content, aspects):
    max_length = 512
    aspect_sentiments = {aspect: [] for aspect in aspects}
    print(aspect_sentiments)
    aspect_sentences = extract_aspect_sentences(content, aspects)
    
    for aspect, sentences in aspect_sentences.items():
        for sentence in sentences:
            tokens = tokenizer.encode(sentence, add_special_tokens=False)
            # Process tokens in chunks
            for i in range(0, len(tokens), max_length):
                chunk = tokens[i:i + max_length]
                chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
                sentiment_result = sentiment_analyzer(chunk_text)
                sentiment_label = sentiment_result[0]['label']
                aspect_sentiments[aspect].append(sentiment_label)
    
    # Aggregate sentiments for each aspect
    aggregated_sentiments = {aspect: ', '.join(labels) for aspect, labels in aspect_sentiments.items()}
    return aggregated_sentiments

csv_path = "C:/Users/nandk/Documents/Project Documentation/Financial-AI/src/data/processed_data/pd_content_data_2024-09-12.csv"
df = pd.read_csv(csv_path)

def analyze_sentiment(row):
    content = row['content']
    aspects = row['Stock_Names'].split(',')
    sentiments = get_aspect_sentiments(content, aspects)
    return sentiments

sentiments_df = df.apply(analyze_sentiment, axis=1)

results = []
for idx, row in sentiments_df.iteritems():
    for aspect, sentiment in row.items():
        results.append({
            'Index': idx,
            'Stock_Name': aspect,
            'Sentiment': sentiment
        })

results_df = pd.DataFrame(results)
output_path = "C:/Users/nandk/Documents/Project Documentation/Financial-AI/src/data/processed_data/sentiment_output.csv"
results_df.to_csv(output_path, index=False)

print("Sentiment analysis completed and saved to:", output_path)
