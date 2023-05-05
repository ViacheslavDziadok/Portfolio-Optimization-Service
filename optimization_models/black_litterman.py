from pypfopt import expected_returns
from pypfopt import BlackLittermanModel, EfficientFrontier
from pypfopt import CovarianceShrinkage

def optimize_portfolio_black_litterman(stock_data):
    cov_matrix = CovarianceShrinkage(stock_data).ledoit_wolf()
    market_prior = expected_returns.capm_return(stock_data)

    # Example views on stocks (replace with your views)
    viewdict = {
        "TSLA": 0.1,  # Stock 0 will return 10%
        "F": -0.05  # Stock 3 will return -5%
    }

    delta = 2  # Risk aversion parameter
    bl = BlackLittermanModel(cov_matrix, pi=market_prior, absolute_views=viewdict, delta=delta)

    posterior_returns = bl.bl_returns()
    posterior_cov_matrix = bl.bl_cov()

    # Calculate optimal weights using Efficient Frontier with the Black-Litterman expected returns and covariance matrix
    ef = EfficientFrontier(posterior_returns, posterior_cov_matrix)
    ef.efficient_return(target_return=0.1)
    
    return ef