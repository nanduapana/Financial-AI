
# AI-Powered Financial Portfolio Analysis using Sentiment Analysis of News Articles

## Project Overview 
This project aims to analyze financial news articles to determine their sentiment and understand the impact on financial portfolios.

## Problem Statement
This project focuses on developing an AI-powered financial risk management system for individual portfolio management. It leverages sentiment analysis of news articles to predict stock market trends and guide investment decisions. Traditional methods like fundamental and technical analysis often fall short in accounting for global events impacting market volatility. By integrating sentiment analysis from authentic news sources with AI, this system enhances stock price predictions. Combining sentiment analysis with technical and fundamental insights will provide a comprehensive and efficient tool for safer and more informed investment decisions. The project aims to simplify stock prediction access for investors.
![image](https://github.com/user-attachments/assets/125914ec-071e-4a86-8310-7737babb2710)


## Objectives
The goal of my project is to build a system that gathers news data from multiple sources, extracts and processes relevant information, analyzes the data using a Large Language Model (LLM) for roles and sentiment, summarizes the content based on sentiment, and then makes this data searchable using indexing and querying capabilities. The system also exposes APIs to enable easy retrieval of search results with different keywords.

![image](https://github.com/user-attachments/assets/1dbd2a0b-f08c-42dc-bac9-fe7e3556f43d)

## Architecture

![image](https://github.com/user-attachments/assets/e3076619-36c3-4390-8abc-f77ca74a2955)

## Data Sources

![image](https://github.com/user-attachments/assets/94a4943e-2e31-4451-8ae3-3d71e6e9df58)

## Data Pre-Processing

![image](https://github.com/user-attachments/assets/73fc8d71-b973-4a49-9d38-f7a7e96e12d5)

## Sentiment Analysis
Technique to identify the polarity of the expression as +ve, -ve or neutral or some emotions as recognized by humans. 

![image](https://github.com/user-attachments/assets/df1adf77-8b9e-44e7-a955-95a5646c36da)

## Text Summarization
It’s the technique to condense the one or more texts into shorter summaries which will give more informative insights from the complete text

![image](https://github.com/user-attachments/assets/93af6cfd-a4b4-4bd3-a8c0-d7c65a80778d)

## Types of the text Summarization

![image](https://github.com/user-attachments/assets/71afa3b6-2ec8-4989-9f66-725e72c5e9c2)

## LLM Model

![image](https://github.com/user-attachments/assets/db689e96-0bed-4c38-8327-90086a35bcc3) 

LLM are the basic models which are trained on huge amounts of data to create capabilities to resolve a wide range of the tasks and to drive the multiple use cases. 
LLM in NLP and AI are now easily available to public through openAI’s chat GPT-X, Meta’s Llama model, Google’s BERT and PaLM model. 

![image](https://github.com/user-attachments/assets/9d73dcd3-fae7-46da-b4e7-ea0e9c030f23)

## SiEBERT: English-Language Sentiment Classification Model

![image](https://github.com/user-attachments/assets/03eff44c-a264-4d04-8dc5-61a12a453ebe)

## BART (Large Model) for Summarization, Fine-tuned on CNN Daily Mail Dataset

![image](https://github.com/user-attachments/assets/d52446b6-b02e-4558-8cd1-deba094153b3)

## Search and Queries 

![image](https://github.com/user-attachments/assets/ef785ef6-2e5e-4c77-9a4d-9c6bc4974ffa)

## Output

![image](https://github.com/user-attachments/assets/2fbdc2f8-3809-40e1-9282-f8e4a66a1c65)


## Challenges faced and Future Scope

![image](https://github.com/user-attachments/assets/04b6dd63-7cd3-48ba-b73a-4007d4bf69b2)

## Conclusion

- Developed a conceptual model for stock prediction using sentiment analysis of news to support informed investments and portfolio risk management.
- Leveraged Large Language Models (LLMs) – Sibert & BART for improved accuracy and efficiency in analyzing sentiment and summarizing news articles.
- Simplified UI enables ease of use, while the project lays the foundation for future AI-based portfolio management advancements.


## Structure
- `src/`: Source code for scraping and processing news articles.
- `data/`: Directory to store collected data.
- `requirements.txt`: List of dependencies.
- `.gitignore`: Specifies which files to ignore in the repository.

## Setup
To set up the project, run:

```bash
pip install -r requirements.txt
 
=======
# Financial-AI
AI-powered Financial Portfolio Analysis using Sentiment Analysis of News Articles
>>>>>>> 85773762dc1af77158e8eea97a7f6d6dc5a84669
