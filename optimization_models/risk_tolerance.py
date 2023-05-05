from pypfopt import expected_returns
from pypfopt import EfficientFrontier
from pypfopt import risk_models

def calculate_risk_tolerance(age, financial_state, risk_aversion):
    # We use a simple weighted average for the starting point
    age_factor = 1 - age / 100
    risk_tolerance = (age_factor * 0.5) + (financial_state * 0.3) + (risk_aversion * 0.2)
    return risk_tolerance

def optimize_portfolio_risk_tolerance(stock_data, risk_tolerance, target_return_factor=0.75):
    # Calculate expected returns and covariance matrix
    mu = expected_returns.mean_historical_return(stock_data)
    cov_matrix = risk_models.sample_cov(stock_data)

    # Adjust the target return based on risk tolerance
    min_return = mu.min()
    max_return = mu.max()
    target_return = min_return + (max_return - min_return) * risk_tolerance * target_return_factor

    # Create the Efficient Frontier object
    ef = EfficientFrontier(mu, cov_matrix)

    # Minimize risk for the given target return
    ef.efficient_return(target_return)

    return ef