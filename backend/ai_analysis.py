import requests
from backend.currency import format_currency

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def get_ai_explanation(ticker, metrics, fundamentals, currency):

    prompt = f"""
You are a professional financial analyst.

Analyze the following stock.

Ticker: {ticker}

Performance:
Start Price: {format_currency(metrics['start_price'], currency)}
End Price: {format_currency(metrics['end_price'], currency)}
Total Return: {metrics['total_return']:.2f}%
Volatility: {metrics['volatility']:.2f}%

Fundamentals:
Market Cap: {format_currency(fundamentals.get("Market Cap"), currency)}
Revenue: {format_currency(fundamentals.get("Total Revenue"), currency)}
Net Income: {format_currency(fundamentals.get("Net Income"), currency)}
PE Ratio: {fundamentals.get("PE Ratio", "N/A")}
Debt to Equity: {fundamentals.get("Debt to Equity", "N/A")}
ROE: {fundamentals.get("ROE", "N/A")}
Free Cash Flow: {format_currency(fundamentals.get("Free Cash Flow"), currency)}

All financial values are in {currency}.

Explain:

1. Company's financial health.
2. Strengths.
3. Weaknesses.
4. Investment outlook.
5. Overall conclusion.

Use simple language.
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1000
                }
            },
            timeout=180
        )

        if response.status_code != 200:
            return f"AI Error: {response.text}"

        data = response.json()

        return data.get("response", "AI could not generate explanation.")

    except Exception as e:
        return f"AI Error: {str(e)}"