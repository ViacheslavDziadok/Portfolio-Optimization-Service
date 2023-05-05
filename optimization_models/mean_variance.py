from pypfopt import EfficientFrontier
from pypfopt import expected_returns
from pypfopt import CovarianceShrinkage

def optimize_portfolio_mean_variance(stock_data):
    mu = expected_returns.mean_historical_return(stock_data)
    cov_matrix = CovarianceShrinkage(stock_data).ledoit_wolf()
    ef = EfficientFrontier(mu, cov_matrix)
    ef.min_volatility()
    return ef