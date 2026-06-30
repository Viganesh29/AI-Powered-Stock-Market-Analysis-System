import streamlit as st
from backend.currency import convert_currency, format_currency
from backend.performance import get_stock_performance
from backend.fundamentals import get_fundamentals
from backend.ai_analysis import get_ai_explanation
from backend.comparison import compare_assets
from backend.trading_signal import generate_trading_signal
from backend.database import (
    save_search_history,
    save_ai_report,
    save_asset_comparison,
    save_prediction,
    get_most_searched,
    get_most_compared,
    get_ai_reports,
    get_predictions
)
from backend.prediction import predict_hybrid
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from ai_agent import ask_ai_about_stock

st.set_page_config(
    page_title="VIAN FINSERVE Dashboard",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("VIAN FINSERVE Dashboard")

page = st.sidebar.selectbox(
    "Navigation",
    ["Market Dashboard", "Database Analytics"]
)

if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ---------------- STOCK SEARCH FUNCTION ----------------

@st.cache_data(ttl=300)
def search_yahoo_stocks(query):
    if not query:
        return []

    url = "https://query1.finance.yahoo.com/v1/finance/search"

    params = {
        "q": query,
        "quotesCount": 8,
        "newsCount": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=5
        )

        if response.status_code != 200:
            return []

        data = response.json()

        results = []

        for item in data.get("quotes", []):

            symbol = item.get("symbol")
            name = item.get("shortname") or item.get("longname")

            if symbol and name:
                results.append(f"{symbol} - {name}")

        return results

    except Exception:
        return []


# ---------------- DATABASE ANALYTICS PAGE ----------------

if page == "Database Analytics":

    st.title("🗄 Database Analytics")

    st.markdown("### 📊 Most Searched Assets")

    searched = get_most_searched()

    if searched:

        df_search = pd.DataFrame(searched, columns=["Asset", "Search Count"])

        st.dataframe(df_search, use_container_width=True)

        st.bar_chart(df_search.set_index("Asset"))

    else:

        st.info("No search data yet.")


    st.markdown("### ⚖️ Most Compared Assets")

    compared = get_most_compared()

    if compared:

        df_compare = pd.DataFrame(
            compared,
            columns=["Asset 1", "Asset 2", "Count"]
        )

        st.dataframe(df_compare, use_container_width=True)

    else:

        st.info("No comparisons yet.")


    st.markdown("### 🧠 AI Report History")

    reports = get_ai_reports()

    if reports:

        df_reports = pd.DataFrame(
            reports,
            columns=["Ticker", "Generated At"]
        )

        st.dataframe(df_reports, use_container_width=True)

    else:

        st.info("No AI reports yet.")

    st.markdown("### 🔮 Prediction History")

    predictions = get_predictions()

    if predictions:

        df_predictions = pd.DataFrame(
        predictions,
        columns=[
            "Ticker",
            "Period",
            "Predicted Price",
            "Expected Return %",
            "Signal",
            "Risk",
            "Confidence"
        ]
    )

        st.dataframe(df_predictions, use_container_width=True)

    else:
        st.info("No predictions saved yet.")


# ---------------- MARKET DASHBOARD ----------------

st.markdown("## 📊 VIAN FINSERVE Dashboard")

st.sidebar.markdown("### 🔎 Search Asset")

asset_type = st.sidebar.selectbox(
    "Select Asset Type",
    [
        "Stocks",
    ]
)

ticker = None

# ---------- STOCK SEARCH ----------

if asset_type == "Stocks":

    search_query = st.sidebar.text_input("Type company name or ticker")

    if search_query and len(search_query) >= 2:

        results = search_yahoo_stocks(search_query)

        if results:

            selected = st.sidebar.selectbox(
                "Select Stock",
                results
            )

            ticker = selected.split(" - ")[0]





period = st.sidebar.selectbox(
    "Time Period",
    ["1mo", "6mo", "1y", "3y", "5y"]
)

st.sidebar.markdown("### 📊 Chart Type")

chart_type = st.sidebar.selectbox(
    "Select Chart",
    [
        "Line Chart",
        "Candlestick",
        "Moving Average",
        "RSI Indicator"
    ]
)

st.sidebar.markdown("### 💱 Currency")

currency = st.sidebar.selectbox(
    "Select Currency",
    ["USD", "INR", "EUR", "GBP"],
    index=0
)


if not ticker:

    st.warning("Please enter a assets ticker.")

    st.stop()


# FIX 1: SAVE SEARCH HISTORY (moved outside stop block)

save_search_history(ticker, asset_type, period)


# ---------------- PERFORMANCE ----------------

with st.spinner("Fetching price data..."):

    df, metrics = get_stock_performance(ticker, period)


if df is None:

    st.error("No data found for this ticker.")

else:

    fig = go.Figure()

    df["Converted_Close"] = df["Close"].apply(
    lambda x: convert_currency(x, "USD", currency)
)

    fig = go.Figure()

# LINE CHART
if chart_type == "Line Chart":

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price"
    ))


# CANDLESTICK
elif chart_type == "Candlestick":

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick"
    ))


# MOVING AVERAGE
elif chart_type == "Moving Average":

    df["MA20"] = df["Close"].rolling(window=20).mean()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        name="Close Price",
        line=dict(color="blue", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["MA20"],
        name="MA 20",
        line=dict(color="orange", width=3)
    ))


# RSI
elif chart_type == "RSI Indicator":

    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["RSI"],
        name="RSI"
    ))

    fig.update_layout(
    title=f"{ticker} Price Chart",
    xaxis_title="Date",
    yaxis_title="Price"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "scrollZoom": True,
        "displayModeBar": True
    }
)


# ---------------- AI PREDICTION ----------------

st.markdown("### 🔮 AI Price Prediction")

# Initialize session state
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

prediction_options = {
    "1 Week": 7,
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365
}

selected_period = st.selectbox(
    "Prediction Period",
    list(prediction_options.keys())
)

prediction_days = prediction_options[selected_period]

# Run prediction
if st.button("Run AI Prediction"):

    with st.spinner("Running prediction model..."):

        future_prices = predict_hybrid(ticker, prediction_days)

    if future_prices is not None:

        current_price = convert_currency(
            metrics["end_price"],
            "USD",
            currency
        )

        signal_data = generate_trading_signal(
            current_price,
            future_prices
        )

        # Save prediction to session state
        st.session_state.prediction_result = signal_data

        # Save to database
        save_prediction(
            ticker,
            selected_period,
            signal_data["predicted_price"],
            signal_data["expected_return"],
            signal_data["volatility"],
            signal_data["signal"],
            signal_data["risk"],
            signal_data["confidence"]
        )

# Display prediction (persists after rerun)
if st.session_state.prediction_result:

    signal_data = st.session_state.prediction_result

    symbol_map = {
        "USD": "$",
        "INR": "₹",
        "EUR": "€",
        "GBP": "£"
    }

    symbol = symbol_map[currency]

    converted_price = convert_currency(
        signal_data["predicted_price"],
        "USD",
        currency
    )

    st.success(f"Predicted Price: {symbol}{converted_price:.2f}")
    st.metric("Expected Return", f"{signal_data['expected_return']:.2f}%")
    st.metric("Trading Signal", signal_data["signal"])
    st.metric("Risk Level", signal_data["risk"])
    st.metric("Confidence", signal_data["confidence"])

# ---------------- FUNDAMENTALS ----------------
def format_currency(value, currency):

    if value is None:
        return "N/A"

    symbol_map = {
        "USD": "$",
        "INR": "₹",
        "EUR": "€",
        "GBP": "£"
    }

    symbol = symbol_map.get(currency, "$")

    value = convert_currency(value, "USD", currency)

    if abs(value) >= 1e12:
        return f"{symbol}{value/1e12:.2f}T"

    if abs(value) >= 1e9:
        return f"{symbol}{value/1e9:.2f}B"

    if abs(value) >= 1e6:
        return f"{symbol}{value/1e6:.2f}M"

    return f"{symbol}{value:.2f}"

st.markdown("### 📊 Fundamentals Snapshot")

fundamentals = get_fundamentals(ticker)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Market Cap", format_currency(fundamentals.get("Market Cap"), currency))
    st.metric("Total Revenue", format_currency(fundamentals.get("Total Revenue"), currency))
    st.metric("Net Income", format_currency(fundamentals.get("Net Income"), currency))

with col2:
    st.metric("PE Ratio", format_currency(fundamentals.get("PE Ratio"), currency))
    st.metric("Debt to Equity", format_currency(fundamentals.get("Debt to Equity"), currency))

with col3:
    st.metric("ROE", f"{fundamentals.get('ROE',0)*100:.2f}%")
    st.metric("Free Cash Flow", format_currency(fundamentals.get("Free Cash Flow"), currency))

# ---------------- AI EXPLANATION ----------------

st.markdown("### 🧠 AI Explanation")

if "ai_explanation" not in st.session_state:
    st.session_state.ai_explanation = None

if st.button("Generate AI Explanation"):

    with st.spinner("AI analyzing..."):

        st.session_state.ai_explanation = get_ai_explanation(
            ticker,
            metrics,
            fundamentals,
            currency
        )

        save_ai_report(ticker, st.session_state.ai_explanation)

if st.session_state.ai_explanation:

    st.markdown(
    f"""
    <div style="
        background-color: var(--secondary-background-color);
        padding:20px;
        border-radius:12px;
        line-height:1.6;
        font-size:16px;
        color: var(--text-color);
    ">
    {st.session_state.ai_explanation}
    </div>
    """,
    unsafe_allow_html=True
)
#----------- Ask AI Agent --------------

st.markdown("### 💬 Ask AI About This Asset")

if "ask_ai_answer" not in st.session_state:
    st.session_state.ask_ai_answer = None

with st.form("ask_ai_form"):

    user_question = st.text_input(
        "Ask a financial question",
        placeholder="Example: Is this asset overvalued?"
    )

    submit_question = st.form_submit_button("Ask AI")

if submit_question and user_question:

    with st.spinner("AI analyzing..."):

        st.session_state.ask_ai_answer = ask_ai_about_stock(
            ticker,
            metrics,
            fundamentals,
            user_question,
            currency
        )

if st.session_state.ask_ai_answer:

    st.markdown(
    f"""
    <div style="
        background-color: var(--secondary-background-color);
        padding:20px;
        border-radius:12px;
        line-height:1.6;
        font-size:16px;
        color: var(--text-color);
    ">
    {st.session_state.ask_ai_answer}
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- COMPARISON ----------------

# ================= ASSET COMPARISON =================
st.markdown("### ⚖️ Asset Comparison")

# Keep comparison result persistent
if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = None

colA, colB = st.columns(2)

ticker_1 = None
ticker_2 = None

# ---------- FIRST ASSET SEARCH ----------

with colA:

    search_1 = st.text_input(
        "Search First Asset",
        placeholder="Example: Apple, BTC, Reliance",
        key="search_asset_1"
    )

    if search_1 and len(search_1) >= 2:

        results_1 = search_yahoo_stocks(search_1)

        if results_1:

            selected_1 = st.selectbox(
                "Select First Asset",
                results_1,
                key="select_asset_1"
            )

            ticker_1 = selected_1.split(" - ")[0]

        else:
            st.warning("No assets found.")


# ---------- SECOND ASSET SEARCH ----------

with colB:

    search_2 = st.text_input(
        "Search Second Asset",
        placeholder="Example: Microsoft, ETH, TCS",
        key="search_asset_2"
    )

    if search_2 and len(search_2) >= 2:

        results_2 = search_yahoo_stocks(search_2)

        if results_2:

            selected_2 = st.selectbox(
                "Select Second Asset",
                results_2,
                key="select_asset_2"
            )

            ticker_2 = selected_2.split(" - ")[0]

        else:
            st.warning("No assets found.")


# ---------- RUN COMPARISON ----------

if st.button("Compare Assets"):

    if ticker_1 and ticker_2 and ticker_1 != ticker_2:

        with st.spinner("Comparing assets..."):

            try:

                m1, f1, m2, f2, verdict = compare_assets(
                    ticker_1,
                    ticker_2,
                    period
                )

                st.session_state.comparison_result = verdict

                # Save to database
                save_asset_comparison(
                    ticker_1,
                    ticker_2,
                    float(m1["total_return"]),
                    float(m2["total_return"]),
                    float(m1["volatility"]),
                    float(m2["volatility"]),
                    verdict
                )

            except Exception as e:
                st.error(f"Comparison failed: {str(e)}")

    else:
        st.warning("Please select two different assets.")


# ---------- DISPLAY RESULT ----------

# ---------- DISPLAY RESULT ----------

if st.session_state.comparison_result is not None:

    st.markdown("### 📊 Asset Comparison Result")

    clean_text = (
        st.session_state.comparison_result
        .replace("`", "")
        .replace("|", "")
    )

    st.markdown(
        f"""
        <div style="
            background-color: var(--secondary-background-color);
            padding:22px;
            border-radius:12px;
            line-height:1.7;
            font-size:16px;
            color: var(--text-color);
        ">
        {clean_text}
        """,
        unsafe_allow_html=True
    )
