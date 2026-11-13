# Stage 2 data notes — 13 Nov 2026

**Source:** 25 Bloomberg "Financial Statement Analysis" PDFs, pulled 13 Nov 2026 15:08–15:22. They're in `data/stage2_25_companies/fa/` (`TICKER_FA.pdf`), indexed in `fa/file_index.csv`. The original zip is in `_original_zip/`.
**Parsed into:** `raw_long_stage2.csv`, 42,572 numbers in the same long format as Stage 1. Spot check: 120 of 120 random values found on the matching PDF line.

**Rebuild:**
```bash
/usr/local/bin/python3 -I tools/extract_bloomberg.py data/stage2_25_companies/fa analysis/stage2_25_to_15/raw_long_stage2.csv
```

## What's in each report (6 templates, up to 10 fiscal years, usually FY2017–FY2025 + LTM + estimates)
| Section in CSV | Bloomberg template | Useful rows |
|---|---|---|
| `Standardized` | Bal Sheet – Standardized | Total Assets, Total Current Assets/Liabilities, Goodwill, LT Debt, Total Equity, Shares Outstanding |
| `GAAP` | Income – GAAP | Revenue, Gross Profit, Operating Income, Net Income GAAP vs `Net Income Avail to Common, Adj`, Diluted EPS GAAP vs Adjusted, Diluted Weighted Avg Shares |
| `SBC & Amort` | Income – SBC & Amort | sub `Stock Based Compensation` → Pre-Tax/After-Tax SBC; sub `Earnings Per Share Reconciliation` → EPS ex-SBC; amortisation blocks |
| `Earnings` | Key Stats – Earnings | sub = block (`Revenue`, `Earnings Per Share`, `EBIT`, `EBITDA`, `Gross Margin %`, `Pretax Income (Loss)`, `Net Income`, `FFO Per Share` for WPC). Rows: Consensus Estimate, Comparable Actual, Surprise %, GAAP Actual, Adjusted Actual. Annual columns are fiscal-year surprises; estimate columns are consensus for coming years |
| `Liquidity` | Ratios – Liquidity | Current Ratio, Quick Ratio, Cash Ratio, CFO/Avg Current Liab, CFO/CapEx, **Altman's Z-Score**, debt/asset ratios |
| `DuPont Analysis` | Ratios – DuPont | sub = component: Tax Burden, Adjustment Factor, Interest Burden, Operating Margin, Asset Turnover, Leverage Ratio; Adjusted ROE, 5-yr avg ROE, Payout, Sustainable Growth |

## Expected gaps
- **JPM, PGR, WPC:** no Current Ratio, Altman Z or gross profit. Bloomberg doesn't compute these for banks, insurers and REITs.
- **NVO:** gross profit is labelled `Gross Profit + Other Operating`. Reports are in DKK.
- **YUM:** no DuPont ROE (negative equity).
- **CEG:** no SBC & Amort page. CEG has 6 fiscal years (spun off 2022).
- **Not pulled:**
  - Price history, so no momentum, return correlations or benchmark tracking.
  - ANR, EEG, BICO, transcripts.

## Parser changes made for Stage 2 (Stage 1 metrics and scores re-verified identical)
- Section titles are only recognised at the top of a page. Wrapped labels like "+ Tax Allowance/**Credit**" were being read as a new section.
- New sub-headers were added for the DuPont components, the SBC page blocks, and the Earnings-page blocks (the latter only inside the Earnings section).
