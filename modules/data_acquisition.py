import yfinance as yf
from sec_edgar_downloader import Downloader
import os
import glob
from bs4 import BeautifulSoup

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price_history = None
        self.sec_reports = None
        self.news = None

    def set_price_history(self, price_history):
        self.price_history = price_history

    def set_sec_reports(self, sec_reports):
        self.sec_reports = sec_reports

    def set_news(self, news):
        self.news = news

def read_edgar_file(ticker, report_type, file_name):
    # NOTE: the downloader puts the files in 10-K/some_naming_convention/report so I am using '*' to take care of that
    path = os.path.join(os.getcwd(),"sec-edgar-filings", ticker, report_type) 
    
    # Use glob to find the file
    dirs = [d for d in os.listdir(path)]# if os.path.isdir(os.path.join(path, d))]
    matching_files = []
    for dir in dirs:
        files = glob.glob(f'{path}/{dir}/{file_name}')
        if files:
           matching_files += files 

    # Check if any matching files were found
    if matching_files:
        file_path = matching_files[0]
        with open(file_path, 'r') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup.find_all('div')
        list_of_paragraphs = [paragraph.text for paragraph in paragraphs]
    else:
        list_of_paragraphs = None

    return list_of_paragraphs

def fetch_stock_data(stock: StockData, period="1y", interval="1d"):
    ticker_data = yf.Ticker(stock.ticker)
    price_history = ticker_data.history(period=period, interval=interval)
    stock.set_price_history(price_history)

def fetch_sec_reports(stock: StockData, amount=1):

    #TODO: for the timebeing only 10-K is collected
    report_type = "10-K"

    # Initialize a downloader
    dl = Downloader()

    # Download the 10-K reports
    dl.get(report_type, stock.ticker, amount=amount, download_details=True)
    #TODO: Add additional calls here to download other reports if needed

    # Parse the downloaded reports and extract the data you need. This might involve 
    parsed_reports = read_edgar_file(stock.ticker, report_type, "filing-details.html")

    stock.set_sec_reports(parsed_reports)

def fetch_news_data(stock: StockData):
    ticker_data = yf.Ticker(stock.ticker)
    news_data = ticker_data.get_news()
    stock.set_news(news_data)

if __name__ == "__main__":
    # Test fetch_stock_data
    test_stock = StockData("AAPL")
    try:
        fetch_stock_data(test_stock)
        assert test_stock.price_history is not None, "Failed to fetch stock data"
    except Exception as e:
        print(f"Test fetch_stock_data failed with exception: {e}")

    # Test fetch_sec_reports
    test_stock = StockData("AAPL")
    try:
        fetch_sec_reports(test_stock)
        assert test_stock.sec_reports is not None, "Failed to fetch SEC reports"
    except Exception as e:
        print(f"Test fetch_sec_reports failed with exception: {e}")

    # Test fetch_news_data
    test_stock = StockData("AAPL")
    try:
        fetch_news_data(test_stock)
        assert test_stock.news is not None, "Failed to fetch news data"
    except Exception as e:
        print(f"Test fetch_news_data failed with exception: {e}")
