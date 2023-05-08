import yfinance as yf
import pandas as pd
from database import load_tickers, store_tickers

def fetch_stock_data(tickers, start_date='2021-01-01', end_date='2022-01-01', load_from_database=False):
    """
    Fetches stock data for a list of stocks from Yahoo Finance.
    :param tickers: list of stocks to fetch data for
    :param start_date: start date for fetching data
    :param end_date: end date for fetching data
    :param load_from_database: whether to load tickers from database or fetch them from Yahoo Finance
    :return: dictionary of stock data for each stock
    """
    if load_from_database:
        # Load tickers from database
        stock_data = load_tickers()
    else:
        stock_data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        store_tickers(stock_data)
    return stock_data

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