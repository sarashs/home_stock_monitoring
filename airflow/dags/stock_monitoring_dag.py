from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from modules.data_acquisition import StockData
from modules.sentiment_analysis import SentimentAnalyzer
from modules.database_handler import DatabaseHandler

def acquire_data(ticker):
    stock_data = StockData(ticker)
    stock_data.get_historical_data()
    stock_data.get_sec_filings()
    stock_data.get_news()

def analyze_sentiment(ticker):
    sentiment_analyzer = SentimentAnalyzer()
    sentiment_analyzer.analyze_stock_data(ticker)

def store_data(ticker):
    db_handler = DatabaseHandler("stock_data.db")
    db_handler.insert_stock_data(ticker)
    db_handler.insert_sec_data(ticker)
    db_handler.insert_news_data(ticker)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('stock_monitor', default_args=default_args, schedule_interval=timedelta(days=1))

tickers = ['TSLA', 'AAPL', 'GOOGL']  # Add or remove tickers as needed

for ticker in tickers:
    t1 = PythonOperator(
        task_id=f'acquire_data_{ticker}',
        python_callable=acquire_data,
        op_kwargs={'ticker': ticker},
        dag=dag)

    t2 = PythonOperator(
        task_id=f'analyze_sentiment_{ticker}',
        python_callable=analyze_sentiment,
        op_kwargs={'ticker': ticker},
        dag=dag)

    t3 = PythonOperator(
        task_id=f'store_data_{ticker}',
        python_callable=store_data,
        op_kwargs={'ticker': ticker},
        dag=dag)

    t1 >> t2 >> t3