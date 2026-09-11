import sqlite3

def clearTable(table):
    with sqlite3.connect("StockMarket.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table}")
        conn.commit()

def clearTableByTicker(table,ticker):
    with sqlite3.connect("StockMarket.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE ticker='{ticker}' ")
            conn.commit()
def newestRecord(table,ticker):
     with sqlite3.connect("StockMarket.db") as conn:
                 cursor = conn.cursor()
                 cursor.execute(f"SELECT * FROM {table} WHERE ticker='{ticker}' ORDER BY date DESC LIMIT 1")
                 new = cursor.fetchall()
                 conn.commit()
                 return new[0] if new else 0
def oldestRecord(table,ticker):
     with sqlite3.connect("StockMarket.db") as conn:
                 cursor = conn.cursor()
                 cursor.execute(f"SELECT * FROM {table} WHERE ticker='{ticker}' ORDER BY date ASC LIMIT 1")
                 old = cursor.fetchall()
                 conn.commit()
                 return old[0]  if old else 0
def clearNewestRecords(table,ticker,count):
         with sqlite3.connect("StockMarket.db") as conn:
                   cursor = conn.cursor()
                   cursor.execute(f"DELETE FROM {table} WHERE rowid IN (SELECT rowid FROM {table} WHERE ticker = '{ticker}' ORDER BY date DESC LIMIT {count})")
                   conn.commit()
def getTimeStamp(t):
    TIME= {1 : "1d", 5 :"5d", 30 :"1mo", 90 :"3mo", 180 :"6mo", 365 :"1y", 730 :"2y", 1825 :"5y", 3650 :"10y", 0 :"max"}
    update = 1
    for k in TIME.keys():
        update = k
        if t < k:
            break
    return TIME[update]