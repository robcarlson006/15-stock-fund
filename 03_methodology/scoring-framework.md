# Scoring framework: 75 → 25 → 15 → dollar weights → monthly review

Horizon 1 year · benchmark S&P 500 total return · reviewed and reweighted monthly.

Written before any data arrives, so the data can't bend the rules. Change a rule only with a dated note in `journal/decision-log.md`.

Data source: the Bloomberg custom report (9 templates, 10 annual periods), pulled for every company **on the same date**:
Key Stats Multiples, Key Stats Enterprise Value, Key Stats Adj Highlights, Cash Flow Standardized, Ratios Profitability, Ratios Growth, Ratios Credit, Ratios Yield Analysis, Addl CAPEX & Depreciation.

**Plus one price file for all 75** (needed for momentum and correlations): 37 month-end values (3 years + the current month) of the total-return index, one column per ticker. Details in `data/README.md`.

---

## Stage 1: 75 → 25 (screen)

### Step 1. Extract the metrics
From each report, pull these into `analysis/stage1_75_to_25/metrics.csv` (one row per company):

| Pillar | Metric | Better is | Notes |
|---|---|---|---|
| **Quality (30%)** | ROIC, latest year | higher | Banks/insurers: ROE |
| | ROIC, 5-year average | higher | Rewards consistency |
| | Gross profit / total assets | higher | Novy-Marx measure; skip for financials |
| | Operating margin, 5-year trend (slope) | rising | |
| | FCF conversion (FCF / net income, 5-year avg) | higher | Catches earnings that never turn into cash |
| **Value (20%)** | EV/EBITDA now ÷ own 5-year average | lower | Cheap vs its own history |
| | P/E now ÷ own 5-year average | lower | |
| | FCF yield | higher | |
| | Shareholder yield (dividend + net buyback) | higher | |
| **Balance sheet (15%)** | Net debt / EBITDA | lower | Financials: skip; REITs: net debt / EBITDA still applies |
| | Interest coverage (EBIT / interest) | higher | |
| **Growth (15%)** | 3-year revenue CAGR | higher | |
| | 3-year EPS CAGR | higher | |
| | Capex / revenue trend | context only | Flags AI-capex strain (not scored) |
| **Momentum (20%)** | 12-1 month total return (the last 12 months, skipping the most recent month) | higher | 70% of the pillar. Skipping the last month avoids short-term reversal |
| | 6-1 month total return | higher | 30% of the pillar. Picks up turns faster |

Weights total 100%: Quality 30, Value 20, Momentum 20, Balance sheet 15, Growth 15. Value was cut from 30% because cheapness usually takes years to pay off, and the horizon is 1 year; momentum works over 3 to 12 months.

**Momentum crash guard:** momentum can reverse sharply when a falling market rebounds (as after the 5 Nov 2026 tech selloff). The sector and theme caps limit this. If momentum and value disagree strongly on a name (top 20% on one, bottom 20% on the other), flag it for a manual look rather than trusting the blend.

### Step 2. Red-flag filters (fail = out, whatever the score)
- Negative free cash flow in 2 of the last 3 years (except financials, utilities and REITs).
- Net debt / EBITDA above 4.0x (except utilities, REITs and financials; utilities above 6.0x).
- Interest coverage below 3x (except financials, utilities and REITs).
- *Why utilities and REITs are exempt from the FCF and coverage rules (amended 13 Nov 2026):* they fund long-lived assets with debt by design, so negative FCF and ~2x coverage are normal for them. The 6.0x debt limit for utilities still applies.
- EPS fell in 3 of the last 5 years **and** revenue is shrinking.
- An announced acquisition of the company itself (e.g. Dominion): it's a merger-spread trade, not a 3 to 5 year holding.

### Step 3. Score within sector
- Convert each metric to a **percentile rank inside its own sector** (0 to 100). A bank is only compared with banks.
- Pillar score = average of its metric percentiles. Total = weighted pillar scores.
- **Financials (banks, insurers, exchanges, card networks):** Quality = ROE and ROE stability; Value = P/E vs history and P/B relative to ROE; Balance sheet = leverage, plus CET1 for banks if available; Growth as normal.
- **REITs:** Value = P/FFO (or P/AFFO) vs history and dividend yield spread over the 10-year Treasury; Quality = FFO growth and occupancy if available.
- If a metric is missing for a company, average over the metrics that are present and flag it.

**Refinements added 13 Nov 2026 (Stage 1 run):**
- "Own 5-year history" = the **median** of the last five yearly averages, so one freak year (e.g. a COVID-depressed EBITDA) can't distort the baseline.
- No price file was available, so Stage 1 was scored **without momentum**, with the other pillars scaled up proportionally (Quality 37.5%, Value 25%, Balance sheet 18.75%, Growth 18.75%). Momentum comes back at Stage 2.
- A **robustness check** re-runs the selection under six weightings and reports how often each name is picked (`tools/sensitivity_stage1.py`).

### Step 4. Pick 25 with sector balance
1. Take the top 2 per sector (11 sectors = 22 names, fewer if a sector has under 2 survivors).
2. Fill the remaining spots with the highest total scores left in the pool, until there are 25. **Only names in the top half of their own sector qualify for these fill spots** (added 13 Nov 2026), because percentiles in a 3-company sector run 33/67/100 and would otherwise favour weak firms in small sectors.
3. **Theme cap at this stage:** max 7 AI/data-center names, max 3 oil names.
4. Output `analysis/stage1_75_to_25/shortlist_25.md`: the ranked table, every cut name with its reason, and data gaps.

---

## Stage 2: 25 → 15 (deep check)

With the fuller Bloomberg pull for the 25:

1. **Re-score** on the full data (same pillars, and the full Piotroski F-score where data allows).
2. **Qualitative check for each name:** moat, what would break the thesis, upcoming catalysts, management capital allocation. One paragraph each.
3. **Portfolio constraints for the final 15:**
   - At least 7 different sectors, at most 3 names per sector.
   - **At most 4 AI/data-center names** (direct + adjacent, as tagged in the pool report).
   - At most 2 oil-linked names.
   - At most 3 rate-sensitive income names (REITs, regulated utilities).
   - At most 3 non-US ADRs (currency and tax admin).
   - No pair with a 3-year monthly-return correlation above 0.85 (keep the higher-scored one), using the price history pulled for momentum.
4. Output `analysis/stage2_25_to_15/final_15.md` with a thesis and a sell trigger for each name.

### Stage 2 scoring spec (pre-committed 13 Nov 2026, before any Stage 2 result was computed)

Written after checking which rows exist in the Stage 2 files, but before computing any metric, score or ranking. Source of the spec: `analysis/stage2_25_to_15/STAGE2_PROMPT.md`; the data-handling details below were added here.

**No price history, ANR or EEG was pulled (Rob's decision, 13 Nov 2026).** So Stage 2 has no momentum pillar and the 0.85 correlation limit can't be checked. Theme limits stand in for it, and overlapping bets are flagged, not enforced.

**Stage 2 score = 60% Stage 1 score + 40% Stage 2 checks score.**
- Stage 1 score: the `score` column of `analysis/stage1_75_to_25/scores.csv`, unchanged (sector-relative, ranked against the full sector).
- Stage 2 checks: six checks, equal weight. Each metric is a percentile rank (0–100) across the 25 names that have it. A check's score is the average of its metric percentiles. A metric or check that doesn't apply to a company is skipped for it, and its checks score is the average of the checks it has. The number of checks used is recorded.

| # | Check | Metric(s) | Better | Source |
|---|---|---|---|---|
| 1 | Piotroski F-score | 0–9, nine signals below | higher | Stage 2 Bal Sheet, Income GAAP, Liquidity, DuPont; Stage 1 Cash Flow |
| 2 | Earnings quality | (a) 5-year average of \|Adjusted NI ÷ GAAP NI − 1\|; (b) pre-tax SBC ÷ revenue, latest fiscal year | lower | Income GAAP; SBC & Amort |
| 3 | SBC-adjusted FCF yield | Stage 1 FCF yield (latest 12 months) − latest-12-month after-tax SBC ÷ current market cap | higher | Stage 1 Yield Analysis; SBC & Amort |
| 4 | Financial strength | (a) Altman Z (current, else latest fiscal year); (b) current ratio | higher | Ratios Liquidity |
| 5 | Earnings delivery | (a) average EPS surprise % over the last 4 fiscal years; (b) number of those years with a positive surprise | higher | Key Stats Earnings |
| 6 | Forward growth | consensus EPS for the first fiscal year after the last reported one ÷ comparable actual EPS of the last reported year − 1 | higher | Key Stats Earnings |

**Piotroski signals** (latest fiscal year vs the one before; one point each): ROA > 0 (GAAP net income ÷ total assets at the start of the year); operating cash flow > 0; ROA up; operating cash flow > net income; long-term debt ÷ total assets down; current ratio up; diluted weighted shares not up; gross margin up; asset turnover up (Bloomberg revenue ÷ average assets).
- A signal whose inputs Bloomberg doesn't report for a company is skipped (current ratio and gross margin for JPM, PGR and WPC).
- The two cash-flow signals are also skipped for banks (JPM): a bank's operating cash flow is driven by deposits and trading assets, not by earnings quality.
- Score = points ÷ signals used × 9. The signals used are recorded per company.

**Data-handling rules, fixed in advance:**
- Earnings quality (a): each year's gap is capped at 100%. A year with GAAP net income ≤ 0 counts as 100%. Uses the last 5 fiscal years (fewer if the company has fewer).
- CEG has no SBC page: its earnings quality uses (a) only, and check 3 uses the plain FCF yield. Flagged.
- Check 3 is skipped for Financials and Real Estate (JPM, PGR, WPC, EQIX). Reason: these are the two sectors where Stage 1 already replaces FCF-based value metrics (banks have no FCF, an insurer's is inflated by premium float, a REIT's counts property purchases as capex). This is the one place the spec differs from the brief, which was silent on it. The memo reports whether scoring it anyway would change the 15.
- Check 4 is skipped for JPM, PGR and WPC (Bloomberg computes neither metric for them).
- WPC uses the `FFO Per Share` block for checks 5 and 6.
- Check 6 is skipped if the last reported EPS is ≤ 0.
- NVO is in DKK throughout; every metric is a ratio, so currency doesn't matter.
- Ties in Stage 2 score are broken by Stage 1 score.

**Choosing the 15:** walk down the Stage 2 ranking and add each name unless it breaks a limit in step 3 above (3 per sector, 4 AI/data-center, 2 oil, 3 rate-sensitive income, 3 ADRs). A name is also blocked if adding it would leave too few open places to reach 7 sectors. A blocked name is recorded as "blocked by X". The 10 not picked are the bench, in rank order.

**Qualitative overrides** can only exclude a name, never promote one. Each needs a specific written reason and a decision-log entry.

**Robustness:** repeat the selection at 80/20 and 40/60. A name picked at 60/40 but not at both others is "borderline".

**Sizing when a limit binds (Stage 3):** take $1 at a time from the lowest-ranked name in the breaching group (never below $4) and give it to the highest-ranked name outside the group that hasn't yet received a dollar and can take it within every limit. Repeat until no limit is breached.

---

## Stage 3: dollar weights for $100

1. Start every name at **$6.67** (equal weight).
2. Tilt by Stage 2 score rank:
   - Top 5: **$8**
   - Middle 5: **$7**
   - Bottom 5: **$5**
   - That sums to $100 (40 + 35 + 25).
3. Then adjust within these hard limits:
   - Every position between **$4 and $10**.
   - No sector above **$25**.
   - AI/data-center theme no more than **$30** in total.
   - Whole dollars only; total exactly $100.
4. Why not optimize mathematically: with 15 stocks and noisy return forecasts, optimizers chase estimation error. Simple, capped tilts are more robust (see `01_research/how-to-build-a-fund.md`, section 2).

The final allocation goes in `portfolio/target_allocation.csv`. The broker orders are placed by Rob, not by Claude.

---

## Stage 4: monthly review (every month for 1 year)

**Who's watched:** the 15 holdings plus the **bench**, the other 10 names from the 25-name shortlist.

**Data Rob pulls (all 25, one date, first week of the month):** last price, 1-month and 12-month total return, current P/E and EV/EBITDA, FCF yield, consensus EPS estimate for the next 12 months (and how it changed over the month), plus any new quarterly results. A short Bloomberg sheet or Excel export is enough; the full report is only needed when a company has just reported.

**Steps:**
1. **Performance:** fund return vs S&P 500 total return, for the month and since inception. Log it in `journal/monthly/YYYY-MM.md`.
2. **Sell triggers and red flags:** check every holding. Any hit = remove.
3. **Re-score all 25** with the same pillars. Momentum and value update every month; quality, balance-sheet and growth scores only change when new results come out. Momentum will be the main reason ranks move month to month, which is why a swap needs two months in a row.
4. **Swap test:** a holding is replaced when a bench name in a permitted slot (same portfolio limits) beats it by ≥15 points at two reviews in a row. Max 3 swaps per month.
5. **Reweight:** rerun Stage 3 on the updated ranks (top 5 $8, middle 5 $7, bottom 5 $5, all caps apply), scaled to the fund's current value rather than $100.
6. **Orders:** list the trades needed (ticker, buy/sell, dollar amount). Rob places them and logs them in `portfolio/trade_log.csv`.

**Skip small trades:** if a position is within **$0.50** of its target (or 0.5% of fund value once it grows), leave it. This saves needless trades and tax lots.

---

## Caveats
- This is a rules-based educational exercise, not personal investment advice. Claude is not a licensed advisor; the buying decision and the order placement are Rob's.
- Past ratios don't guarantee future returns. The scoring tells you what is cheap and good on paper, not what will go up.
