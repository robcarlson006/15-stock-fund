"""Write README.md from the latest tracking outputs (rebuilt every run)."""
import json
import os
import sys
from urllib.parse import quote

import pandas as pd

from common import CONFIG, HOLDINGS, NAV, ROOT, SUMMARY

MINUS = "−"


def pct(v, signed=True, dp=2):
    if v is None:
        return "n/a"
    return (f"{v:+.{dp}%}" if signed else f"{v:.{dp}%}").replace("-", MINUS)


def money(v, signed=False):
    s = f"${abs(v):,.2f}"
    return (("+" if v >= 0 else MINUS) + s) if signed else s


def badge(label, value, color):
    q = lambda x: quote(str(x).replace("-", "--").replace("_", "__").replace(" ", "_"), safe="")
    return f"![{label}](https://img.shields.io/badge/{q(label)}-{q(value)}-{color}?style=flat-square)"


def chart(name, alt, chart_dir="assets/charts"):
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{chart_dir}/{name}-dark.png">\n'
            f'  <img alt="{alt}" src="{chart_dir}/{name}-light.png" width="100%">\n</picture>')


def main() -> int:
    s = json.loads(SUMMARY.read_text())
    h = pd.read_csv(HOLDINGS)
    nav = pd.read_csv(NAV)
    bench = CONFIG["benchmark"]["name"]
    asof = pd.Timestamp(s["as_of"]).strftime("%-d %b %Y")
    inc = pd.Timestamp(s["inception"]).strftime("%-d %b %Y")
    repo = os.environ.get("GITHUB_REPOSITORY") or CONFIG.get("repo")
    exc = s["excess_return"]

    badges = [
        badge("fund", pct(s["total_return"]), "2a78d6"),
        badge(f"vs {bench}", f"{exc * 100:+.2f} pts".replace("-", MINUS), "2ea44f" if exc >= 0 else "d73a49"),
        badge("as of", s["as_of"], "555"),
        badge("holdings", s["positions"], "555"),
    ]
    if repo:
        badges.insert(0, f"[![daily update](https://github.com/{repo}/actions/workflows/daily-update.yml/badge.svg)]"
                         f"(https://github.com/{repo}/actions/workflows/daily-update.yml)")

    note = ""
    if s["mode"] == "model":
        note = (f"> [!NOTE]\n> Positions are currently **modelled** as the target dollar amounts bought at the "
                f"{inc} close. They switch to the actual Robinhood fills as soon as "
                f"[`portfolio/trade_log.csv`](portfolio/trade_log.csv) is filled in.\n\n")

    def stat(v, fmt):
        return fmt(v) if v is not None else "_20d+_"

    exc_s = f"{exc * 100:+.2f} pts".replace("-", MINUS)
    vol = pct(s["volatility"], False, 1) if s["volatility"] is not None else "_after 5 days_"
    beat = (pct(s["days_beat_benchmark"], False, 0)
            if s["days_beat_benchmark"] is not None and s["trading_days"] > 1 else "—")
    kpi = (
        f"| NAV | Since inception | {bench} | Excess return | Last session |\n"
        "|:--:|:--:|:--:|:--:|:--:|\n"
        f"| **{money(s['nav'])}** | **{pct(s['total_return'])}** | {pct(s['benchmark_return'])} | "
        f"**{exc_s}** | {pct(s['day_return'])} vs {pct(s['benchmark_day_return'])} |\n"
    )
    risk = (
        "| Max drawdown | Volatility | Sharpe | Beta | Tracking error | Days beating index | Dividends | Days tracked |\n"
        "|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n"
        f"| {pct(s['max_drawdown'], False)} | {vol} | {stat(s['sharpe'], lambda v: f'{v:.2f}')} | "
        f"{stat(s['beta'], lambda v: f'{v:.2f}')} | {stat(s['tracking_error'], lambda v: pct(v, False, 1))} | "
        f"{beat} | {money(s['dividends_received'])} | {s['trading_days']} |\n"
    )

    rows = ["| | Ticker | Company | Sector | Weight | Target | Price | Return | P&L |",
            "|--:|:--|:--|:--|--:|--:|--:|--:|--:|"]
    for i, r in enumerate(h[h["shares"] > 0].itertuples(), 1):
        rows.append(f"| {i} | **{r.ticker}** | {r.company} | {r.sector} | {r.weight:.1%} | "
                    f"{r.target_weight:.0%} | ${r.price:,.2f} | {pct(r.return_pct, dp=1)} | "
                    f"{money(r.total_pl, True)} |")
    holdings = "\n".join(rows)

    md = f"""<div align="center">

# {CONFIG['fund_name']}

**{CONFIG['tagline']}**

{' '.join(badges)}

</div>

{note}## Performance

{kpi}
{risk}
{chart('performance', 'Cumulative return of the fund vs the S&P 500 Total Return')}

<sub>Updated automatically after every US market close. Time-weighted returns, dividends included; benchmark is the {bench} index ({CONFIG['benchmark']['ticker']}). Data as of {asof}.</sub>

## Holdings

{holdings}

{chart('holdings', 'Return by holding since purchase')}

{chart('allocation', 'Current weight vs target weight, by holding and by sector')}

{chart('drawdown', 'Fund drawdown vs benchmark drawdown')}

## How the 15 were picked

{chart('funnel', 'Selection funnel: 75 candidates, 25 shortlisted, 15 held')}

The fund was built the way an institutional fund is: **rules first, then data, then picks, then sizing.** Every rule was written down before any company was scored, and every change is dated in the [decision log](journal/decision-log.md).

| Stage | What happened | Output |
|:--|:--|:--|
| **0. Policy** | Wrote the investment policy (1-year horizon, {bench} benchmark, monthly review) and the scoring rules | [Investment policy](02_policy/investment-policy-statement.md) · [Scoring framework](03_methodology/scoring-framework.md) |
| **1. 75 → 25** | Pulled a Bloomberg financial-analysis report for all 75 on one day, parsed them with Python, removed red flags, then scored each company **against its own sector** on quality, value, balance sheet and growth | [Shortlist memo](analysis/stage1_75_to_25/shortlist_25.md) |
| **2. 25 → 15** | Pulled fuller Bloomberg data, re-scored (Piotroski F-score, earnings-beat record, consensus growth, cash yield after stock pay), ran robustness checks on the weights, applied sector and theme limits | [Investment committee memo](analysis/stage2_25_to_15/final_15.md) |
| **3. Sizing** | Tiered dollar weights ($8 / $7 / $5) with position and sector caps, checked by script | [Target allocation](portfolio/target_allocation.csv) |
| **4. Run it** | Daily tracking (this page) and a monthly review against written sell triggers | [Monthly journal](journal/monthly/) |

Every holding has a one-line thesis and a **written sell trigger** set before purchase, in [`target_allocation.csv`](portfolio/target_allocation.csv).

## How the tracking works

```mermaid
flowchart LR
    A[GitHub Actions<br/>weekdays after close] --> B[prices.py<br/>Yahoo Finance closes<br/>and dividends]
    B --> C[nav.py<br/>positions from trade log<br/>NAV, returns, risk]
    C --> D[charts.py<br/>light + dark charts]
    D --> E[readme.py<br/>this page]
    E --> F[(Commit to repo<br/>timestamped record)]
```

- **Schedule:** every weekday at 21:30 UTC (4:30 pm New York in winter, 5:30 pm in summer), after the close. Market holidays add no row.
- **Positions:** rebuilt each run from [`portfolio/trade_log.csv`](portfolio/trade_log.csv), so a new trade only needs one line in that file.
- **Returns:** time-weighted (new money is not counted as performance). Dividends are credited on the ex-date as an estimate of cash the broker pays on the pay date.
- **Data files:** [`tracking/nav.csv`](tracking/nav.csv) (daily NAV and index levels), [`tracking/prices.csv`](tracking/prices.csv), [`tracking/holdings.csv`](tracking/holdings.csv), [`tracking/summary.json`](tracking/summary.json).
- **Audit trail:** each daily commit is a timestamped record of the portfolio, so the track record can't be backfilled or edited after the fact without it showing in the history.

## Repository layout

```
02_policy/          investment policy statement
03_methodology/     scoring rules for every stage
analysis/           Stage 1 and Stage 2 scores, robustness checks, memos
portfolio/          target allocation and trade log
journal/            decision log and monthly reviews
tracking/           daily prices, NAV, holdings, summary (auto-updated)
assets/charts/      README charts (auto-updated)
tools/              Python: Bloomberg extraction, scoring, sizing, daily tracker
```

---

<sub>Educational project with real money ($100). Picks are the output of written rules, not investment advice. Raw Bloomberg exports are not redistributed in this repository. Prices from Yahoo Finance; small differences from broker prices are expected.</sub>
"""
    (ROOT / "README.md").write_text(md)
    print("readme: written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
