from data.stock_data import fetch_stock_data, select_low_correlation_stocks, preprocess_data
from data.news_data import fetch_news_data, get_sentiment_scores

from data.database import load_all_optimized_portfolios

from optimization_models.PortfolioOptimizer import PortfolioOptimizer
from optimization_models.risk_tolerance import optimize_portfolio_risk_tolerance, calculate_risk_tolerance

from utils.plot_utils import plot_portfolios

def whole_pipeline(selected_companies, start_date, end_date):

    stock_data = fetch_stock_data(selected_companies, start_date, end_date, load_from_database=False)

    # Select the top low-correlation stocks
    # low_correlation_stocks = select_low_correlation_stocks(stock_data, n_stocks=10)

    # Fetch stock data for the low-correlation stocks
    # stock_data = fetch_stock_data(low_correlation_stocks)

    # Fetch news data for the low-correlation stocks
    news_data = fetch_news_data(stock_data, n_articles=10, load_from_database=False)
    sentiment_scores = get_sentiment_scores(news_data)

    # preprocess_data.py
    clean_stock_data = preprocess_data(stock_data)
    risk_tolerance = calculate_risk_tolerance(35, 0.5, 0.5)

    # optimize_portfolios.py
    port_opt = PortfolioOptimizer(clean_stock_data, risk_tolerance)
    portfolios = port_opt.optimize("all")

    # [portfolio.save() for portfolio in portfolios]

    # portfolios = PortfolioOptimizer.load("all")

    # get_weights.py
    weights = [portfolio.clean_weights for portfolio in portfolios]

    # print_weights.py
    [print(f"{portfolio.name.title()} weights: {weights}") for portfolio, weights in zip(portfolios, weights)]

    # plot_portfolios.py
    return plot_portfolios(portfolios)