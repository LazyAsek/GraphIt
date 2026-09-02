import yfinance as yf
import pandas as pd
import sqlite3
import utylity
import datetime

TIME= {1 : "1d", 5 :"5d", 30 :"1mo", 90 :"3mo", 180 :"6mo", 365 :"1y", 730 :"2y", 1825 :"5y", 3650 :"10y", 0 :"max"}
curTime = 30

def addStock(table,ticker,time=30):

    data = yf.Ticker(ticker)
    #get history / base 10 days
    records = data.history(period=f'{TIME[time]}')

    #format to sql table
    """
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            dividents DOUBLE,
            PRIMARY KEY (ticker, date)
    """
    #prepare for reading
    dictRecords = records.to_dict(orient='index', into=dict)

    #connect to database
    with sqlite3.connect("StockMarket.db") as conn:
            cursor = conn.cursor()
            for k,v in dictRecords.items():
                    date = k.date()
                    values = f"'{ticker}','{date}',{v['Open']},{v['High']},{v['Low']},{v['Close']},{v['Volume']},{v['Dividends']}"
                    cursor.execute(f"INSERT INTO {table} VALUES({values})")
                    
            conn.commit()

    # record  {Timestamp('2026-08-26 00:00:00+0200', tz='Europe/Warsaw'): {'Open': 151.83999633789062, 'High': 152.0, 'Low': 148.10000610351562, 'Close': 149.0, 'Volume': 1537400, 'Dividends': 0.0, 'Stock Splits': 0.0}
def updateStock(table,ticker):
        data = yf.Ticker(ticker)
        #get history / base 10 days
        current =  datetime.date.strptime(utylity.newestRecord(table,ticker)[1],"%Y-%m-%d")
        sinceUpdate = (datetime.date.today() - current).days
        if sinceUpdate == 0:
            print("Stock is uptodate")
        update=1
        for k in TIME.keys():
                update = k
                if sinceUpdate < k:
                    break
        newestDate = datetime.date.strptime(utylity.newestRecord(table,ticker)[1],"%Y-%m-%d")
        data = yf.Ticker(ticker)
        records = data.history(period=f'{TIME[update]}')
        dictRecords = records.to_dict(orient='index', into=dict)
        with sqlite3.connect("StockMarket.db") as conn:
            cursor = conn.cursor()
                   
            for k,v in dictRecords.items():
                date = k.date()
                if date > newestDate:               
                        values = f"'{ticker}','{date}',{v['Open']},{v['High']},{v['Low']},{v['Close']},{v['Volume']},{v['Dividends']}"
                        cursor.execute(f"INSERT INTO {table} VALUES({values})")
                            
            conn.commit()

def getData(table,ticker):
    with sqlite3.connect("StockMarket.db") as conn:
        cursor = conn.cursor()
        query =f"""
            SELECT date, open, high, low, close, volume 
            FROM stock_prices 
            WHERE ticker = '{ticker}' 
            ORDER BY date ASC
        """
        data = pd.read_sql(query,conn)
        data["date"] = pd.to_datetime(data["date"])
    return data