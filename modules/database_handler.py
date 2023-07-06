import sqlite3
from sqlite3 import Error

class DatabaseHandler:
    def __init__(self, db_file):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_table(self):
        """ create table for stock data, SEC filings and news """
        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS STOCK
                        (TICKER           TEXT     NOT NULL,
                         DATE             DATE     NOT NULL,
                         PRICE            REAL     NOT NULL,
                         VOLUME           REAL     NOT NULL,
                         PRIMARY KEY (TICKER, DATE));''')

            self.conn.execute('''CREATE TABLE IF NOT EXISTS SEC
                        (TICKER           TEXT     NOT NULL,
                         DATE             DATE     NOT NULL,
                         REPORT           TEXT     NOT NULL,
                         SENTIMENT        REAL,
                         PRIMARY KEY (TICKER, DATE));''')

            self.conn.execute('''CREATE TABLE IF NOT EXISTS NEWS
                        (TICKER           TEXT     NOT NULL,
                         DATE             DATE     NOT NULL,
                         NEWS             TEXT     NOT NULL,
                         SENTIMENT        REAL,
                         PRIMARY KEY (TICKER, DATE));''')
            print("Tables created successfully")
        except Error as e:
            print(e)

    def insert_stock_data(self, data):
        """ Insert stock data into STOCK table """
        # Assuming data is a dictionary with 'TICKER', 'DATE', 'PRICE' and 'VOLUME'
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO STOCK(TICKER, DATE, PRICE, VOLUME) VALUES(?,?,?,?)''', 
                       (data['TICKER'], data['DATE'], data['PRICE'], data['VOLUME']))
        self.conn.commit()

    def insert_sec_data(self, data):
        """ Insert SEC data into SEC table """
        # Assuming data is a dictionary with 'TICKER', 'DATE', 'REPORT' and 'SENTIMENT'
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO SEC(TICKER, DATE, REPORT, SENTIMENT) VALUES(?,?,?,?)''', 
                       (data['TICKER'], data['DATE'], data['REPORT'], data['SENTIMENT']))
        self.conn.commit()

    def insert_news_data(self, data):
        """ Insert news data into NEWS table """
        # Assuming data is a dictionary with 'TICKER', 'DATE', 'NEWS' and 'SENTIMENT'
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO NEWS(TICKER, DATE, NEWS, SENTIMENT) VALUES(?,?,?,?)''', 
                       (data['TICKER'], data['DATE'], data['NEWS'], data['SENTIMENT']))
        self.conn.commit()

    def get_stock_data(self, ticker):
        """ Fetch stock data for a given ticker """
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM STOCK WHERE TICKER=?''', (ticker,))
        return cursor.fetchall()

    def get_sec_data(self, ticker):
        """ Fetch SEC data for a given ticker """
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM SEC WHERE TICKER=?''', (ticker,))
        return cursor.fetchall()
