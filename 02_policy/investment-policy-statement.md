# Investment Policy Statement — draft

Owner: Rob · Drafted 13 Nov 2026 · Status: **agreed 13 Nov 2026**

## 1. Objective
Run a real, small ($100) concentrated equity fund to learn portfolio management end to end: research, selection, sizing, monitoring and review. Secondary goal: beat the benchmark over the horizon after costs.

## 2. Capital and horizon
- Starting capital: **$100 USD**.
- Time horizon: **1 year** from the first purchase date, then a full review of whether to continue.
- Additional contributions: none planned.

## 3. Benchmark
**S&P 500, total return (dividends reinvested), in USD.** SPY's total return is the practical proxy. The fund's return is measured monthly and since inception, after all fees.

## 4. Universe
- The 75-name pool in `00_context/candidate_pool_75.csv`. Names may be swapped in with a logged reason.
- US-listed shares and US-listed ADRs only. No non-US funds or ETFs (PFIC risk for a US taxpayer).
- No leverage, options, short selling or margin.

## 5. Construction rules
- Exactly 15 holdings.
- Each position $4 to $10 at purchase. Sector cap $25. AI/data-center theme cap $30.
- At least 7 sectors. Max 2 oil-linked, max 3 rate-sensitive income, max 3 ADRs.
- Selection follows `03_methodology/scoring-framework.md`.

## 6. Monthly review and reweighting
- **One review per month**, in the first week, using data pulled on one date. The process is in `03_methodology/scoring-framework.md`, Stage 4.
- Each review: re-score the 15 holdings and the 10-name bench, decide any swaps, then reset every position to its new target weight.
- **Maximum 3 swaps per month**, so the fund stays a portfolio and not a trading account.
- No trading between reviews unless a sell trigger fires.

## 7. Adding and removing stocks
**Remove** a holding when any of these is true:
- Its written sell trigger fires (thesis broken).
- It fails a red-flag filter.
- It is being acquired.
- A bench name outscores it by **15 or more points** (out of 100) at two reviews in a row. The two-month rule stops one noisy month from causing a trade.

**Add** only from the bench (the 25-name shortlist minus current holdings). A name from outside the 25 needs a full Stage 2 check first.

Not a reason to sell: the price fell and nothing else changed.

## 8. Records
- Every trade in `portfolio/trade_log.csv`: date, ticker, side, quantity, price, fees, USD/GBP rate (needed for UK and US tax).
- Every decision and rule change in `journal/decision-log.md`.

## 9. Costs and broker
- $0-commission broker with fractional shares covering every holding (incl. ADRs). Check eligibility for a US citizen with a UK address.
- Track currency-conversion costs if funding in GBP.
- Monthly reweighting means many small trades. Holding under a year makes every gain short-term for US tax (taxed as ordinary income) and a disposal for UK CGT. At $100 the amounts are tiny, but log every trade.

## 10. Review of this policy
At the 1-year mark, or after any big change in circumstances. Signed off by Rob.
