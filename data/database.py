import config
import pyodbc
import pickle
import json
import pandas as pd

# Connection and configuration details
DATABASE_CONFIG = config.DATABASE_CONFIG

def connect_to_database():
    connection_string = ';'.join([f'{k}={v}' for k, v in DATABASE_CONFIG.items()])
    connection = pyodbc.connect(connection_string)
    return connection

# Tickers
def store_tickers(tickers):
    connection = connect_to_database()
    # Loop through tickers and insert data into SQL Server
    for ticker in tickers:
        # Serialize the ticker object
        pickled_ticker = pickle.dumps(ticker)
        # Insert the serialized ticker into the database
        connection.execute("INSERT INTO Tickers (TickerData) VALUES (?)", (pickled_ticker))
    # Commit the changes and close the connection
    connection.commit()
    connection.close()

def load_tickers():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT TickerData FROM Tickers")
    rows = cursor.fetchall()
    # Deserialize each ticker object and append to a list
    tickers = []
    for row in rows:
        pickled_ticker = row[0]
        ticker = pickle.loads(pickled_ticker)
        tickers.append(ticker)
    # Close the cursor and connection
    cursor.close()
    return tickers

# Articles
def store_articles(articles):
    connection = connect_to_database()
    cursor = connection.cursor()
    for row in articles.itertuples(index=False):
        result = cursor.execute("SELECT ID FROM Tickers WHERE Symbol = ?", row.ticker).fetchone()
        if result is not None:
            ticker_id = result[0]
        else:
            ticker_id = None # Or whatever default value we want to use
        cursor.execute("INSERT INTO Articles (TickerID, Title, Description, Sentiment) VALUES (?, ?, ?, ?)",
                       ticker_id, row.title, row.description, row.sentiment)
    connection.commit()
    connection.close()

def load_articles():
    connection = connect_to_database()
    cursor = connection.cursor()
    articles_data = cursor.execute("SELECT t.Symbol, a.Title, a.Description, a.Sentiment FROM Articles a JOIN Tickers t ON a.TickerID = t.ID").fetchall()
    connection.close()
    
    articles = pd.DataFrame(articles_data, columns=["ticker", "title", "description", "sentiment"])
    return articles

# Optimized portfolios
def store_optimized_portfolio(portfolio):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    name = portfolio.name
    serialized_weights = json.dumps(portfolio.weights)

    mu, sigma, sharpe = portfolio.portfolio_performance()
    query = """
        INSERT INTO OptimizedPortfolios (Name, CleanWeights, ExpectedReturns, Volatility, SharpeRatio)
        VALUES (?, ?, ?, ?, ?)
    """
    params = (name, serialized_weights, mu, sigma, sharpe)
    cursor.execute(query, params)
    connection.commit()
    connection.close()

def load_optimized_portfolio(name):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT Name, CleanWeights, ExpectedReturns, Volatility, SharpeRatio FROM OptimizedPortfolios"
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        return None

    weights = json.loads(result[1])
    expected_returns = result[2]
    volatility = result[3]
    sharpe_ratio = result[4]

    return name, weights, expected_returns, volatility, sharpe_ratio

def load_all_optimized_portfolios():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM OptimizedPortfolios"
    cursor.execute(query)
    results = cursor.fetchall()

    portfolios = []
    for row in results:
        name = row[1]
        serialized_weights = row[2]
        weights = json.loads(serialized_weights)
        expected_returns = row[3]
        volatility = row[4]
        sharpe_ratio = row[5]
        portfolio = name, weights, expected_returns, volatility, sharpe_ratio
        portfolios.append(portfolio)

    return portfolios