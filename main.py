from data.stock_data import fetch_stock_data, select_low_correlation_stocks, preprocess_data
from data.news_data import fetch_news_data

from data.database import load_tickers, load_articles, load_optimized_portfolio, store_tickers, store_optimized_portfolio

from optimization_models.black_litterman import optimize_portfolio_black_litterman
from optimization_models.mean_variance import optimize_portfolio_mean_variance
from optimization_models.risk_tolerance import optimize_portfolio_risk_tolerance, calculate_risk_tolerance
from optimization_models.hrp import optimize_portfolio_hrp

from utils.plot_utils import plot_portfolios

# Fetch the stock data for all stocks you are considering
tickers = fetch_stock_data(
            ["MSFT", "AMZN", "KO", "MA", "COST", 
           "LUV", "XOM", "PFE", "JPM", "UNH", 
           "ACN", "DIS", "GILD", "F", "TSLA"])

# Fetch news data for the 10 low-correlation stocks
news_data = fetch_news_data(tickers, n_articles=100)

# Select the top 15 low-correlation stocks
low_correlation_stocks = select_low_correlation_stocks(tickers, n_stocks=10)

# Fetch stock data for the 10 low-correlation stocks
stock_data = fetch_stock_data(low_correlation_stocks)

# preprocess_data.py
clean_stock_data = preprocess_data(stock_data)
risk_tolerance = calculate_risk_tolerance(35, 0.5, 0.5)

# optimize_portfolios.py
bl_port = optimize_portfolio_black_litterman(clean_stock_data)
mv_port = optimize_portfolio_mean_variance(clean_stock_data)
rt_port = optimize_portfolio_risk_tolerance(clean_stock_data, risk_tolerance)
hrp_port = optimize_portfolio_hrp(clean_stock_data)

# get_weights.py
black_litterman_weights = bl_port.clean_weights()
mean_variance_weights = mv_port.clean_weights()
risk_tolerance_weights = rt_port.clean_weights()
hrp_weights = hrp_port.clean_weights()

# print_weights.py
print("Max Sharpe Ratio Portfolio Weights:\n", black_litterman_weights)
print("\nMean Variance Ratio Portfolio Weights:\n", mean_variance_weights)
print("\nRisk Tolerance Ratio Portfolio Weights:\n", risk_tolerance_weights)
print("\nHierarchical Risk Parity Portfolio Weights:\n", hrp_weights)

# plot_portfolios.py
portfolios = [bl_port, mv_port, rt_port, hrp_port]
portfolios_labels = ["Black Litterman", "Mean Variance", "Risk Tolerance", "Hierarchical Risk Parity"]

plot_portfolios(portfolios, portfolios_labels)