import yfinance as yf
import pandas as pd
import db_menager
import plotly.graph_objects as go
import streamlit as st
import ticker_menager
import datetime
import utylity

#choose stock by ticker
table= "stock_prices"
tickerChosen = None
st.set_page_config(page_title="GraphIt",layout="wide")

#SIDEBAR
add_sidebar = st.sidebar
add_sidebar_title = st.sidebar.header("Find Ticker")

sidebar_textinput = st.sidebar.text_input(
    label="Type Ticker:",
    help="Type your ticker like : XTB.WA, PKN.WA, AAPL",
    placeholder="search")

#Ticker list
match_Ticker = ticker_menager.findTicker(sidebar_textinput)

if match_Ticker:
    chosen = st.sidebar.selectbox(
        label="Found",
        options=match_Ticker,
        index=0
    )
    tickerChosen = chosen [0]
   
else:
    raw = sidebar_textinput.strip().upper()
    if raw:
        st.sidebar.info(f"No Resoults for {raw}")

st.sidebar.markdown("---")

if tickerChosen:
    st.sidebar.success(f"Current Ticker: {tickerChosen}")
    if utylity.newestRecord(table,tickerChosen) != 0:
        st.sidebar.info(f"Oldest record fetched: { datetime.date.strptime(utylity.oldestRecord(table,tickerChosen)[1],"%Y-%m-%d")}")
    st.sidebar.subheader("📅 Date Range")

 
    default_start = datetime.date.today() - datetime.timedelta(days=365)
    default_end = datetime.date.today()

    start_date = st.sidebar.date_input("Start date", value=default_start)
    end_date = st.sidebar.date_input("End date", value=default_end)

    col1,col2 = st.sidebar.columns(2)
    show_chart = None

    with col1:
        if st.button("Add to DataBase"):
            if start_date<= end_date:
                with st.spinner("Fetching Data ..."):
                    db_menager.addStock(table,tickerChosen,(end_date-start_date).days)
    with col2 :
        if utylity.newestRecord(table,tickerChosen) != 0:
            show_chart = st.button("Display")
        else:
            st.sidebar.error("No Data In Database, Fetch data First")

    if show_chart:
        data = yf.Ticker(tickerChosen)
        db_menager.updateStock(table,tickerChosen)
        print(start_date)
        dataSet = db_menager.getData(table,tickerChosen,start_date,end_date)


        fig = go.Figure(
            data =[
                go.Candlestick(x=dataSet["date"],open=dataSet["open"],high=dataSet["high"],low=dataSet["low"],close=dataSet["close"],name=tickerChosen)
            ]
        )

        fig.update_layout(
            title = f"Graph of {tickerChosen}",
            yaxis_title="Price ",
            xaxis_title="Date",
            template="plotly_dark",  # Ciemny motyw (opcjonalnie: 'plotly_white')
            xaxis_rangeslider_visible=False,
        )

        st.plotly_chart(fig,use_container_width=True)