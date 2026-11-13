# Stage 1 shortlist: 75 → 25

**Fund:** My own investment fund ($100, 15 stocks, 1-year horizon, benchmark S&P 500 total return)  
**Data:** Bloomberg Financial Statement Analysis, all 75 pulled 13 Nov 2026  
**Method:** `03_methodology/scoring-framework.md`, Stage 1 (amendments in `journal/decision-log.md`)  
**Status:** for Rob's review. Rules-based output, not personal investment advice.

## Summary

- **59 of 75 passed the red-flag checks**, and the 25 below were selected from them, covering 10 sectors. Energy is absent: all five oil names failed the falling-earnings check.
- **The shortlist is robust:** 16 of the 25 are selected under all six weightings tested, and 23 under at least four. Borderline: GOOGL (2/6), JNJ (3/6).
- **AI/data-center exposure is at its cap of 7** (VRT, VST, META, CEG, EQIX, FCX, GOOGL). TSMC and Caterpillar scored high enough to be included but were blocked by that cap.
- **Momentum is not scored.** No price file was pulled, so the other four pillars were scaled up proportionally (Quality 37.5%, Value 25%, Balance sheet 18.75%, Growth 18.75%). Price history should be pulled at Stage 2.

## The 25

Pillar scores are percentiles within the company's own sector (100 = best in sector). "Stable" counts how many of the six weight sets also select the name.

| # | Ticker | Company | Sector | Theme | Quality | Value | Bal. sheet | Growth | **Score** | Stable | Why in | Key numbers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **VRT** | Vertiv | Industrials | AI direct | 94 | 65 | 100 | 100 | **89.1** | 6/6 | Top 2 in Industrials | ROIC 26.9%, EV/EBITDA 1.16× own history, FCF yield 3.9%, net debt/EBITDA -0.1x, rev growth 21.6%/yr |
| 2 | **BKNG** | Booking Holdings | Cons. Discretionary |  | 92 | 96 | 67 | 92 | **88.0** | 6/6 | Top 2 in Cons. Discretionary | ROIC 61.5%, EV/EBITDA 0.60× own history, FCF yield 7.4%, net debt/EBITDA 0.4x, rev growth 16.3%/yr |
| 3 | **NVO** | Novo Nordisk (ADR) | Health Care |  | 78 | 98 | 95 | 85 | **87.4** | 6/6 | Top 2 in Health Care | ROIC 34.8%, EV/EBITDA 0.28× own history, FCF yield 5.8%, net debt/EBITDA 0.5x, rev growth 20.4%/yr |
| 4 | **COST** | Costco | Cons. Staples |  | 90 | 50 | 100 | 100 | **83.8** | 6/6 | Top 2 in Cons. Staples | ROIC 20.8%, EV/EBITDA 1.10× own history, FCF yield 1.9%, net debt/EBITDA -0.7x, rev growth 7.8%/yr |
| 5 | **VST** | Vistra | Utilities | AI direct | 90 | 81 | 50 | 100 | **82.2** | 6/6 | Top 2 in Utilities | ROIC 12.9%, EV/EBITDA 0.81× own history, FCF yield 5.8%, net debt/EBITDA 2.5x, rev growth 8.9%/yr |
| 6 | **PGR** | Progressive | Financials |  | 59 | 93 | 78 | 100 | **78.7** | 6/6 | Top 2 in Financials | ROE 33.2%, P/E 12.3x (0.38× own history), P/B 4.0x, rev growth 19.1%/yr |
| 7 | **FICO** | Fair Isaac | Technology |  | 94 | 89 | 14 | 86 | **76.4** | 6/6 | Top 2 in Technology | ROIC 69.4%, EV/EBITDA 0.44× own history, FCF yield 6.6%, net debt/EBITDA 3.9x, rev growth 18.8%/yr |
| 8 | **META** | Meta Platforms | Comm. Services | AI direct | 80 | 60 | 70 | 90 | **75.0** | 6/6 | Top 2 in Comm. Services | ROIC 24.0%, EV/EBITDA 0.83× own history, FCF yield 1.8%, net debt/EBITDA 0.3x, rev growth 19.9%/yr |
| 9 | **LLY** | Eli Lilly | Health Care |  | 78 | 42 | 79 | 100 | **73.5** | 6/6 | Top 2 in Health Care | ROIC 33.3%, EV/EBITDA 0.71× own history, FCF yield 1.5%, net debt/EBITDA 1.2x, rev growth 31.7%/yr |
| 10 | **CEG** | Constellation Energy | Utilities | AI direct | 70 | 75 | 100 | 50 | **73.1** | 5/6 | Top 2 in Utilities | ROIC 11.2%, EV/EBITDA 0.95× own history, FCF yield 1.3%, net debt/EBITDA 2.4x, rev growth 1.5%/yr |
| 11 | **NFLX** | Netflix | Comm. Services |  | 72 | 85 | 40 | 90 | **72.6** | 6/6 | Top 2 in Comm. Services | ROIC 29.1%, EV/EBITDA 0.43× own history, FCF yield 4.3%, net debt/EBITDA 0.6x, rev growth 12.6%/yr |
| 12 | **ISRG** | Intuitive Surgical | Health Care |  | 54 | 68 | 100 | 85 | **71.8** | 6/6 | Best remaining score (top half of sector) | ROIC 16.1%, EV/EBITDA 0.71× own history, FCF yield 2.3%, net debt/EBITDA -1.0x, rev growth 17.4%/yr |
| 13 | **LIN** | Linde | Materials |  | 80 | 67 | 67 | 67 | **71.7** | 6/6 | Top 2 in Materials | ROIC 10.3%, EV/EBITDA 1.06× own history, FCF yield 2.1%, net debt/EBITDA 1.8x, rev growth 0.6%/yr |
| 14 | **EQIX** | Equinix | Real Estate | AI adjacent | 75 | 38 | 100 | 75 | **70.3** | 5/6 | Top 2 in Real Estate | ROIC 5.3%, EV/EBITDA 1.02× own history, FCF yield -2.7%, net debt/EBITDA 4.9x, rev growth 8.3%/yr |
| 15 | **ADBE** | Adobe | Technology |  | 69 | 96 | 71 | 36 | **69.9** | 6/6 | Top 2 in Technology | ROIC 38.8%, EV/EBITDA 0.32× own history, FCF yield 10.9%, net debt/EBITDA 0.1x, rev growth 10.5%/yr |
| 16 | **GE** | GE Aerospace | Industrials |  | 61 | 75 | 69 | 79 | **69.3** | 6/6 | Top 2 in Industrials | ROIC 16.0%, EV/EBITDA 0.84× own history, FCF yield 2.3%, net debt/EBITDA 0.9x, rev growth 13.9%/yr |
| 17 | **WPC** | W. P. Carey | Real Estate |  | 83 | 100 | 38 | 25 | **68.0** | 4/6 | Top 2 in Real Estate | ROIC 4.7%, P/FFO 0.83× own history, FCF yield -5.2%, net debt/EBITDA 6.3x, rev growth 5.1%/yr |
| 18 | **FCX** | Freeport-McMoRan | Materials | AI adjacent | 67 | 58 | 83 | 67 | **67.7** | 5/6 | Top 2 in Materials | ROIC 12.5%, EV/EBITDA 1.35× own history, FCF yield 2.3%, net debt/EBITDA 0.5x, rev growth 4.4%/yr |
| 19 | **JPM** | JPMorgan Chase | Financials |  | 67 | 37 | 94 | 67 | **64.5** | 5/6 | Top 2 in Financials | ROE 18.7%, P/E 14.2x (1.16× own history), P/B 2.6x, rev growth 12.1%/yr |
| 20 | **GOOGL** | Alphabet | Comm. Services | AI direct | 64 | 40 | 100 | 60 | **64.0** | 2/6 | Best remaining score (top half of sector) | ROIC 20.4%, EV/EBITDA 0.99× own history, FCF yield 0.6%, net debt/EBITDA -0.6x, rev growth 12.5%/yr |
| 21 | **TJX** | TJX Companies | Cons. Discretionary |  | 59 | 50 | 88 | 67 | **63.7** | 6/6 | Top 2 in Cons. Discretionary | ROIC 25.0%, EV/EBITDA 1.14× own history, FCF yield 3.9%, net debt/EBITDA 0.9x, rev growth 6.5%/yr |
| 22 | **YUM** | Yum Brands | Cons. Discretionary |  | 80 | 71 | 33 | 50 | **63.3** | 4/6 | Best remaining score (top half of sector) | ROIC 73.0%, EV/EBITDA 0.58× own history, FCF yield 3.7%, net debt/EBITDA 2.1x, rev growth 6.3%/yr |
| 23 | **HSY** | Hershey | Cons. Staples |  | 65 | 94 | 50 | 25 | **61.9** | 5/6 | Top 2 in Cons. Staples | ROIC 17.6%, EV/EBITDA 0.69× own history, FCF yield 6.1%, net debt/EBITDA 1.5x, rev growth 3.9%/yr |
| 24 | **SYK** | Stryker | Health Care |  | 62 | 68 | 42 | 65 | **60.1** | 6/6 | Best remaining score (top half of sector) | ROIC 9.8%, EV/EBITDA 0.65× own history, FCF yield 3.8%, net debt/EBITDA 1.8x, rev growth 10.8%/yr |
| 25 | **JNJ** | Johnson & Johnson | Health Care |  | 62 | 30 | 79 | 55 | **55.9** | 3/6 | Best remaining score (top half of sector) | ROIC 17.1%, EV/EBITDA 1.45× own history, FCF yield 3.0%, net debt/EBITDA 0.8x, rev growth 5.6%/yr |

## Shape of the 25

| Sector | Names |
|---|---|
| Health Care | 5 |
| Comm. Services | 3 |
| Cons. Discretionary | 3 |
| Cons. Staples | 2 |
| Financials | 2 |
| Industrials | 2 |
| Materials | 2 |
| Real Estate | 2 |
| Technology | 2 |
| Utilities | 2 |

- **Themes:** AI/data-center 7 (direct: VRT, VST, META, CEG, GOOGL; adjacent: EQIX, FCX). Oil 0.
- **Non-US listings:** NVO (buy as the US ADR).
- **Rate-sensitive income names:** WPC, EQIX (REITs); CEG and VST are merchant power producers rather than regulated utilities.
- **Clusters to manage at Stage 2:**
  - CEG, VST, VRT, META and GOOGL all depend on data-center demand.
  - LLY and NVO are both GLP-1 obesity-drug bets.
  - TJX and COST both depend on consumers trading down to value.

## Borderline names and alternates

Names whose place depends on the weighting, and the first names that would replace them:

| In the 25, but borderline | Stable | Score |
|---|---|---|
| GOOGL | 2/6 | 64.0 |
| JNJ | 3/6 | 55.9 |

| First alternates (not in the 25) | Picked under | Score | Note |
|---|---|---|---|
| PLD | 3/6 weightings | 65.6 | bottom half of sector |
| AMZN | 2/6 weightings | 56.5 | bottom half of sector |
| GS | 2/6 weightings | 55.0 |  |
| CAT | 1/6 weightings | 61.9 | blocked by AI cap |
| CTVA | 1/6 weightings | 60.6 | bottom half of sector |
| DUK | 1/6 weightings | 50.5 | bottom half of sector |
| SAP | 1/6 weightings | 54.5 | bottom half of sector |
| SPGI | 1/6 weightings | 53.2 |  |

## Every cut name and why

### Failed a red-flag check (16)

| Ticker | Sector | Reason |
|---|---|---|
| SNPS | Technology | Interest coverage 2.0x < 3x |
| NXPI | Technology | EPS fell in 3 of last 5 years and revenue shrinking |
| NKE | Cons. Discretionary | EPS fell in 3 of last 5 years and revenue shrinking |
| CPB | Cons. Staples | Net debt/EBITDA 5.1x > 4.0x; Interest coverage 2.6x < 3x |
| CLX | Cons. Staples | Net debt/EBITDA 4.1x > 4.0x |
| ODFL | Industrials | EPS fell in 3 of last 5 years and revenue shrinking |
| NUE | Materials | EPS fell in 3 of last 5 years and revenue shrinking |
| EMN | Materials | EPS fell in 3 of last 5 years and revenue shrinking |
| MOS | Materials | Net debt/EBITDA 10.4x > 4.0x |
| XOM | Energy | EPS fell in 3 of last 5 years and revenue shrinking |
| CVX | Energy | EPS fell in 3 of last 5 years and revenue shrinking |
| SHEL | Energy | EPS fell in 3 of last 5 years and revenue shrinking |
| TTE | Energy | EPS fell in 3 of last 5 years and revenue shrinking |
| COP | Energy | EPS fell in 3 of last 5 years and revenue shrinking |
| NEE | Utilities | Net debt/EBITDA 7.0x > 6.0x (utility limit) |
| D | Utilities | Net debt/EBITDA 7.4x > 6.0x (utility limit); Being acquired by NextEra (merger-spread trade, not a 1-year holding) |

### Passed the checks, not selected (34)

| Ticker | Sector | Score | Rank in sector | Reason |
|---|---|---|---|---|
| PLD | Real Estate | 65.6 | 3 of 4 | Bottom half of its sector |
| TSM | Technology | 62.1 | 3 of 7 | Would qualify, but the AI/data-center cap (7) was already full |
| CAT | Industrials | 61.9 | 3 of 7 | Would qualify, but the AI/data-center cap (7) was already full |
| CTVA | Materials | 60.6 | 3 of 3 | Bottom half of its sector |
| AMZN | Cons. Discretionary | 56.5 | 4 of 6 | Bottom half of its sector |
| WMT | Cons. Staples | 56.1 | 3 of 4 | Bottom half of its sector |
| MSFT | Technology | 55.0 | 4 of 7 | Top half of sector, but outscored for the last open places |
| GS | Financials | 55.0 | 3 of 9 | Top half of sector, but outscored for the last open places |
| SAP | Technology | 54.5 | 5 of 7 | Bottom half of its sector |
| UNH | Health Care | 53.9 | 6 of 10 | Bottom half of its sector |
| SPGI | Financials | 53.2 | 4 of 9 | Top half of sector, but outscored for the last open places |
| SONY | Comm. Services | 52.6 | 4 of 5 | Bottom half of its sector |
| ETN | Industrials | 51.9 | 4 of 7 | Top half of sector, but outscored for the last open places |
| CME | Financials | 51.6 | 5 of 9 | Top half of sector, but outscored for the last open places |
| MA | Financials | 50.7 | 6 of 9 | Bottom half of its sector |
| DUK | Utilities | 50.5 | 3 of 4 | Bottom half of its sector |
| PWR | Industrials | 49.4 | 5 of 7 | Bottom half of its sector |
| HD | Cons. Discretionary | 49.4 | 5 of 6 | Bottom half of its sector |
| CB | Financials | 49.1 | 7 of 9 | Bottom half of its sector |
| WFC | Financials | 48.8 | 8 of 9 | Bottom half of its sector |
| V | Financials | 48.4 | 9 of 9 | Bottom half of its sector |
| AVGO | Technology | 48.3 | 6 of 7 | Bottom half of its sector |
| MDLZ | Cons. Staples | 48.3 | 4 of 4 | Bottom half of its sector |
| MRK | Health Care | 46.5 | 7 of 10 | Bottom half of its sector |
| O | Real Estate | 46.1 | 4 of 4 | Bottom half of its sector |
| SO | Utilities | 44.2 | 4 of 4 | Bottom half of its sector |
| UNP | Industrials | 42.3 | 6 of 7 | Bottom half of its sector |
| ABT | Health Care | 42.0 | 8 of 10 | Bottom half of its sector |
| RTX | Industrials | 40.1 | 7 of 7 | Bottom half of its sector |
| VZ | Comm. Services | 35.8 | 5 of 5 | Bottom half of its sector |
| DHR | Health Care | 34.4 | 9 of 10 | Bottom half of its sector |
| TXN | Technology | 33.8 | 7 of 7 | Bottom half of its sector |
| SBUX | Cons. Discretionary | 32.2 | 6 of 6 | Bottom half of its sector |
| TMO | Health Care | 29.2 | 10 of 10 | Bottom half of its sector |

## How the scoring worked

1. **Checks:** red-flag rules removed 16 names. Utilities and REITs are exempt from the FCF and interest-coverage rules (agreed 13 Nov).
2. **Within-sector percentiles:** each metric was ranked only against the company's sector peers, so a bank is never compared with a software firm.
3. **Pillars:**
   - Quality: ROIC, gross profit/assets, margin trend, FCF conversion.
   - Value: EV/EBITDA and P/E vs the company's own 5-year history, FCF yield, shareholder yield.
   - Balance sheet: net debt/EBITDA, interest coverage.
   - Growth: 3-year revenue and EPS growth.
   - Financials use ROE level and stability, P/E vs history, P/B relative to ROE, and capital strength.
   - REITs use P/FFO vs history.
4. **Selection:** the top 2 in each sector, then the best remaining scores from the top half of their sector, with at most 7 AI/data-center names.
5. **Robustness:** re-run under six weightings (base, equal, quality-heavy, value-heavy, growth-heavy, and the original pre-momentum weights).

**Data adjustments** (details in `extraction_notes.md`):
- The history baseline is the median of five yearly averages, so a freak year like Booking's 2021 COVID multiple can't distort it.
- Normalised EPS was used where the latest 12 months contain a one-off (YUM, MRK, SNPS, NEE, MOS).
- GE's revenue growth is measured after its spin-offs.

## Caveats

- **Backward-looking:** Stage 1 uses reported accounts and multiples, with no view yet on moats, catalysts or management. That is Stage 2's job.
- **One date:** valuations are as of 13 Nov 2026 and will move.
- **No momentum:** for a 1-year horizon, that is the largest gap in this screen.

## What to pull for Stage 2 (the 25 names)

1. **Price history:** 3 years of month-end total-return prices for the 25, plus SPX, in one sheet. Bloomberg `HP` per name, or Excel `BDH("<ticker> US Equity","TOT_RETURN_INDEX_GROSS_DVDS",start,end,"Per=M")`. This gives momentum, correlations and the benchmark comparison.
2. **Templates not pulled yet:** Bal Sheet – Standardized, Income – GAAP, Ratios – DuPont, Key Stats – Earnings (estimates and surprises).
3. **Analyst view:** `ANR` (consensus rating and target) and `EE` (estimate revisions over the last 3 months) for each name.
4. **Latest guidance:** the most recent earnings release or call summary for each name.
