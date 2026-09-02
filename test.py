import utylity


ticker = "XTB.WA"
table= "stock_prices"

new = utylity.newestRecord(table,ticker)
print(new)