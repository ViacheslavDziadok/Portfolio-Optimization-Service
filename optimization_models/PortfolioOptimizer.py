from pypfopt import expected_returns, CovarianceShrinkage
from pypfopt import BlackLittermanModel, EfficientFrontier, HRPOpt
from data.database import store_optimized_portfolio, load_optimized_portfolio, load_all_optimized_portfolios

class OptimizedPortfolio:
    def __init__(self, name, clean_weights, expected_returns, volatility, sharpe_ratio):
        self.name = name
        self.clean_weights = clean_weights
        self.expected_returns = expected_returns
        self.volatility = volatility
        self.sharpe_ratio = sharpe_ratio

    def __iter__(self):
        yield self.name
        yield self.clean_weights
        yield self.expected_returns
        yield self.volatility
        yield self.sharpe_ratio

    def save(self):
        store_optimized_portfolio(self)

    @classmethod
    def from_portfolio(cls, portfolio):
        return cls(portfolio.name, portfolio.clean_weights, portfolio.expected_returns, portfolio.volatility, portfolio.sharpe_ratio)

    @classmethod
    def load(cls, name):
        optimized_portfolio = load_optimized_portfolio(name)
        if optimized_portfolio is not None:
            return cls(*optimized_portfolio)

class PortfolioOptimizer:
    def __init__(self, stock_data, risk_tolerance=None, news_sentiment_scores=None):
        self.stock_data = stock_data
        self.news_sentiment_scores = news_sentiment_scores
        self.risk_tolerance = risk_tolerance

    def optimize(self, model):
        match model.lower():
            case "mean-variance":
                return self.optimize_mean_variance()
            case "black-litterman":
                return self.optimize_black_litterman()
            case "hrp":
                return self.optimize_hrp()
            case "all":
                return [self.optimize_mean_variance(), self.optimize_black_litterman(), self.optimize_hrp()]
            case _:
                raise ValueError("Invalid optimization model")

    def load(self, model):
        model_name = model.lower()
        match model_name:
            case "mean-variance" | "black-litterman" | "hrp":
                return OptimizedPortfolio.load(model_name)
            case "all":
                return [OptimizedPortfolio.from_portfolio(portfolio) for portfolio in load_all_optimized_portfolios()]
            case _:
                raise ValueError("Invalid optimization model")

    def optimize_mean_variance(self) -> OptimizedPortfolio:
        mu = expected_returns.mean_historical_return(self.stock_data)
        cov_matrix = CovarianceShrinkage(self.stock_data).ledoit_wolf()
        ef = EfficientFrontier(mu, cov_matrix)
        ef.min_volatility()
        op = OptimizedPortfolio("mean-variance", ef.clean_weights(), *ef.portfolio_performance(verbose=True))
        return op

    def optimize_black_litterman(self) -> OptimizedPortfolio:
        cov_matrix = CovarianceShrinkage(self.stock_data).ledoit_wolf()
        market_prior = expected_returns.capm_return(self.stock_data)

        # TODO: Sentiment scores or user's views?
        viewdict = {}
        if self.news_sentiment_scores is not None:
            # Use sentiment scores to create absolute views
            for ticker in self.stock_data.columns:
                if ticker in self.news_sentiment_scores:
                    viewdict[ticker] = self.news_sentiment_scores[ticker] / 100.0
        else:
            # Example views on stocks (replace with your views)
            viewdict = {
                # "TSLA": 0.1,  # Stock 0 will return 10%
                # "F": -0.05  # Stock 3 will return -5%
            }

        # TODO: Alter delta to risk tolerance (see risk_tolerance.py)
        delta = 2  # Risk aversion parameter
        bl = BlackLittermanModel(cov_matrix, pi=market_prior, absolute_views=viewdict, delta=delta)

        posterior_returns = bl.bl_returns()
        posterior_cov_matrix = bl.bl_cov()

        # Calculate optimal weights using Efficient Frontier with the Black-Litterman expected returns and covariance matrix
        ef = EfficientFrontier(posterior_returns, posterior_cov_matrix)
        # TODO: Check if this is the correct way to calculate the target return
        ef.efficient_return(target_return=0.4)
        
        op = OptimizedPortfolio("black-litterman", ef.clean_weights(), *ef.portfolio_performance(verbose=True))
        return op

    # Hierarchical Risk Parity
    def optimize_hrp(self) -> OptimizedPortfolio:
        # Normalize the stock data
        returns = self.stock_data.pct_change().dropna()

        # Optimize portfolio using HRP
        hrp = HRPOpt(returns)
        hrp.optimize()

        #Calculate optimized weights and portfolio performance
        weights = hrp.clean_weights()
        mu, sigma, sharpe_ratio = hrp.portfolio_performance(verbose=True)

        # Create OptimizedPortfolio object
        op = OptimizedPortfolio("hrp", weights, mu, sigma, sharpe_ratio)
        return op