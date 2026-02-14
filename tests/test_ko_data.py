import unittest
from unittest.mock import patch
import pandas as pd
from ko.data import get_stock_data


class TestGetStockData(unittest.TestCase):
    def make_df(self, days=12, include_adj=True):
        idx = pd.date_range(end=pd.Timestamp.today(), periods=days, freq="B")
        data = {
            "Open": [100 + i for i in range(days)],
            "High": [100 + i + 1 for i in range(days)],
            "Low": [100 + i - 1 for i in range(days)],
            "Close": [100 + i for i in range(days)],
            "Volume": [1000 + i for i in range(days)],
        }
        df = pd.DataFrame(data, index=idx)
        if include_adj:
            df["Adj Close"] = df["Close"]
        return df

    @patch("ko.data.yf.Ticker")
    def test_returns_last_10_rows_and_adj_close_present(self, mock_ticker_cls):
        df_full = self.make_df(days=12, include_adj=True)
        mock_ticker = mock_ticker_cls.return_value
        mock_ticker.history.return_value = df_full

        result = get_stock_data("KO", period="30d", interval="1d")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 10)
        self.assertIn("Adj Close", result.columns)

    @patch("ko.data.yf.Ticker")
    def test_adds_adj_close_when_missing(self, mock_ticker_cls):
        df_full = self.make_df(days=12, include_adj=False)
        mock_ticker = mock_ticker_cls.return_value
        mock_ticker.history.return_value = df_full

        result = get_stock_data("KO", period="30d", interval="1d")
        self.assertIn("Adj Close", result.columns)
        self.assertEqual(len(result), 10)
        pd.testing.assert_series_equal(result["Adj Close"], result["Close"])

    @patch("ko.data.yf.Ticker")
    def test_returns_empty_df_when_no_data(self, mock_ticker_cls):
        mock_ticker = mock_ticker_cls.return_value
        mock_ticker.history.return_value = pd.DataFrame()
        result = get_stock_data("KO")
        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
