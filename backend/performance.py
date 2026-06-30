import yfinance as yf
import numpy as np
import streamlit as st

@st.cache_data
def get_stock_performance(ticker: str, period: str):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)

    if df.empty:
        return None, None

    df["Daily Return"] = df["Close"].pct_change()

    metrics = {
        "start_price": float(df["Close"].iloc[0]),
        "end_price": float(df["Close"].iloc[-1]),
        "total_return": (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100,
        "volatility": df["Daily Return"].std() * np.sqrt(252) * 100
    }

    return df, metrics
