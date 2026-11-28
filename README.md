<div align="center">

# 15-Stock Rules-Based Fund

**A $100, 15-stock US equity fund picked by written rules from Bloomberg data, tracked daily against the S&P 500 Total Return.**

[![daily update](https://github.com/robcarlson006/15-stock-fund/actions/workflows/daily-update.yml/badge.svg)](https://github.com/robcarlson006/15-stock-fund/actions/workflows/daily-update.yml) ![fund](https://img.shields.io/badge/fund-%E2%88%924.39%25-2a78d6?style=flat-square) ![vs S&P 500 Total Return](https://img.shields.io/badge/vs_S%26P_500_Total_Return-%E2%88%920.95_pts-d73a49?style=flat-square) ![as of](https://img.shields.io/badge/as_of-2026--11--27-555?style=flat-square) ![holdings](https://img.shields.io/badge/holdings-15-555?style=flat-square)

</div>

## Performance

| NAV | Since inception | S&P 500 Total Return | Excess return | Last session |
|:--:|:--:|:--:|:--:|:--:|
| **$96.09** | **−4.39%** | −3.44% | **−0.95 pts** | +1.22% vs +1.60% |

| Max drawdown | Volatility | Sharpe | Beta | Tracking error | Days beating index | Dividends | Days tracked |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| −9.06% | 30.4% | _20d+_ | _20d+_ | _20d+_ | 44% | $0.23 | 10 |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/charts/performance-dark.png">
  <img alt="Cumulative return of the fund vs the S&P 500 Total Return" src="assets/charts/performance-light.png" width="100%">
</picture>

<sub>Updated automatically after every US market close. Time-weighted returns, dividends included; benchmark is the S&P 500 Total Return index (^SP500TR). Data as of 27 Nov 2026.</sub>

## Holdings

| | Ticker | Company | Sector | Weight | Target | Price | Return | P&L |
|--:|:--|:--|:--|--:|--:|--:|--:|--:|
| 1 | **COST** | Costco | Cons. Staples | 8.3% | 8% | $1,097.81 | +1.9% | +$0.15 |
| 2 | **NFLX** | Netflix | Comm. Services | 8.2% | 8% | $60.93 | −2.0% | −$0.16 |
| 3 | **LLY** | Eli Lilly | Health Care | 8.0% | 8% | $1,392.38 | −3.7% | −$0.29 |
| 4 | **BKNG** | Booking Holdings | Cons. Discretionary | 7.8% | 8% | $150.39 | −6.6% | −$0.53 |
| 5 | **VRT** | Vertiv | Industrials | 7.8% | 8% | $178.71 | −6.6% | −$0.53 |
| 6 | **PGR** | Progressive | Financials | 7.3% | 7% | $239.14 | +0.1% | +$0.01 |
| 7 | **NVO** | Novo Nordisk (ADR) | Health Care | 7.1% | 7% | $41.07 | −2.2% | −$0.15 |
| 8 | **FICO** | Fair Isaac | Technology | 7.1% | 7% | $708.57 | −3.0% | −$0.21 |
| 9 | **ISRG** | Intuitive Surgical | Health Care | 7.1% | 7% | $430.18 | −3.2% | −$0.22 |
| 10 | **ADBE** | Adobe | Technology | 7.0% | 7% | $234.79 | −3.3% | −$0.23 |
| 11 | **WPC** | W. P. Carey | Real Estate | 5.3% | 5% | $66.97 | +1.0% | +$0.05 |
| 12 | **VST** | Vistra | Utilities | 4.9% | 5% | $122.65 | −5.0% | −$0.25 |
| 13 | **JPM** | JPMorgan Chase | Financials | 4.9% | 5% | $322.96 | −6.5% | −$0.33 |
| 14 | **FCX** | Freeport-McMoRan | Materials | 4.6% | 5% | $50.77 | −10.9% | −$0.55 |
| 15 | **CEG** | Constellation Energy | Utilities | 4.5% | 5% | $238.10 | −13.8% | −$0.69 |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/charts/holdings-dark.png">
  <img alt="Return by holding since purchase" src="assets/charts/holdings-light.png" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/charts/allocation-dark.png">
  <img alt="Current weight vs target weight, by holding and by sector" src="assets/charts/allocation-light.png" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/charts/drawdown-dark.png">
  <img alt="Fund drawdown vs benchmark drawdown" src="assets/charts/drawdown-light.png" width="100%">
</picture>

## How the 15 were picked

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/charts/funnel-dark.png">
  <img alt="Selection funnel: 75 candidates, 25 shortlisted, 15 held" src="assets/charts/funnel-light.png" width="100%">
</picture>

The fund was built the way an institutional fund is: **rules first, then data, then picks, then sizing.** Every rule was written down before any company was scored, and every change is dated in the [decision log](journal/decision-log.md).

| Stage | What happened | Output |
|:--|:--|:--|
| **0. Policy** | Wrote the investment policy (1-year horizon, S&P 500 Total Return benchmark, monthly review) and the scoring rules | [Investment policy](02_policy/investment-policy-statement.md) · [Scoring framework](03_methodology/scoring-framework.md) |
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
- **Returns:** fund and index are both measured from the inception-day close, then time-weighted (new money is not counted as performance). P&L per holding is measured from the actual fill price. Dividends are credited on the ex-date as an estimate of cash the broker pays on the pay date.
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
