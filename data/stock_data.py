import yfinance as yf
import pandas as pd
import database as db

def fetch_stock_data(tickers, start_date='2021-01-01', end_date='2022-01-01'):
    stock_data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return stock_data

def save_stock_data(tickers):
    db.store_tickers(tickers)

def select_low_correlation_stocks(stock_data, n_stocks=100):
    # Calculate the correlation matrix
    corr_matrix = stock_data.corr()

    # Find the tickers with the lowest average correlation
    mean_correlations = corr_matrix.mean().sort_values()

    # Select the top n_stocks with the lowest correlation
    low_correlation_stocks = mean_correlations.head(n_stocks).index.tolist()

    return low_correlation_stocks

def preprocess_data(stock_data):
    # Drop any rows with missing values
    stock_data = stock_data.dropna()
    
    # Ensure all data types are numeric
    stock_data = stock_data.apply(pd.to_numeric, errors="coerce")
    
    return stock_data