from backend.performance import get_stock_performance
from backend.fundamentals import get_fundamentals
import numpy as np


def compare_assets(ticker1, ticker2, period):

    data1 = get_stock_performance(ticker1, period)
    data2 = get_stock_performance(ticker2, period)

    if data1 is None or data2 is None:
        return None, None, None, None, "⚠️ Could not fetch data."

    df1, metrics1 = data1
    df2, metrics2 = data2

    f1 = get_fundamentals(ticker1)
    f2 = get_fundamentals(ticker2)

    # Sharpe Ratio
    sharpe1 = metrics1["total_return"] / metrics1["volatility"] if metrics1["volatility"] != 0 else 0
    sharpe2 = metrics2["total_return"] / metrics2["volatility"] if metrics2["volatility"] != 0 else 0

    # Determine winner
    score1 = 0
    score2 = 0

    if metrics1["total_return"] > metrics2["total_return"]:
        score1 += 1
    else:
        score2 += 1

    if metrics1["volatility"] < metrics2["volatility"]:
        score1 += 1
    else:
        score2 += 1

    if sharpe1 > sharpe2:
        score1 += 1
    else:
        score2 += 1

    winner = ticker1 if score1 > score2 else ticker2

    verdict = f"""
📊 **Performance Comparison**

Return:
{ticker1}: {metrics1['total_return']:.2f}%  

{ticker2}: {metrics2['total_return']:.2f}%

Volatility (Risk):
{ticker1}: {metrics1['volatility']:.2f}%  

{ticker2}: {metrics2['volatility']:.2f}%

Sharpe Ratio:
{ticker1}: {sharpe1:.2f}  

{ticker2}: {sharpe2:.2f}

Current Price:
{ticker1}: ${metrics1['end_price']:.2f} 

{ticker2}: ${metrics2['end_price']:.2f}

📊 **Fundamentals Comparison**

Market Cap:
{ticker1}: {f1.get("Market Cap")}  

{ticker2}: {f2.get("Market Cap")}

Revenue:
{ticker1}: {f1.get("Total Revenue")}  

{ticker2}: {f2.get("Total Revenue")}

PE Ratio:
{ticker1}: {f1.get("PE Ratio")}  

{ticker2}: {f2.get("PE Ratio")}

ROE:
{ticker1}: {f1.get("ROE")}  

{ticker2}: {f2.get("ROE")}

🏆 **Overall Better Asset: {winner}**
"""

    return metrics1, f1, metrics2, f2, verdict