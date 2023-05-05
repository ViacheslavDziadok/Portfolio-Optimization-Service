from pypfopt import HRPOpt

def optimize_portfolio_hrp(stock_data):
    hrp = HRPOpt(stock_data)
    hrp.optimize()
    return hrp