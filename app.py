import datetime
import db_menager
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import ticker_menager
import utylity
import yfinance as yf

if "chart_type" not in st.session_state:
    st.session_state.chart_type = "Candlestick"

# choose stock by ticker
table = "stock_prices"
tickerChosen = None
st.set_page_config(page_title="GraphIt", layout="wide")

# SIDEBAR
add_sidebar = st.sidebar
add_sidebar_title = st.sidebar.header("Find Ticker")

sidebar_textinput = st.sidebar.text_input(
    label="Type Ticker:",
    help="Type your ticker like : XTB.WA, PKN.WA, AAPL",
    placeholder="search",
)

# Ticker list
match_Ticker = ticker_menager.findTicker(sidebar_textinput)

if match_Ticker:
    chosen = st.sidebar.selectbox(
        label="Found", options=match_Ticker, index=0
    )
    tickerChosen = chosen[0]
else:
    raw = sidebar_textinput.strip().upper()
    if raw:
        st.sidebar.info(f"No Resoults for {raw}")

st.sidebar.markdown("---")

if tickerChosen:
    st.sidebar.success(f"Current Ticker: {tickerChosen}")
    if utylity.newestRecord(table, tickerChosen) != 0:
        st.sidebar.info(
            f"Oldest record fetched: {datetime.date.strptime(utylity.oldestRecord(table, tickerChosen)[1], '%Y-%m-%d')}"
        )
    st.sidebar.subheader("📅 Date Range")

    default_start = datetime.date.today() - datetime.timedelta(days=365)
    default_end = datetime.date.today()

    start_date = st.sidebar.date_input("Start date", value=default_start)
    end_date = st.sidebar.date_input("End date", value=default_end)

    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("Add to DataBase"):
            if start_date <= end_date:
                with st.spinner("Fetching Data ..."):
                    db_menager.addStock(
                        table, tickerChosen, (end_date - start_date).days
                    )
    with col2:
        if utylity.newestRecord(table, tickerChosen) != 0:
            if st.button("Display"):
                st.session_state.should_display = True
        else:
            st.sidebar.error("No Data In Database, Fetch data First")

    # Wyświetlanie opcji typu wykresu oraz samego wykresu
    if st.session_state.get("should_display", False):
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Chart Type")
        c1, c2 = st.sidebar.columns(2)

        with c1:
            if st.button("🕯️ Candle", use_container_width=True):
                st.session_state.chart_type = "Candlestick"
        with c2:
            if st.button("📈 Line", use_container_width=True):
                st.session_state.chart_type = "Line"

        # Pobranie danych
        data = yf.Ticker(tickerChosen)
        db_menager.updateStock(table, tickerChosen)
        dataSet = db_menager.getData(
            table, tickerChosen, start_date, end_date
        )


        fig = go.Figure()

        if st.session_state.chart_type == "Candlestick":
            fig.add_trace(
                go.Candlestick(
                    x=dataSet["date"],
                    open=dataSet["open"],
                    high=dataSet["high"],
                    low=dataSet["low"],
                    close=dataSet["close"],
                    name=tickerChosen,
                )
            )
        else:
            if not dataSet.empty:
                first = dataSet["close"].iloc[0]
                dataSet["pct_change"] = ((dataSet["close"]-first)/first)*100
            fig.add_trace(
                go.Scatter(
                    x=dataSet["date"],
                    y=dataSet["close"],
                    mode="lines",
                    name=f"{tickerChosen} Close",
                    line=dict(color="#00B4D8", width=2),
                    customdata=dataSet["pct_change"],
                    hovertemplate=("%{customdata:+.2f}%""<extra></extra>")
                )
            )

        fig.update_layout(
            title=f"Graph of {tickerChosen} ({st.session_state.chart_type})",
            yaxis_title="Price",
            xaxis_title="Date",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
        )

        st.plotly_chart(fig, use_container_width=True)