import config
import pyodbc
import pickle
import pandas as pd

# Connection and configuration details
DATABASE_CONFIG = config.DATABASE_CONFIG

def connect_to_database():
    connection_string = ';'.join([f'{k}={v}' for k, v in DATABASE_CONFIG.items()])
    connection = pyodbc.connect(connection_string)
    return connection

def store_tickers(tickers):
    connection = connect_to_database()
    # Loop through tickers and insert data into SQL Server
    for ticker in tickers:
        # Serialize the ticker object
        pickled_ticker = pickle.dumps(ticker)
        # Insert the serialized ticker into the database
        connection.execute("INSERT INTO Tickers (Symbol, TickerData) VALUES (?, ?)", (ticker.ticker, pickled_ticker))
    # Commit the changes and close the connection
    connection.commit()
    connection.close()

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

def store_optimized_portfolio(portfolio_type, portfolio_object):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    serialized_object = pickle.dumps(portfolio_object)
    
    cursor.execute("INSERT INTO OptimizedPortfolios (PortfolioType, PortfolioObject) VALUES (?, ?)", (portfolio_type, serialized_object))
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

def load_articles():
    connection = connect_to_database()
    cursor = connection.cursor()
    articles_data = cursor.execute("SELECT t.Symbol, a.Title, a.Description, a.Sentiment FROM Articles a JOIN Tickers t ON a.TickerID = t.ID").fetchall()
    connection.close()
    
    articles = pd.DataFrame(articles_data, columns=["ticker", "title", "description", "sentiment"])
    return articles

def load_optimized_portfolio(portfolio_type):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    result = cursor.execute("SELECT PortfolioObject FROM OptimizedPortfolios WHERE PortfolioType = ?", (portfolio_type)).fetchone()
    if result is not None:
        serialized_object = result[0]
    else:
        serialized_object = None
    connection.close()
    
    if serialized_object is None:
        portfolio_object = None  # Or whatever default object we want to use
    else:
        portfolio_object = pickle.loads(serialized_object)
    return portfolio_object