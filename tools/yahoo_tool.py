import yfinance as yf

def fetch_financial_data(ticker: str) -> dict:
    """
    Fetch real financial data from Yahoo Finance.
    This is a pure Python function (NOT a crewAI tool).
    """

    stock = yf.Ticker(ticker)

    return {
        "income_statement": stock.financials.to_dict(),
        "balance_sheet": stock.balance_sheet.to_dict(),
        "cash_flow": stock.cashflow.to_dict(),
        "key_metrics": {
            "market_cap": stock.info.get("marketCap"),
            "pe_ratio": stock.info.get("trailingPE"),
            "debt_to_equity": stock.info.get("debtToEquity"),
            "return_on_equity": stock.info.get("returnOnEquity")
        }
    }
