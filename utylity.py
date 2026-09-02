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
                 return new[0]
def oldestRecord(table,ticker):
     with sqlite3.connect("StockMarket.db") as conn:
                 cursor = conn.cursor()
                 cursor.execute(f"SELECT * FROM {table} WHERE ticker='{ticker}' ORDER BY date ASC LIMIT 1")
                 old = cursor.fetchall()
                 conn.commit()
                 return old[0]