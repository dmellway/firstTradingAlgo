from ko.data import get_stock_data
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from typing import Optional


def plot_last_10(ticker: str = "KO", save_path: Optional[str] = None, show: bool = True) -> None:
    """Fetch the last 10 trading rows for `ticker` and plot `Adj Close` using matplotlib.

    If `save_path` is provided the plot will be written to that path (PNG). By default the
    figure is shown with `plt.show()`; pass `show=False` to avoid displaying.
    """
    df = get_stock_data(ticker=ticker, period="30d", interval="1d")
    if df.empty:
        print(f"No data available for {ticker!r}.")
        return

    series = df["Adj Close"] if "Adj Close" in df.columns else df["Close"]

    plt.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(series.index, series.values, marker="o", linewidth=2)
    ax.set_title(f"{ticker} — Last {len(series)} trading days (Adj Close)")
    ax.set_ylabel("Price (USD)")
    ax.set_xlabel("Date")
    fig.autofmt_xdate()
    plt.tight_layout()

    if save_path:
        p = Path(save_path).expanduser()
        if p.parent:
            p.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(p, dpi=300)
        print(f"Saved plot to {p}")

    if show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot last 10 trading days for a ticker (Adj Close).")
    parser.add_argument("ticker", nargs="?", default="KO", help="Ticker symbol (default: KO)")
    parser.add_argument("--save", "-s", dest="save", help="Path to save PNG (optional)")
    parser.add_argument("--no-show", action="store_true", help="Do not call plt.show()")
    args = parser.parse_args()
    plot_last_10(ticker=args.ticker, save_path=args.save, show=not args.no_show)
