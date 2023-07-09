import unittest
from modules.data_acquisition import StockData, fetch_stock_data
from modules.database_handler import DatabaseHandler
from modules.sentiment_analysis import SentimentAnalysis
from datetime import datetime
import os

import warnings

# Filter out DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestStockData(unittest.TestCase):
    def setUp(self):
        self.stock_data = StockData('AAPL')

    def test_fetch_stock_data(self):
        fetch_stock_data(self.stock_data, '2y', '1d')
        self.assertIsNotNone(self.stock_data.price_history)
        # Add more assertions here based on what you expect the output to be...

class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.db_handler = DatabaseHandler("test_db.db")
        self.db_handler.create_table()

        # create some test data
        self.test_stock_data = {'TICKER': 'TSLA', 'DATE': datetime.now().date(), 'PRICE': 100.0, 'VOLUME': 1000.0}
        self.test_sec_data = {'TICKER': 'TSLA', 'DATE': datetime.now().date(), 'REPORT': 'Test report', 'SENTIMENT': 0.8}
        self.test_news_data = {'TICKER': 'TSLA', 'DATE': datetime.now().date(), 'NEWS': 'Test news', 'SENTIMENT': 0.7}

    def test_insert_and_retrieve_stock_data(self):
        # Insert stock data
        self.db_handler.insert_stock_data(self.test_stock_data)
        # Retrieve stock data
        result = self.db_handler.get_stock_data('TSLA')
        # The retrieved data should match the inserted data
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], self.test_stock_data['TICKER'])
        self.assertEqual(result[0][2], self.test_stock_data['PRICE'])
        self.assertEqual(result[0][3], self.test_stock_data['VOLUME'])

    def test_insert_and_retrieve_sec_data(self):
        # Insert SEC data
        self.db_handler.insert_sec_data(self.test_sec_data)
        # Retrieve SEC data
        result = self.db_handler.get_sec_data('TSLA')
        # The retrieved data should match the inserted data
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], self.test_sec_data['TICKER'])
        self.assertEqual(result[0][2], self.test_sec_data['REPORT'])
        self.assertEqual(result[0][3], self.test_sec_data['SENTIMENT'])

    def test_insert_and_retrieve_news_data(self):
        # Insert news data
        self.db_handler.insert_news_data(self.test_news_data)
        # Retrieve news data
        result = self.db_handler.get_news_data('TSLA')
        # The retrieved data should match the inserted data
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], self.test_news_data['TICKER'])
        self.assertEqual(result[0][2], self.test_news_data['NEWS'])
        self.assertEqual(result[0][3], self.test_news_data['SENTIMENT'])

    def tearDown(self):
        os.remove("test_db.db")

class TestSentimentAnalysis(unittest.TestCase):
    def setUp(self):
        self.sentiment_analysis = SentimentAnalysis()

    def test_analyze_news(self):
        test_news = "Apple has a great day with a record high stocks."
        result = self.sentiment_analysis.analyze_news(test_news, "AAPL")
        self.assertEqual(result, 'positive')

# Run all tests
if __name__ == '__main__':
    # Delete existing test database file if exists
    if os.path.exists("test_db.db"):
        os.remove("test_db.db")
    unittest.main()