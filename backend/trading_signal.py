import numpy as np


def generate_trading_signal(current_price, future_prices):

    future_prices = future_prices.flatten()

    predicted_price = future_prices[-1]

    # Expected return
    expected_return = ((predicted_price - current_price) / current_price) * 100

    # Volatility (risk indicator)
    volatility = np.std(future_prices)

    # =========================
    # TRADING SIGNAL
    # =========================

    if expected_return > 8:
        signal = "🚀 Strong Buy (Long)"

    elif expected_return > 3:
        signal = "📈 Buy"

    elif expected_return < -8:
        signal = "⚠ Strong Sell (Short)"

    elif expected_return < -3:
        signal = "📉 Sell"

    else:
        signal = "⏳ Hold"

    # =========================
    # RISK SCORE
    # =========================

    if volatility < current_price * 0.01:
        risk = "🟢 Low Risk"

    elif volatility < current_price * 0.03:
        risk = "🟡 Medium Risk"

    else:
        risk = "🔴 High Risk"

    # =========================
    # CONFIDENCE SCORE
    # =========================

    trend_strength = abs(expected_return)

    if trend_strength > 10:
        confidence = "High Confidence"

    elif trend_strength > 4:
        confidence = "Moderate Confidence"

    else:
        confidence = "Low Confidence"

    return {
        "signal": signal,
        "expected_return": expected_return,
        "volatility": volatility,
        "predicted_price": predicted_price,
        "risk": risk,
        "confidence": confidence
    }