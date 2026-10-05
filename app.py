import datetime
import db_menager
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import ticker_menager
import utylity
import yfinance as yf

# Inicjalizacja zmiennych w session_state
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "Candlestick"

if "chosen_list" not in st.session_state:
    st.session_state.chosen_list = []

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
                if tickerChosen not in st.session_state.chosen_list:
                    st.session_state.chosen_list.append(tickerChosen)
        else:
            st.sidebar.error("No Data In Database, Fetch data First")


if st.session_state.chosen_list:
    
    st.sidebar.markdown("---")

    to_remove = None
    for idx, item in enumerate(st.session_state.chosen_list):
        col_info, col_del = st.sidebar.columns([4, 1])

        with col_info:
            st.success(f"Current : {item}")

        with col_del:
            # Unikalny key dla kazdego przycisku w petli
            if st.button("❌", help=f"Delete {item}", key=f"del_{item}_{idx}"):
                to_remove = item

    if to_remove:
        st.session_state.chosen_list.remove(to_remove)
        if not st.session_state.chosen_list:
            st.session_state.should_display = False
        st.rerun()


if st.session_state.get("should_display", False) and tickerChosen:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Chart Type")
    c1, c2 = st.sidebar.columns(2)

    with c1:
        if st.button("🕯️ Candle", use_container_width=True):
            st.session_state.chart_type = "Candlestick"
    with c2:
        if st.button("📈 Line", use_container_width=True):
            st.session_state.chart_type = "Line"


    fig = go.Figure()

    for ticker in st.session_state.chosen_list:
        db_menager.updateStock(table, ticker)
        dataSet = db_menager.getData(table, ticker, start_date, end_date)

        if not dataSet.empty:
            if st.session_state.chart_type == "Candlestick":
                fig.add_trace(
                    go.Candlestick(
                        x=dataSet["date"],
                        open=dataSet["open"],
                        high=dataSet["high"],
                        low=dataSet["low"],
                        close=dataSet["close"],
                        name=ticker,
                    )
                )
            else:

                first = dataSet["close"].iloc[0]
                dataSet["pct_change"] = ((
                    (dataSet["close"] - first) / first
                ) * 100).round(2)

                fig.add_trace(
                    go.Scatter(
                        x=dataSet["date"],
                        y=dataSet["pct_change"],
                        mode="lines",
                        name=f"{ticker} Close",
                        customdata=dataSet["pct_change"],
                        hovertemplate=(
                            f"<b>{ticker}</b><br>"
                            " %{customdata:+.2f}% <extra></extra>"
                        ),
                    )
                )

    title_tickers = ", ".join(st.session_state.chosen_list)
    fig.update_layout(
        title=f"Graph of {title_tickers} ({st.session_state.chart_type})",
        yaxis_title="Price",
        xaxis_title="Date",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        hovermode="x unified",  
    )

    st.plotly_chart(fig, width='stretch')