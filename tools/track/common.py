"""Shared paths and loaders for the daily tracker."""
import json
import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
# Overridable so chart/README rendering can be tested on sample data.
TRACK = Path(os.environ.get("FUND_TRACK_DIR", ROOT / "tracking"))
CHARTS = Path(os.environ.get("FUND_CHART_DIR", ROOT / "assets" / "charts"))
CONFIG = json.loads((TRACK / "config.json").read_text())

TRADE_LOG = ROOT / "portfolio" / "trade_log.csv"
TARGETS = ROOT / "portfolio" / "target_allocation.csv"
PRICES = TRACK / "prices.csv"          # daily close (not dividend-adjusted)
DIVIDENDS = TRACK / "dividends.csv"    # ex-date, ticker, cash per share
NAV = TRACK / "nav.csv"
HOLDINGS = TRACK / "holdings.csv"
SUMMARY = TRACK / "summary.json"

BENCH = CONFIG["benchmark"]["ticker"]
INCEPTION = pd.Timestamp(CONFIG["inception_date"])


def load_targets() -> pd.DataFrame:
    return pd.read_csv(TARGETS)


def load_trades() -> pd.DataFrame:
    t = pd.read_csv(TRADE_LOG)
    if t.empty:
        return t
    t["date"] = pd.to_datetime(t["date"])
    t["side"] = t["side"].str.lower().str.strip()
    t["fees_usd"] = t["fees_usd"].fillna(0.0)
    return t.sort_values("date").reset_index(drop=True)


def tickers() -> list[str]:
    """Every name ever held or targeted, so prices exist for all of them."""
    names = set(load_targets()["ticker"])
    trades = load_trades()
    if not trades.empty:
        names |= set(trades["ticker"])
    return sorted(names)
