import requests

from backend.currency import format_currency

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def ask_ai_about_stock(ticker, metrics, fundamentals, question, currency):

    prompt = f"""
You are a professional financial analyst.

Stock: {ticker}

Performance:
Start Price: {format_currency(metrics['start_price'], currency)}
End Price: {format_currency(metrics['end_price'], currency)}
Return: {metrics['total_return']:.2f}%
Volatility: {metrics['volatility']:.2f}%

Fundamentals:
Market Cap: {format_currency(fundamentals.get("Market Cap"), currency)}
Revenue: {format_currency(fundamentals.get("Total Revenue"), currency)}
PE Ratio: {format_currency(fundamentals.get("PE Ratio"), currency)}
ROE: {format_currency(fundamentals.get("ROE"), currency)}

User Question:
{question}

Explain clearly in simple terms.
Do not give direct financial advice.
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

        # Check if request failed
        if response.status_code != 200:
            return f"AI Error: {response.text}"

        data = response.json()

        # Ollama returns "response"
        return data.get("response", "AI could not generate answer.")

    except Exception as e:
        return f"AI Error: {str(e)}"