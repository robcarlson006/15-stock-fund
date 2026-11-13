# Decision log

One dated entry per decision or rule change. Newest at the bottom.

## 2026-11-13: Fund set up
- Fund: $100, 15 stocks, US shares and ADRs only.
- Process: 75-name pool → 25 (Bloomberg 9-template report on one date) → 15 (fuller Bloomberg pull) → capped dollar weights.
- Rules written before any data: `03_methodology/scoring-framework.md`, `02_policy/investment-policy-statement.md`.
- Open: time horizon, benchmark, broker choice.

## 2026-11-13: Horizon, benchmark, review cadence
- Rob chose: horizon **1 year**, benchmark **S&P 500 total return**, **monthly** review with reweighting and add/remove.
- Added Stage 4 (monthly review) to the scoring framework. Bench = the 10 shortlisted names not held. Swap rule: bench name ahead by ≥15 points two months running; max 3 swaps a month; skip trades within $0.50 of target.
- Open: broker choice; whether to add a momentum pillar now that the horizon is 1 year.

## 2026-11-13: Momentum added
- Added a Momentum pillar (20%): 12-1 month return (70%) + 6-1 month return (30%), ranked within sector.
- New weights: Quality 30, Value 20 (from 30), Momentum 20, Balance sheet 15 (from 20), Growth 15. Reason: 1-year horizon; momentum works over 3–12 months, value usually over years.
- Stage 1 now needs a 37-month total-return price file for all 75 (also used for correlations and benchmark tracking).
- Momentum/value conflicts (top 20% on one, bottom 20% on the other) get a manual look.

## 2026-11-13: Stage 1 Bloomberg reports received
- 75 PDFs (PairDrop zip) pulled 13 Nov 2026; renamed by ticker, index in `data/stage1_75_companies/file_index.csv`.
- 74 of 75 pool names covered: **DUK missing**, CTVA pulled twice (duplicate set aside).
- Six foreign names are home listings in local currency (SAP EUR, SONY JPY, TSM TWD, NVO DKK; SHEL, TTE in USD). Ratios are comparable; prices for momentum must use the US ADRs.
- Still needed for Stage 1: DUK report, monthly price file.
- DUK report received (pulled 13 Nov, 06:29). All 75 covered. Still needed: monthly price file.

## 2026-11-13: Stage 1 extraction done
- Parsed all 75 reports (`tools/extract_bloomberg.py`) and computed metrics (`tools/compute_metrics.py`) into `analysis/stage1_75_to_25/metrics.csv`. 79/79 spot-checks matched the PDFs.
- Data-handling rules added: normalised EPS when LTM EPS is >40% off the median of FY + 2 estimates (YUM, MRK, SNPS, NEE, MOS); revenue growth restarts after a >40% one-year drop (GE spin-offs).
- Red flags hit 21 names, including every utility, every oil name, and O/WPC. Decision needed from Rob on whether the FCF/coverage rules should exempt utilities and REITs, and whether the EPS-decline rule should apply to commodity producers. See `analysis/stage1_75_to_25/extraction_notes.md`.

## 2026-11-13: Red-flag rule amended
- Rob approved: utilities and REITs exempt from the "FCF negative 2 of 3 years" and "interest coverage < 3x" red flags (they fund long-lived assets with debt by design). Utility 6x debt limit still applies. Oil EPS-decline rule kept.
- Result: 16 flagged, 59 pass. Energy has no survivors, so the 25 will hold no oil names. NEE fails the 6x utility debt limit.

## 2026-11-13: Stage 1 complete, 25 shortlisted
- Rob has no price file, so Stage 1 was scored without momentum (pillars rescaled proportionally: Q 37.5 / V 25 / BS 18.75 / G 18.75).
- Method refinements (logged in the framework): history baseline = median of 5 yearly averages (BKNG's COVID-era 4,811x EV/EBITDA broke the mean); fill places only from the top half of a sector (small-sector percentile inflation); six-weighting robustness check.
- Parser fix: wrapped labels such as "Price/T12M FFO per Share" now keep their Average rows attached (REIT P/FFO history was previously blank).
- **The 25:** VRT, BKNG, NVO, COST, VST, PGR, FICO, META, LLY, EQIX, CEG, NFLX, ISRG, LIN, ADBE, GE, WPC, FCX, JPM, GOOGL, TJX, YUM, HSY, SYK, JNJ. 16 are picked under all six weightings; GOOGL (2/6) and JNJ (3/6) are borderline. AI/data-center cap (7) is full, which kept out TSM and CAT. No energy.
- Memo: `analysis/stage1_75_to_25/shortlist_25.md`. Next: Stage 2 Bloomberg pull for the 25, including price history.

## 2026-11-13: Stage 2 download list
- Stage 2 request written to `data/stage2_25_companies/DOWNLOAD_LIST.md`: price file (pre-built `prices_monthly.xlsx` with BDH formulas), 6 new FA templates (Bal Sheet Std, Income GAAP, SBC & Amort, Key Stats Earnings, Liquidity, DuPont), ANR, EEG; nice-to-have BICO, DS TA, EVT. Stage 1 templates not re-pulled (same day).

## 2026-11-13: Stage 2 data received and organised
- 25 Financial Analysis PDFs (6 templates, pulled 13 Nov 15:08–15:22) → `data/stage2_25_companies/fa/TICKER_FA.pdf`, index `fa/file_index.csv`, zip archived. All 25 present.
- Parsed to `analysis/stage2_25_to_15/raw_long_stage2.csv` (42,572 numbers; 120/120 spot checks). Parser fixes: section titles only at page tops; DuPont/SBC/Earnings sub-headers. Stage 1 metrics and scores re-verified identical.
- Not pulled (Rob's call): price history, ANR, EEG, BICO. Stage 2 runs without momentum or correlations.
- Brief for the Stage 2/3 session: `analysis/stage2_25_to_15/STAGE2_PROMPT.md`. It proposes Stage 2 score = 60% Stage 1 + 40% six unit-free checks (F-score, earnings quality, SBC-adjusted FCF yield, Altman Z/current ratio, EPS surprise record, forward EPS growth), to be pre-committed in the framework before running.

## 2026-11-13: Stage 2 scoring spec pre-committed (before any result)
- Spec written into `03_methodology/scoring-framework.md` (Stage 2 section) before any Stage 2 metric, score or rank was computed. Only row availability had been checked.
- Stage 2 score = 60% Stage 1 score (unchanged, sector-relative) + 40% six equal-weight checks ranked across the 25: Piotroski F-score, earnings quality, SBC-adjusted FCF yield, financial strength, earnings delivery, forward EPS growth. Robustness at 80/20 and 40/60.
- Runs without momentum or correlations (no price file; Rob's earlier decision). Cluster overlaps are flagged, not enforced.
- **One deviation from the brief, with its data reason:** SBC-adjusted FCF yield is skipped for Financials and Real Estate (JPM, PGR, WPC, EQIX), not only for the bank. The brief was silent on insurers and REITs. Stage 1 already drops FCF-based value metrics for these two sectors (an insurer's FCF is inflated by float, a REIT's treats property purchases as capex). The effect of scoring it anyway will be reported in the memo so Rob can overrule it.
- Details fixed in advance: Piotroski signals skipped where Bloomberg has no inputs (and cash-flow signals for banks), rescaled to 0–9; adjusted-vs-GAAP gap capped at 100% a year; CEG scored without SBC (no page); WPC on FFO per share; the 7-sector rule enforced during the walk; the dollar-shifting rule if a cap binds.

## 2026-11-13: Stage 2 and 3 complete, final 15 and dollar weights
- Scored with `tools/score_stage2.py` exactly as pre-committed. Output: `analysis/stage2_25_to_15/scores_stage2.csv`. Memo: `analysis/stage2_25_to_15/final_15.md`.
- **The 15 (rank order):** VRT, BKNG, COST, LLY, NFLX ($8 each); FICO, NVO, ADBE, ISRG, PGR ($7 each); VST, FCX, WPC, JPM, CEG ($5 each). Total $100, 10 sectors. `portfolio/target_allocation.csv`.
- **No portfolio limit blocked a name:** the top 15 by score all fit. AI/data-center is at its 4-name limit (VRT, VST, FCX, CEG; $23). No sizing cap binds, so no dollars were moved.
- **Bench (rank order):** TJX, HSY, META, GOOGL, LIN, GE, EQIX, SYK, YUM, JNJ. All cut on score. META, GOOGL and EQIX would also hit the AI limit; SYK and JNJ the Health Care limit.
- **Qualitative overrides: none.** Web check on 13 Nov 2026 found no takeover, restatement or large guidance cut among the 25. Noted but not override-grade: FICO withheld fiscal 2027 guidance; Novo's US list-price cuts from Jan 2027; Booking's weak Q4 guide.
- **Robustness:** 13 of 15 kept at 80/20 (LIN, META in; FCX, JPM out) and 13 of 15 at 40/60 (HSY, TJX in; CEG, VST out). Borderline: VST, FCX, JPM, CEG. CEG took the 15th place by 0.11 points over TJX.
- **Effect of the one deviation from the brief** (cash-yield check skipped for PGR, WPC, EQIX): if it were scored, WPC drops to rank 20 and TJX comes in; the other 14 are unchanged. The allocation follows the pre-committed spec (WPC). **Open for Rob to confirm or overrule.**
- **Data gap found when running:** GE's SBC rows stop at 2022, so GE was treated like CEG (no SBC adjustment). GE is rank 21; no effect on the selection.
- **Overlaps flagged, not enforced** (no correlation data): LLY/NVO and CEG/VST are both held. Open for Rob.
- Verified with `tools/check_portfolio.py` (20 of 20 checks, exit 0). Monthly review template added at `journal/monthly/TEMPLATE.md`.
- Still open: Rob's approval of the 15, the WPC/TJX and overlap decisions, the price file (momentum, correlations, monthly tracking), and the broker.

## 2026-11-13: WPC kept, both overlapping pairs kept (Rob delegated the call to the rules)
- Rob asked Claude to settle the two open points. Both were settled by what the written rules say, not by a view on which stock will do better.
- **WPC stays, TJX stays first on the bench.** The cash-yield skip for the insurer and REITs was fixed before any result was computed and matches how Stage 1 already treats those sectors. Reversing it after seeing that it costs TJX a place would be changing a rule to fit the outcome. PGR therefore stays at $7 and NFLX at $8.
- **LLY/NVO and CEG/VST: both names kept in each pair.** The framework's only pair rule is the 0.85 correlation limit, which can't be tested without prices, and the brief says not to invent a substitute. Every limit that can be tested passes (Health Care $22 of $25, AI/data-center $23 of $30, 4 of 4 names).
- **Follow-up fixed now:** when the price file arrives, the 0.85 test is run on all pairs. If a pair fails, the lower-scored name (NVO in LLY/NVO, CEG in CEG/VST) is replaced by the highest-ranked bench name that fits the limits. No change to `portfolio/target_allocation.csv`.
