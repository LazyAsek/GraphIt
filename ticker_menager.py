import yahooquery

def findTicker(toFind):
    resoults = yahooquery.search(toFind)
    if "quotes" in resoults:
        for item in resoults["quotes"]:
            ticker = item.get("symbol")
            name = item.get("longname") or item.get("shortname")
            stockExchange = item.get("exchDisp") 
            
            print(f"Ticker: {ticker} | Name: {name} | Stock Exchange: {stockExchange}")
   