import config
import requests
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from datetime import datetime, timedelta

def fetch_news_data(tickers, n_articles=1):
    """
    Fetches news data for a list of stocks from the NewsAPI API.
    :param tickers: list of stocks to fetch news data for
    :param n_articles: number of articles to fetch for each stock
    :return: dictionary of news data for each stock
    """

    API_KEY = config.NEWSAPI_KEY  # NewsAPI key

    # Set up FinancialBERT model and tokenizer
    model_name = config.FinancialBERT
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)

    # Retrieve articles from NewsAPI for each ticker symbol
    articles = pd.DataFrame()
    today = datetime.today().strftime('%Y-%m-%d')
    month_ago = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    for ticker in tickers:
        url = f"https://newsapi.org/v2/top-headlines?q={ticker}&from={month_ago}&to={today}&category=business&pageSize={n_articles}&apiKey={API_KEY}"
        response = requests.get(url)
        articles_ticker = pd.DataFrame(response.json()["articles"])
        articles_ticker["ticker"] = ticker
        articles = pd.concat([articles, articles_ticker], ignore_index=True)

    # Pre-process articles
    articles["text"] = articles["title"] + " " + articles["description"]
    articles["text"] = articles["text"].str.lower()
    articles["text"] = articles["text"].str.replace("[^\w\s]", "")
    articles["text"] = articles["text"].str.replace("\d+", "")
    articles["text"] = articles["text"].str.strip()
    articles = articles.drop_duplicates(subset=["text"]).dropna()

    # Tokenize and prepare input for FinancialBERT model
    nlp = pipeline(task="sentiment-analysis", model=model, tokenizer=tokenizer)
    results = nlp(list(articles["text"]))

    if results:
        # Extract sentiment scores from the results
        articles["sentiment"] = [result['label'] for result in results]

    # Aggregate sentiment scores by ticker symbol
    sentiment_scores = articles.groupby("ticker")["sentiment"].mean().to_dict()

    return sentiment_scores