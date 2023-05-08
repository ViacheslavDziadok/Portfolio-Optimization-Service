from data.stock_data import fetch_stock_data, select_low_correlation_stocks, preprocess_data
from data.news_data import fetch_news_data, get_sentiment_scores

from data.database import load_tickers, load_articles, load_optimized_portfolio, store_tickers, store_optimized_portfolio

from optimization_models.PortfolioOptimizer import PortfolioOptimizer
from optimization_models.risk_tolerance import optimize_portfolio_risk_tolerance, calculate_risk_tolerance

from utils.plot_utils import plot_portfolios

# Fetch the stock data for all stocks you are considering
tickers = fetch_stock_data(
            ["MSFT", "AMZN", "KO", "MA", "COST", 
           "LUV", "XOM", "PFE", "JPM", "UNH", 
           "ACN", "DIS", "GILD", "F", "TSLA"],
           load_from_database=False)

# Fetch news data for the 10 low-correlation stocks
news_data = fetch_news_data(tickers, n_articles=100, load_from_database=False)
sentiment_scores = get_sentiment_scores(news_data)

# Select the top 15 low-correlation stocks
low_correlation_stocks = select_low_correlation_stocks(tickers, n_stocks=10)

# Fetch stock data for the 10 low-correlation stocks
stock_data = fetch_stock_data(low_correlation_stocks)

# preprocess_data.py
clean_stock_data = preprocess_data(stock_data)
risk_tolerance = calculate_risk_tolerance(35, 0.5, 0.5)

# optimize_portfolios.py
port_opt = PortfolioOptimizer(clean_stock_data, risk_tolerance, news_data)
portfolios = port_opt.optimize("all")

# get_weights.py
weights = [portfolio.clean_weights for portfolio in portfolios]

# print_weights.py
[print(f"{portfolio.name.capitalize()} weights: {weights}") for portfolio, weights in zip(portfolios, weights)]

# plot_portfolios.py, rt_port, hrp_port]

plot_portfolios(portfolios)