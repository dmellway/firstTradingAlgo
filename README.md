# firstTradingAlgo
This will be a collection of trading stratgies for algo tradiing

## Plot KO (last 10 trading days)

Requirements:

```bash
pip install -r requirements.txt
```

Run the plot script:

```bash
python plot_ko.py
```

The script fetches the last 10 trading rows for ticker `KO` using `yfinance` and shows a Matplotlib plot of `Adj Close`.
