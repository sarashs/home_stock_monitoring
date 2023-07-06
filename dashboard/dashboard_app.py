import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from modules.database_handler import DatabaseHandler

app = dash.Dash(__name__)

db_handler = DatabaseHandler("stock_data.db")  # Initialize the database handler

app.layout = html.Div([
    dcc.Input(id='ticker-input', type='text', value='TSLA'),
    html.Button('Submit', id='submit-btn', n_clicks=0),
    dcc.Graph(id='price-graph'),
    dcc.Graph(id='sec-sentiment-graph'),
    dcc.Graph(id='news-sentiment-graph'),
])

@app.callback(
    [Output('price-graph', 'figure'),
     Output('sec-sentiment-graph', 'figure'),
     Output('news-sentiment-graph', 'figure')],
    [Input('submit-btn', 'n_clicks')],
    [dash.dependencies.State('ticker-input', 'value')]
)
def update_graph(n_clicks, ticker):
    stock_data = db_handler.get_stock_data(ticker)  # Fetch data from database
    sec_reports = db_handler.get_sec_data(ticker)  # Fetch data from database
    news_data = db_handler.get_news_data(ticker)  # Fetch data from database

    # Generate figures
    price_figure = create_stock_figure(stock_data)
    sec_sentiment_figure = create_sec_sentiment_figure(sec_reports)
    news_sentiment_figure = create_news_sentiment_figure(news_data)

    return price_figure, sec_sentiment_figure, news_sentiment_figure

def create_stock_figure(data):
    trace = go.Scatter(
        x=[d[1] for d in data],  # assuming that DATE is at index 1
        y=[d[2] for d in data],  # assuming that PRICE is at index 2
        mode='lines'
    )

    layout = go.Layout(
        title="Price History",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Price")
    )

    return go.Figure(data=[trace], layout=layout)

def create_sec_sentiment_figure(data):
    trace = go.Bar(
        x=[d[1] for d in data],  # assuming that DATE is at index 1
        y=[d[3] for d in data],  # assuming that SENTIMENT is at index 3
    )

    layout = go.Layout(
        title="SEC Report Sentiment",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Sentiment")
    )

    return go.Figure(data=[trace], layout=layout)

def create_news_sentiment_figure(data):
    trace = go.Bar(
        x=[d[1] for d in data],  # assuming that DATE is at index 1
        y=[d[3] for d in data],  # assuming that SENTIMENT is at index 3
    )

    layout = go.Layout(
        title="News Sentiment",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Sentiment")
    )

    return go.Figure(data=[trace], layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
