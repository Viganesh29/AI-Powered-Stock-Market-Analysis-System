import yfinance as yf
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense


def predict_hybrid(ticker, days):

    # ==============================
    # DOWNLOAD DATA
    # ==============================

    df = yf.download(ticker, period="5y")

    if df.empty:
        return None

    # Only use closing price
    close_prices = df["Close"].values

    # ==============================
    # SCALE DATA
    # ==============================

    scaler = MinMaxScaler(feature_range=(0, 1))

    scaled_data = scaler.fit_transform(close_prices.reshape(-1, 1))

    # ==============================
    # CREATE TRAINING DATA
    # ==============================

    window = 60

    X = []
    y = []

    for i in range(window, len(scaled_data)):
        X.append(scaled_data[i-window:i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X)
    y = np.array(y)

    # reshape for LSTM
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # ==============================
    # BUILD MODEL
    # ==============================

    model = Sequential()

    model.add(
        LSTM(
            units=50,
            return_sequences=True,
            input_shape=(X.shape[1], 1)
        )
    )

    model.add(LSTM(units=50))

    model.add(Dense(1))

    model.compile(
        optimizer="adam",
        loss="mean_squared_error"
    )

    model.fit(
        X,
        y,
        epochs=5,
        batch_size=32,
        verbose=0
    )

    # ==============================
    # PREDICT FUTURE
    # ==============================

    last_window = scaled_data[-window:]

    future_predictions = []

    current_window = last_window

    for _ in range(days):

        pred = model.predict(
            current_window.reshape(1, window, 1),
            verbose=0
        )

        future_predictions.append(pred[0][0])

        current_window = np.append(
            current_window[1:],
            pred
        )

    future_predictions = np.array(future_predictions)

    # ==============================
    # INVERSE SCALE
    # ==============================

    future_prices = scaler.inverse_transform(
        future_predictions.reshape(-1, 1)
    )

    return future_prices