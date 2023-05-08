import matplotlib.pyplot as plt

def plot_portfolios(portfolios):
    # Get portfolio returns, volatilities, and Sharpe ratios
    names = []
    portfolio_returns = []
    portfolio_volatilities = []
    sharpe_ratios = []

    for portfolio in portfolios:
        name = portfolio.name
        portfolio_return, portfolio_volatility, sharpe_ratio = portfolio.expected_returns, portfolio.volatility, portfolio.sharpe_ratio
        
        names.append(name)
        portfolio_returns.append(portfolio_return)
        portfolio_volatilities.append(portfolio_volatility)
        sharpe_ratios.append(sharpe_ratio)

    plt.figure(figsize=(12, 6))
    for i in range(len(portfolios)):
        plt.scatter(portfolio_volatilities[i], portfolio_returns[i], label=f'{names[i]} (Sharpe: {sharpe_ratios[i]:.2f})')

    plt.xlabel('Volatility (Standard Deviation)')
    plt.ylabel('Expected Return')
    plt.title('Portfolio Optimization Comparison')
    plt.legend()
    plt.grid()
    plt.show()