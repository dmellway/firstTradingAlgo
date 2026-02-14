import pandas as pd
import yfinance as yf
from typing import Optional


def get_stock_data(ticker: str = "KO", period: str = "30d", interval: str = "1d") -> pd.DataFrame:
    """Fetch recent price history for `ticker` and return the last 10 trading rows.

    - ticker: stock symbol (default "KO")
    - period: how far back to fetch (use a larger window, e.g. "30d", to ensure 10 trading days)
    - interval: data interval (daily = "1d")
    """
    df = yf.Ticker(ticker).history(period=period, interval=interval)
    if df is None or df.empty:
        return pd.DataFrame()

    # ensure 'Adj Close' exists (fall back to 'Close' if necessary)
    if "Adj Close" not in df.columns and "Close" in df.columns:
        df["Adj Close"] = df["Close"]

    # return the last 10 trading rows
    return df.tail(10)
