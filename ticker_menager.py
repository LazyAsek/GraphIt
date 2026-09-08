import yahooquery

def findTicker(toFind):
    resoults = yahooquery.search(toFind)
    result = []
    if "quotes" in resoults:
        for item in resoults["quotes"]:
            ticker = item.get("symbol")
            name = item.get("longname") or item.get("shortname")
            stockExchange = item.get("exchDisp") 
            
            result.append([ticker,name,stockExchange])
    return result

def tickerReadFormated(ticker_list):
    result =[]
    for i in ticker_list:
        result.append(f"Ticker: {ticker_list[0]} | Name: {ticker_list[1]} | Stock Exchange: {ticker_list[2]}")
    return result