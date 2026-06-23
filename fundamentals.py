import yfinance as yf
import streamlit as st
@st.cache_data
def get_fundamentals(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info

    fundamentals = {
        "Market Cap": info.get("marketCap"),
        "Total Revenue": info.get("totalRevenue"),
        "Net Income": info.get("netIncomeToCommon"),
        "PE Ratio": info.get("trailingPE"),
        "Debt to Equity": info.get("debtToEquity"),
        "ROE": info.get("returnOnEquity"),
        "Free Cash Flow": info.get("freeCashflow"),
    }

    return fundamentals
