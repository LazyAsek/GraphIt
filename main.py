import yfinance as yf
import pandas as pd
import sqlite3
import utylity
import db_menager
import ticker_menager
import plotly
import plotly.graph_objects as go

#choose stock by ticker
ticker = "PKN.WA"
table= "stock_prices"

data = yf.Ticker(ticker)
db_menager.addStock(table,ticker)
db_menager.updateStock(table,ticker)
dataSet = db_menager.getData(table,ticker)
print(dataSet)
fig = go.Figure(
    data =[
        go.Candlestick(x=dataSet["date"],open=dataSet["open"],high=dataSet["high"],low=dataSet["low"],close=dataSet["close"],name=ticker)
    ]
)

fig.update_layout(
    title = f"Graph of {ticker}",
    yaxis_title="Price (PLN)",
    xaxis_title="Date",
    template="plotly_dark",  # Ciemny motyw (opcjonalnie: 'plotly_white')
    xaxis_rangeslider_visible=False,
)
fig.show()