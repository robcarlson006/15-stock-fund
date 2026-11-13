# Stage 1 extraction notes — 13 Nov 2026

**Source:** 75 Bloomberg "Financial Statement Analysis" PDFs, all pulled 13 Nov 2026 (`data/stage1_75_companies/`).
**Output:**
- `raw_long.csv`: every number in every report, 173,811 rows (file, section, row, year, value).
- `metrics.csv`: one row per company with the Stage 1 metrics and red flags.

**Rebuild:**
```bash
/usr/local/bin/python3 -I tools/extract_bloomberg.py data/stage1_75_companies analysis/stage1_75_to_25/raw_long.csv
/usr/local/bin/python3 -I tools/compute_metrics.py analysis/stage1_75_to_25/raw_long.csv 00_context/candidate_pool_75.csv data/stage1_75_companies/file_index.csv analysis/stage1_75_to_25/metrics.csv
```

## Checks
- **Spot check:** 79 randomly chosen values (ROIC, ROE, EV/EBITDA, net debt/EBITDA, FCF yield, shareholder yield across 14 companies) all appear verbatim on the matching PDF line.
- **Derived numbers:** MSFT 3-year revenue CAGR = (331,839 / 211,915)^(1/3) − 1 = 16.1%, which matches by hand.
- **Blank years** (e.g. CEG before its 2022 spin-off) stay blank. Numbers are placed by page position, so nothing shifts into the wrong year.

## What the reports contain
- **History:** 7 fiscal years (FY2019/20 to FY2025/26, depending on year-end), plus the latest 12 months ("LTM") and 2 estimate years. That's not the 10 years requested, but enough for every 3- and 5-year metric.
- **Templates by industry:** Bloomberg used different layouts for banks (JPM, WFC, GS), insurers (PGR, CB) and REITs (O, WPC, PLD). These have no EBITDA, FCF or ROIC. Per the framework, they are scored on ROE, P/E, P/Book, P/FFO, Tier 1 capital and combined ratio instead.
- **Total assets** aren't in the 9 templates. They're backed out as net income ÷ ROA (or total debt ÷ debt/assets), and used only for gross profit/assets.

## Adjustments made (rules, applied to all 75)
1. **Distorted 12-month EPS:** if LTM EPS is more than 40% away from the median of (last fiscal-year EPS, next two estimates), the P/E uses that median instead. It applied to 5 names:

| Ticker | LTM EPS | Used | Why it looks one-off |
|---|---|---|---|
| YUM | 1.53 | 6.42 | FY2025 was 5.95; estimates 6.42 / 6.72 |
| MRK | 2.34 | 8.04 | Acquisition R&D charge; FY2025 8.04, 2027 estimate 9.03 |
| SNPS | 2.98 | 15.16 | Ansys deal charges; estimates 15.16 / 18.70 |
| NEE | 5.76 | 4.03 | LTM boosted vs FY2025 2.94 and estimates ~4.0 to 4.4 |
| MOS | −1.51 | 1.04 | Loss-making; P/E vs history not meaningful, left blank |

2. **Spin-off break:** if revenue drops more than 40% in one year, growth is measured from after the drop. Only **GE** is affected (GE HealthCare and Vernova spun off). 3-year revenue CAGR is +13.9% from 2023, not −15.7%.

## Data gaps (scored on the metrics present)
- **ROE blank, negative equity:** FICO, YUM, SBUX, BKNG. Buybacks have made book equity negative, so ROE isn't meaningful. ROIC is still there.
- **No gross profit line:** UNP, TTE, COP, BKNG, plus all financials and REITs.
- **No interest-coverage rows:** ISRG (no debt) and VRT (has $3.3B debt, but Bloomberg left the rows blank).
- **No shareholder yield:** ETN (latest 12-month row is blank).
- **No 3-year EPS growth:** CEG (EPS was negative in the base year).
- **Foreign listings:** SAP, SONY, TSM, NVO are reported in EUR, JPY, TWD, DKK. Ratios are unaffected.

## Update 13 Nov 2026: utilities and REITs exempted
Rob agreed to exempt utilities and REITs from the FCF and interest-coverage rules. The oil EPS rule stays. Result: **16 names flagged, 59 pass.**
- Still out: SNPS, NXPI, NKE, CPB, CLX, ODFL, NUE, EMN, MOS, all 5 oil names, NEE (7.0x debt > 6x utility limit), D (debt + being acquired).
- Back in: CEG, VST, DUK, SO, O, WPC.
- Survivors by sector: Health Care 10, Financials 9, Technology 7, Industrials 7, Cons. Discretionary 6, Comm. Services 5, Cons. Staples 4, Real Estate 4, Utilities 4, Materials 3, **Energy 0**.

## Red flags under the original rules (21 names, superseded)
| Rule | Names |
|---|---|
| EPS fell 3 of last 5 years + revenue shrinking | NXPI, NKE, ODFL, NUE, EMN, **all 5 oil names** (XOM, CVX, SHEL, TTE, COP) |
| Net debt/EBITDA too high | CPB 5.1x, CLX 4.1x, MOS 10.4x; NEE 7.0x, D 7.4x (utility limit 6x) |
| Interest coverage < 3x | SNPS 2.0x, CPB 2.6x, O 1.9x, WPC 2.7x, NEE 1.8x, VST 1.6x, D 2.2x, DUK 2.4x, SO 2.2x |
| FCF negative 2 of last 3 years | NEE, CEG, D, DUK, SO |
| Being acquired | D |

## Issues for Rob to decide before scoring
1. **All 6 utilities fail.** Regulated utilities borrow to fund their building programmes. That makes negative free cash flow and roughly 2x interest coverage normal for them. The framework already exempts utilities from the 4x debt rule (6x instead) but not from the FCF and coverage rules. Applied literally, the sector is wiped out.
2. **All 5 oil names fail the EPS rule.** That's because 2022 was a record year and EPS has fallen since. On LTM numbers, though, oil earnings are rising again with Brent near $96. The rule works as written, but it removes the whole sector.
3. **Both net-lease REITs (O, WPC) fail interest coverage.** Low coverage is typical for net-lease REITs.

If these stand, Stage 1 has no utilities and no energy names, and only PLD and EQIX left in real estate. The "top 2 per sector" step would then pick from fewer than 11 sectors.

## Still missing
- **Momentum:** the monthly price file (37 month-ends, total-return index, US tickers for the ADRs) isn't in yet. `ret_12_1m` and `ret_6_1m` are blank.
