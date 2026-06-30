import yfinance as yf

def convert_currency(price, from_currency="USD", to_currency="USD"):

    if price is None:
        return None

    if from_currency == to_currency:
        return price

    pair = f"{from_currency}{to_currency}=X"

    try:
        rate = yf.Ticker(pair).history(period="1d")["Close"].iloc[-1]
        return price * rate
    except:
        return price


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