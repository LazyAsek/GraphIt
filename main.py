import yfinance as yf
import pandas as pd
import sqlite3
import utylity
import db_menager


TIME= {1 : "1d", 5 :"5d", 30 :"1mo", 90 :"3mo", 180 :"6mo", 365 :"1y", 730 :"2y", 1825 :"5y", 3650 :"10y", 0 :"max"}
curTime = 5
#choose stock by ticker
ticker = "XTB.WA"
table= "stock_prices"
data = yf.Ticker(ticker)
db_menager.addStock(table,ticker)

