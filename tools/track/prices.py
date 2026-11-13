"""Pull daily closes and dividends for every holding plus the benchmark.

Re-downloads from just before inception each run (cheap, and it picks up any
late corrections), then merges over the stored file so a bad download never
wipes good history.
"""
import sys

import pandas as pd
import yfinance as yf

from common import BENCH, DIVIDENDS, INCEPTION, PRICES, tickers


def main() -> int:
    names = tickers() + [BENCH]
    start = (INCEPTION - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    raw = yf.download(names, start=start, auto_adjust=False, actions=True,
                      progress=False, threads=True)
    if raw.empty:
        print("ERROR: no data returned from Yahoo Finance", file=sys.stderr)
        return 1

    close = raw["Close"].reindex(columns=names)
    close.index = pd.to_datetime(close.index).tz_localize(None).normalize()
    close = close.dropna(how="all")
    missing = [c for c in names if close[c].dropna().empty]
    if missing:
        print(f"ERROR: no prices for {missing}", file=sys.stderr)
        return 1

    if PRICES.exists():
        old = pd.read_csv(PRICES, index_col="date", parse_dates=True)
        close = close.combine_first(old)  # new values win, old fill gaps
    close.index.name = "date"
    close.sort_index().round(4).to_csv(PRICES)

    div = raw["Dividends"].reindex(columns=names).drop(columns=[BENCH])
    div.index = pd.to_datetime(div.index).tz_localize(None).normalize()
    div = div.stack()
    div = div[div > 0].rename("cash_per_share").reset_index()
    div.columns = ["ex_date", "ticker", "cash_per_share"]
    if DIVIDENDS.exists():
        old = pd.read_csv(DIVIDENDS, parse_dates=["ex_date"])
        div = pd.concat([old, div]).drop_duplicates(["ex_date", "ticker"], keep="last")
    div.sort_values(["ex_date", "ticker"]).to_csv(DIVIDENDS, index=False)

    last = close.index.max().date()
    print(f"prices: {len(close)} days x {len(names)} series, latest {last}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
