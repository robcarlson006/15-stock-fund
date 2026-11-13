<div align="center">

# 15-Stock Rules-Based Fund

**A $100, 15-stock US equity fund picked by written rules from Bloomberg data, tracked daily against the S&P 500 Total Return.**

![fund](https://img.shields.io/badge/fund-%2B0.00%25-2a78d6?style=flat-square) ![vs S&P 500 Total Return](https://img.shields.io/badge/vs_S%26P_500_Total_Return-%2B0.00_pts-2ea44f?style=flat-square) ![as of](https://img.shields.io/badge/as_of-2026--11--13-555?style=flat-square) ![holdings](https://img.shields.io/badge/holdings-15-555?style=flat-square)

</div>

> [!NOTE]
> Positions are currently **modelled** as the target dollar amounts bought at the 13 Nov 2026 close. They switch to the actual Robinhood fills as soon as [`portfolio/trade_log.csv`](portfolio/trade_log.csv) is filled in.

## Performance

| NAV | Since inception | S&P 500 Total Return | Excess return | Max drawdown | Days tracked |
|:−−:|:−−:|:−−:|:−−:|:−−:|:−−:|
| **$100.00** | **+0.00%** | +0.00% | **+0.00 pts** | +0.00% | 1 |

| Last session | Volatility (ann.) | Sharpe | Beta | Tracking error | Days beating index | Dividends |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| +0.00% vs +0.00% | _after 5 days_ | _after 20 days_ | _after 20 days_ | _after 20 days_ | — | $0.00 |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/charts/performance-dark.png">
  <img alt="Cumulative return of the fund vs the S&P 500 Total Return" src="assets/charts/performance-light.png" width="100%">
</picture>

<sub>Updated automatically after every US market close. Time-weighted returns, dividends included; benchmark is the S&P 500 Total Return index (^SP500TR). Data as of 13 Nov 2026.</sub>

## Holdings

| | Ticker | Company | Sector | Weight | Target | Price | Return | P&L |
|--:|:--|:--|:--|--:|--:|--:|--:|--:|
| 1 | **BKNG** | Booking Holdings | Cons. Discretionary | 8.0% | 8% | $159.58 | +0.0% | +$0.00 |
| 2 | **COST** | Costco | Cons. Staples | 8.0% | 8% | $1,106.21 | +0.0% | +$0.00 |
| 3 | **LLY** | Eli Lilly | Health Care | 8.0% | 8% | $1,443.50 | +0.0% | +$0.00 |
| 4 | **NFLX** | Netflix | Comm. Services | 8.0% | 8% | $62.15 | +0.0% | +$0.00 |
| 5 | **VRT** | Vertiv | Industrials | 8.0% | 8% | $202.07 | +0.0% | +$0.00 |
| 6 | **ADBE** | Adobe | Technology | 7.0% | 7% | $243.08 | +0.0% | +$0.00 |
| 7 | **FICO** | Fair Isaac | Technology | 7.0% | 7% | $720.19 | +0.0% | +$0.00 |
| 8 | **ISRG** | Intuitive Surgical | Health Care | 7.0% | 7% | $443.59 | +0.0% | +$0.00 |
| 9 | **NVO** | Novo Nordisk (ADR) | Health Care | 7.0% | 7% | $41.63 | +0.0% | +$0.00 |
| 10 | **PGR** | Progressive | Financials | 7.0% | 7% | $235.78 | +0.0% | +$0.00 |
| 11 | **CEG** | Constellation Energy | Utilities | 5.0% | 5% | $280.20 | +0.0% | +$0.00 |
| 12 | **FCX** | Freeport-McMoRan | Materials | 5.0% | 5% | $59.26 | +0.0% | +$0.00 |
| 13 | **JPM** | JPMorgan Chase | Financials | 5.0% | 5% | $346.19 | +0.0% | +$0.00 |
| 14 | **VST** | Vistra | Utilities | 5.0% | 5% | $133.01 | +0.0% | +$0.00 |
| 15 | **WPC** | W. P. Carey | Real Estate | 5.0% | 5% | $65.67 | +0.0% | +$0.00 |

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
