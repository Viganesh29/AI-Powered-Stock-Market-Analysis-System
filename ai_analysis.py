import requests
from backend.currency import format_currency
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "llama3"


def get_ai_explanation(ticker, metrics, fundamentals, currency):

    prompt = f"""
You are a financial analyst.

Analyze the following asset:

Ticker: {ticker}

Performance:
Start Price: {format_currency(metrics['start_price'], currency)}
End Price: {format_currency(metrics['end_price'], currency)}
Total Return: {(metrics['total_return']):.2f}%
Volatility: {metrics['volatility']}%

Fundamentals:
Market Cap: {format_currency(fundamentals.get("Market Cap"), currency)}
Revenue: {format_currency(fundamentals.get("Total Revenue"), currency)}
Net Income: {format_currency(fundamentals.get("Net Income"), currency)}
PE Ratio: {format_currency(fundamentals.get("PE Ratio"), currency)}
Debt to Equity: {format_currency(fundamentals.get("Debt to Equity"), currency)}
ROE: {format_currency(fundamentals.get("ROE"), currency)}
Free Cash Flow: {format_currency(fundamentals.get("Free Cash Flow"), currency)}

Explain the financial health of the company.
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=120
        )

        data = response.json()

        # Safe parsing
        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        elif "message" in data:
            return data["message"]

        else:
            return f"AI Error: Unexpected response from model → {data}"

    except Exception as e:
        return f"AI Error: {str(e)}"