import sqlite3


with sqlite3.connect("StockMarket.db") as conn:
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS stock_prices (
        ticker TEXT NOT NULL,
        date TEXT NOT NULL,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        dividents DOUBLE,
        PRIMARY KEY (ticker, date)
    );
    """

    cursor.execute(create_table_query)
    conn.commit()

print("database created")