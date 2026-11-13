"""Rebuild the fund's daily NAV, holdings and summary from the trade log.

Positions come from portfolio/trade_log.csv. If the log is still empty, the
fund is modelled as the target allocation bought at the inception-day close,
and every output is marked mode="model" so it is never mistaken for real fills.

Returns are time-weighted: r_t = NAV_t / (NAV_{t-1} + new money_t) - 1, so
adding cash later does not count as performance. Dividends are credited as
cash on the ex-date using shares held the day before (Robinhood pays on the
pay date, so this is an estimate for the gap between the two).
"""
import json
import sys

import numpy as np
import pandas as pd

from common import (BENCH, CONFIG, DIVIDENDS, HOLDINGS, INCEPTION, NAV, PRICES,
                    SUMMARY, load_targets, load_trades)


def model_trades(prices: pd.DataFrame) -> pd.DataFrame:
    day = prices.index[prices.index >= INCEPTION][0]
    rows = []
    for _, r in load_targets().iterrows():
        px = prices.at[day, r.ticker]
        rows.append(dict(date=day, ticker=r.ticker, side="buy",
                         quantity=r.target_usd / px, price_usd=px, fees_usd=0.0))
    return pd.DataFrame(rows)


def main() -> int:
    prices = pd.read_csv(PRICES, index_col="date", parse_dates=True).sort_index().ffill()
    divs = pd.read_csv(DIVIDENDS, parse_dates=["ex_date"]) if DIVIDENDS.exists() else \
        pd.DataFrame(columns=["ex_date", "ticker", "cash_per_share"])

    trades = load_trades()
    mode = "actual"
    if trades.empty:
        trades, mode = model_trades(prices), "model"

    first = trades["date"].min()
    days = prices.index[prices.index >= first.normalize()]
    if len(days) == 0:
        print("ERROR: no price days on/after first trade", file=sys.stderr)
        return 1

    names = sorted(set(trades["ticker"]))
    shares = dict.fromkeys(names, 0.0)
    cost = dict.fromkeys(names, 0.0)       # cost basis of shares still held
    bought = dict.fromkeys(names, 0.0)     # total ever spent on the name
    realized = dict.fromkeys(names, 0.0)
    div_cash = dict.fromkeys(names, 0.0)
    cash = contributed = prev_nav = 0.0
    applied = 0
    rows = []

    for d in days:
        for _, dv in divs[divs["ex_date"] == d].iterrows():
            if dv.ticker in shares and shares[dv.ticker] > 0:
                amt = shares[dv.ticker] * dv.cash_per_share
                cash += amt
                div_cash[dv.ticker] += amt

        while applied < len(trades) and trades.at[applied, "date"].normalize() <= d:
            t = trades.loc[applied]
            q, p, fee = float(t.quantity), float(t.price_usd), float(t.fees_usd)
            if t.side == "buy":
                cash -= q * p + fee
                shares[t.ticker] += q
                cost[t.ticker] += q * p + fee
                bought[t.ticker] += q * p + fee
            elif t.side == "sell":
                avg = cost[t.ticker] / shares[t.ticker]
                cash += q * p - fee
                realized[t.ticker] += q * p - fee - avg * q
                cost[t.ticker] -= avg * q
                shares[t.ticker] -= q
            else:
                print(f"ERROR: unknown side {t.side!r} in trade log", file=sys.stderr)
                return 1
            applied += 1

        flow = 0.0
        if cash < -1e-9:              # buys beyond cash on hand = new money in
            flow, cash = -cash, 0.0
            contributed += flow

        mv = sum(shares[n] * prices.at[d, n] for n in names)
        nav = mv + cash
        base = prev_nav + flow
        r = nav / base - 1 if base > 0 else 0.0
        rows.append(dict(date=d.date(), market_value=mv, cash=cash, nav=nav,
                         net_contributions=contributed, daily_return=r,
                         benchmark_close=prices.at[d, BENCH]))
        prev_nav = nav

    nav = pd.DataFrame(rows)
    nav["fund_index"] = 100 * (1 + nav["daily_return"]).cumprod()
    nav["benchmark_index"] = 100 * nav["benchmark_close"] / nav["benchmark_close"].iloc[0]
    nav["benchmark_return"] = nav["benchmark_index"].pct_change().fillna(0.0)
    nav["drawdown"] = nav["fund_index"] / nav["fund_index"].cummax() - 1
    nav["benchmark_drawdown"] = nav["benchmark_index"] / nav["benchmark_index"].cummax() - 1
    nav.round(6).to_csv(NAV, index=False)

    # ---- holdings snapshot -------------------------------------------------
    last = days[-1]
    meta = load_targets().set_index("ticker")
    total_target = meta["target_usd"].sum()
    hold = []
    for n in names:
        px = prices.at[last, n]
        mv = shares[n] * px
        pl = mv - cost[n] + realized[n] + div_cash[n]
        hold.append(dict(
            ticker=n,
            company=meta["company"].get(n, ""),
            sector=meta["sector"].get(n, ""),
            shares=shares[n], avg_cost=cost[n] / shares[n] if shares[n] else np.nan,
            price=px, market_value=mv, weight=mv / nav["nav"].iloc[-1],
            target_weight=meta["target_usd"].get(n, 0) / total_target,
            dividends=div_cash[n], realized_pl=realized[n], total_pl=pl,
            return_pct=pl / bought[n] if bought[n] else np.nan))
    hold = pd.DataFrame(hold).sort_values("market_value", ascending=False)
    hold.round(6).to_csv(HOLDINGS, index=False)

    # ---- summary ------------------------------------------------------------
    r = nav["daily_return"].iloc[1:]
    b = nav["benchmark_return"].iloc[1:]
    n = len(r)
    ann = np.sqrt(252)
    rf_d = CONFIG["risk_free_rate_annual"] / 252
    held = hold[hold["shares"] > 0]
    summ = dict(
        as_of=str(last.date()), mode=mode, inception=str(days[0].date()),
        trading_days=len(nav), nav=nav["nav"].iloc[-1],
        net_contributions=contributed, cash=cash,
        total_return=nav["fund_index"].iloc[-1] / 100 - 1,
        benchmark_return=nav["benchmark_index"].iloc[-1] / 100 - 1,
        day_return=float(r.iloc[-1]) if n else 0.0,
        benchmark_day_return=float(b.iloc[-1]) if n else 0.0,
        max_drawdown=nav["drawdown"].min(),
        benchmark_max_drawdown=nav["benchmark_drawdown"].min(),
        volatility=r.std() * ann if n >= 5 else None,
        benchmark_volatility=b.std() * ann if n >= 5 else None,
        sharpe=((r.mean() - rf_d) / r.std() * ann) if n >= 20 and r.std() > 0 else None,
        beta=(np.cov(r, b)[0, 1] / b.var()) if n >= 20 and b.var() > 0 else None,
        tracking_error=(r - b).std() * ann if n >= 20 else None,
        days_beat_benchmark=float((r > b).mean()) if n else None,
        dividends_received=sum(div_cash.values()),
        positions=int(len(held)),
        best=held.nlargest(1, "return_pct")[["ticker", "return_pct"]].to_dict("records")[0],
        worst=held.nsmallest(1, "return_pct")[["ticker", "return_pct"]].to_dict("records")[0],
    )
    summ["excess_return"] = summ["total_return"] - summ["benchmark_return"]
    summ = {k: (float(v) if isinstance(v, (np.floating, np.integer)) else v) for k, v in summ.items()}
    SUMMARY.write_text(json.dumps(summ, indent=2, default=float) + "\n")
    print(f"nav: {mode}, {len(nav)} days, NAV ${summ['nav']:.2f}, "
          f"fund {summ['total_return']:+.2%} vs bench {summ['benchmark_return']:+.2%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
