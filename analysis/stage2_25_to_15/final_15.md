# Final 15 and dollar weights: investment committee memo

**Fund:** My own investment fund ($100, 15 stocks, 1-year horizon, benchmark S&P 500 total return, monthly review)  
**Data:** Bloomberg Financial Statement Analysis. Stage 1 (75 names) and Stage 2 (25 names) both pulled 13 Nov 2026  
**Method:** `03_methodology/scoring-framework.md`, Stages 2 and 3. The Stage 2 scoring spec was written into the framework before any result was computed (decision log, 13 Nov 2026)  
**Status:** for Rob's approval. This is the output of the written rules, not personal investment advice. Rob places every trade himself.

## Summary

- **The 15:** VRT, BKNG, COST, LLY, NFLX, FICO, NVO, ADBE, ISRG, PGR, VST, FCX, WPC, JPM, CEG. They cover 10 sectors. No portfolio limit blocked any name: the top 15 by Stage 2 score all fit.
- **Dollars:** $8 each for the top 5 (VRT, BKNG, COST, LLY, NFLX), $7 for the middle 5 (FICO, NVO, ADBE, ISRG, PGR), $5 for the bottom 5 (VST, FCX, WPC, JPM, CEG). No cap binds, so no dollars were moved. Total $100.
- **The last place was close.** CEG (62.32) beat TJX (62.21) and HSY (62.03) by less than half a point.
- **Robustness:** 13 of 15 survive an 80/20 split and 13 of 15 survive 40/60. Borderline: VST, FCX, JPM, CEG. The other 11 are picked under all three splits.
- **One scoring choice changes one name.** The spec skips the cash-yield check for REITs and the insurer. If it were scored for them, WPC would drop out and TJX would come in. See 'Decisions for Rob'.
- **No qualitative overrides.** The news check found no takeover of any of the 25, no restatement and no large guidance cut.
- **Two overlapping bets are both in the 15:** LLY with NVO (GLP-1 drugs) and CEG with VST (power for data centers). These are flagged for Rob, not enforced, because the correlation limit can't be checked without price data.
- **Not scored:** momentum and correlations (no price file). For a 1-year horizon that is the biggest gap in this work.

## The 15

Scores are out of 100. Stage 2 score = 60% Stage 1 score + 40% Stage 2 checks.

| # | Ticker | Company | Sector | Theme | $ | Stage 1 | Checks | **Stage 2** | Key numbers |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **VRT** | Vertiv | Industrials | AI direct | **$8** | 89.1 | 66.1 | **79.9** | ROIC 26.9%, P/E 38.3x (0.45x own history), FCF yield after stock pay 3.9%, Piotroski 6.0/9, EPS beats 3/4, consensus EPS growth +69% |
| 2 | **BKNG** | Booking Holdings | Cons. Discretionary |  | **$8** | 88.0 | 62.6 | **77.9** | ROIC 61.5%, P/E 15.1x (0.50x own history), FCF yield after stock pay 7.0%, Piotroski 6.8/9, EPS beats 4/4, consensus EPS growth +15% |
| 3 | **COST** | Costco | Cons. Staples |  | **$8** | 83.8 | 55.6 | **72.5** | ROIC 20.8%, P/E 52.6x (1.10x own history), FCF yield after stock pay 1.8%, Piotroski 7.0/9, EPS beats 3/4, consensus EPS growth +10% |
| 4 | **LLY** | Eli Lilly | Health Care |  | **$8** | 73.5 | 66.4 | **70.7** | ROIC 33.3%, P/E 36.4x (0.67x own history), FCF yield after stock pay 1.5%, Piotroski 8.0/9, EPS beats 4/4, consensus EPS growth +46% |
| 5 | **NFLX** | Netflix | Comm. Services |  | **$8** | 72.6 | 65.9 | **69.9** | ROIC 29.1%, P/E 18.2x (0.33x own history), FCF yield after stock pay 4.2%, Piotroski 7.0/9, EPS beats 2/4, consensus EPS growth +42% |
| 6 | **FICO** | Fair Isaac | Technology |  | **$7** | 76.4 | 57.0 | **68.7** | ROIC 69.4%, P/E 19.4x (0.36x own history), FCF yield after stock pay 5.7%, Piotroski 8.0/9, EPS beats 3/4, consensus EPS growth +3% |
| 7 | **NVO** | Novo Nordisk (ADR) | Health Care | ADR | **$7** | 87.4 | 39.8 | **68.3** | ROIC 34.8%, P/E 10.8x (0.29x own history), FCF yield after stock pay 5.6%, Piotroski 5.0/9, EPS beats 2/4, consensus EPS growth -1% |
| 8 | **ADBE** | Adobe | Technology |  | **$7** | 69.9 | 64.5 | **67.7** | ROIC 38.8%, P/E 13.1x (0.30x own history), FCF yield after stock pay 8.8%, Piotroski 7.0/9, EPS beats 4/4, consensus EPS growth +17% |
| 9 | **ISRG** | Intuitive Surgical | Health Care |  | **$7** | 71.8 | 59.4 | **66.8** | ROIC 16.1%, P/E 46.9x (0.59x own history), FCF yield after stock pay 1.9%, Piotroski 6.0/9, EPS beats 3/4, consensus EPS growth +26% |
| 10 | **PGR** | Progressive | Financials |  | **$7** | 78.7 | 48.2 | **66.5** | ROE 33.2%, P/E 12.3x (0.38x own history), Piotroski 6.4/9, EPS beats 3/4, consensus EPS growth +0% |
| 11 | **VST** † | Vistra | Utilities | AI direct | **$5** | 82.2 | 41.3 | **65.8** | ROIC 12.9%, P/E 19.3x (0.76x own history), FCF yield after stock pay 5.5%, Piotroski 5.0/9, EPS beats 1/4, consensus EPS growth +282% |
| 12 | **FCX** † | Freeport-McMoRan | Materials | AI adjacent | **$5** | 67.7 | 57.8 | **63.7** | ROIC 12.5%, P/E 22.5x (0.95x own history), FCF yield after stock pay 2.1%, Piotroski 5.0/9, EPS beats 3/4, consensus EPS growth +75% |
| 13 | **WPC** | W. P. Carey | Real Estate | REIT income | **$5** | 68.0 | 55.3 | **62.9** | ROE 7.7%, P/FFO 12.2x (0.83x own history), Piotroski 7.7/9, FFO beats 2/4, consensus FFO growth +36% |
| 14 | **JPM** † | JPMorgan Chase | Financials |  | **$5** | 64.5 | 60.4 | **62.8** | ROE 18.7%, P/E 14.2x (1.16x own history), Piotroski 5.4/9, EPS beats 4/4, consensus EPS growth +20% |
| 15 | **CEG** † | Constellation Energy | Utilities | AI direct | **$5** | 73.1 | 46.1 | **62.3** | ROIC 11.2%, P/E 24.9x (0.68x own history), FCF yield after stock pay 1.3%, Piotroski 6.0/9, EPS beats 4/4, consensus EPS growth +31% |

† Borderline: not picked under both alternative splits.

## Each holding: thesis, risk and sell trigger

### 1. VRT, Vertiv: $8

- **Thesis:** Vertiv has the top Stage 2 score: the best Stage 1 score of the 25 and above-average checks. Orders more than doubled in Q3 2026 and guidance was raised, so the next year's sales are largely already ordered.
- **Key risk:** It depends on hyperscaler capex, like the fund's other AI names, and trades at 38x earnings.
- **Sell trigger:** Organic orders fall year on year for two quarters in a row, or full-year sales guidance is cut.

### 2. BKNG, Booking Holdings: $8

- **Thesis:** Booking earns a 61.5% return on capital, trades at 0.60x its 5-year EV/EBITDA and has a 7.4% free-cash-flow yield, most of which it returns through buybacks. It has beaten EPS consensus in each of the last 4 years.
- **Key risk:** Travel demand is softening: Q4 2026 guidance is for only 1-3% room-night growth.
- **Sell trigger:** Room nights fall year on year for two quarters in a row, or net debt/EBITDA rises above 2.5x.

### 3. COST, Costco: $8

- **Thesis:** Costco's adjusted and reported profits are almost identical (1.8% gap, the second-smallest of the 25), it has net cash, and sales are still growing about 10% a year. It ranks first in Consumer Staples at Stage 1.
- **Key risk:** Valuation: 53x earnings and only a 1.8% free-cash-flow yield after stock pay.
- **Sell trigger:** Comparable sales excluding fuel turn negative for two quarters in a row, or the US/Canada renewal rate falls below 90%.

### 4. LLY, Eli Lilly: $8

- **Thesis:** Lilly's revenue has grown 31.7% a year for three years, it scores 8 of 9 on Piotroski, and it has beaten EPS consensus four years running. Consensus expects EPS up 45.7% next year.
- **Key risk:** GLP-1 price erosion, and overlap with Novo Nordisk in the same drug class.
- **Sell trigger:** Combined Mounjaro and Zepbound revenue falls quarter on quarter twice in a row, or full-year revenue guidance is cut.

### 5. NFLX, Netflix: $8

- **Thesis:** Netflix trades at 0.43x its 5-year EV/EBITDA, with a 4.3% free-cash-flow yield and little gap between adjusted and reported profit. Consensus expects EPS up 41.9% next year.
- **Key risk:** EPS missed consensus in two of the last four years, and management has shown appetite for a very large acquisition.
- **Sell trigger:** Revenue growth falls below 8% year on year for two quarters in a row, or it announces an acquisition above $25B.

### 6. FICO, Fair Isaac: $7

- **Thesis:** Fair Isaac earns a 69% return on capital and scores 8 of 9 on Piotroski. It trades at 0.44x its 5-year EV/EBITDA after the 2026 sell-off over mortgage-score rules.
- **Key risk:** Regulation of mortgage-score pricing, and debt of 3.9x EBITDA, just under the 4.0x red-flag limit.
- **Sell trigger:** Scores revenue falls year on year in any quarter, or net debt/EBITDA goes above 4.0x (a Stage 1 red flag).

### 7. NVO, Novo Nordisk (ADR): $7

- **Thesis:** Novo Nordisk has the third-best Stage 1 score: a 34.8% return on capital at 0.28x its 5-year EV/EBITDA and 10.8x earnings. Its Stage 2 checks are weak (39.8), because the balance sheet has weakened and consensus expects EPS to fall 1.1%.
- **Key risk:** US price cuts from January 2027 outrunning volume growth; overlap with Lilly.
- **Sell trigger:** 2027 guidance (due February 2027) implies operating profit falling more than 10% at constant currency, or Wegovy plus Ozempic sales fall year on year for two quarters in a row.

### 8. ADBE, Adobe: $7

- **Thesis:** Adobe has the highest free-cash-flow yield of the 25 even after deducting stock pay (8.8%), trades at 0.32x its 5-year EV/EBITDA, and has beaten EPS consensus four years running.
- **Key risk:** Generative AI competition and a pending CEO change; stock pay is 8.3% of revenue.
- **Sell trigger:** Ending ARR growth falls below 9% year on year for two quarters in a row, or fiscal 2027 revenue targets imply growth below 8%.

### 9. ISRG, Intuitive Surgical: $7

- **Thesis:** Intuitive has the highest Altman Z (28.6) and current ratio (4.9) of the 25, no debt, and revenue growing 17% a year. Each installed robot produces recurring instrument sales.
- **Key risk:** US procedure growth has slowed to 10% and it plans price cuts of 3-5% per procedure; it trades at 47x earnings.
- **Sell trigger:** Worldwide da Vinci procedure growth falls below 10% for two quarters in a row.

### 10. PGR, Progressive: $7

- **Thesis:** Progressive earns a 33% return on equity and trades at 12.3x earnings, 0.38x its 5-year average. Its Q3 2026 combined ratio was 88.7, well inside its 96 target.
- **Key risk:** The auto insurance cycle is softening: premium growth has slowed to 2% and consensus expects flat EPS.
- **Sell trigger:** The trailing-12-month combined ratio rises above 96, or policies in force fall year on year.

### 11. VST, Vistra: $5

- **Thesis:** Vistra ranks first in Utilities at Stage 1 (82.2) with a 5.8% free-cash-flow yield. Its Stage 2 checks are weak (41.3): reported profit is far from adjusted profit and EPS missed consensus in three of four years. It is a borderline pick.
- **Key risk:** Texas power prices and regulation; it overlaps with Constellation and counts toward the AI limit.
- **Sell trigger:** Full-year adjusted EBITDA guidance is cut, or net debt/EBITDA rises above 4.0x.

### 12. FCX, Freeport-McMoRan: $5

- **Thesis:** Freeport has low debt (0.5x EBITDA), has beaten EPS consensus in three of four years, and consensus expects EPS up 75% next year as Grasberg restarts and copper prices stay high. It is a borderline pick.
- **Key risk:** The copper price and further delays at Grasberg; priced above its own history (1.35x).
- **Sell trigger:** Management moves the Grasberg 'near full capacity by end-2027' target later, or 2027 copper sales guidance is cut below 3.4 billion lb (now 3.7).

### 13. WPC, W. P. Carey: $5

- **Thesis:** W. P. Carey is the only Real Estate name picked. It trades at 0.83x its 5-year P/FFO, passes 6 of the 7 Piotroski signals that apply to it, and consensus expects FFO per share up 35.6%.
- **Key risk:** Interest rates and debt of 6.3x EBITDA. Its place depends on a scoring choice: see 'Decisions for Rob'.
- **Sell trigger:** The dividend is cut, full-year AFFO guidance is lowered, or net debt/EBITDA goes above 7.0x.

### 14. JPM, JPMorgan Chase: $5

- **Thesis:** JPMorgan has beaten EPS consensus in each of the last four years, has the smallest gap between adjusted and reported profit of the 25, and holds 14.6% CET1 capital. It is a borderline pick.
- **Key risk:** A credit downturn; it trades at 1.16x its own average P/E, so it isn't cheap.
- **Sell trigger:** CET1 falls below 13%, or return on tangible common equity is below 15% for two quarters in a row.

### 15. CEG, Constellation Energy: $5

- **Thesis:** Constellation has beaten EPS consensus four years running and raised 2026 guidance on 9 Nov 2026. It took the 15th place by 0.11 points over TJX, so it is the most marginal pick.
- **Key risk:** Rules on supplying data centers directly, and a 52% average gap between adjusted and reported profit; overlaps with Vistra.
- **Sell trigger:** The midpoint of full-year adjusted operating EPS guidance is lowered, or net debt/EBITDA rises above 4.0x.

## Portfolio shape and limits

| Sector | Names | Count | Dollars |
|---|---|---|---|
| Health Care | LLY, NVO, ISRG | 3 | $22 |
| Technology | FICO, ADBE | 2 | $14 |
| Financials | PGR, JPM | 2 | $12 |
| Utilities | VST, CEG | 2 | $10 |
| Comm. Services | NFLX | 1 | $8 |
| Cons. Discretionary | BKNG | 1 | $8 |
| Cons. Staples | COST | 1 | $8 |
| Industrials | VRT | 1 | $8 |
| Materials | FCX | 1 | $5 |
| Real Estate | WPC | 1 | $5 |

| Limit | Rule | Actual | Result |
|---|---|---|---|
| Holdings | exactly 15 | 15 | Pass |
| Sectors | at least 7 | 10 | Pass |
| Names per sector | at most 3 | 3 (Health Care) | Pass |
| Dollars per sector | at most $25 | $22 (Health Care) | Pass |
| AI/data-center names | at most 4 | 4 (VRT, VST, FCX, CEG) | Pass, at the limit |
| AI/data-center dollars | at most $30 | $23 | Pass |
| Oil-linked names | at most 2 | 0 | Pass |
| Rate-sensitive income names | at most 3 | 1 (WPC) | Pass |
| Non-US ADRs | at most 3 | 1 (NVO) | Pass |
| Position size | $4 to $10 | $5 to $8 | Pass |
| Pair correlation | none above 0.85 | not checkable (no price data) | Flagged below |

**Overlapping bets (flagged, not enforced):**

- **LLY ($8) and NVO ($7):** both depend on GLP-1 obesity and diabetes drugs, and on US drug pricing. Together $15.
- **CEG ($5) and VST ($5):** both are merchant power producers tied to data-center demand, and both count toward the AI limit. Together $10.
- **COST and TJX:** only COST is held, so this overlap doesn't arise.
- **AI/data-center as a whole:** VRT, VST, FCX, CEG = $23 of $100. META, GOOGL and EQIX are on the bench and can't be added while these four are held.

## Stage 2 checks: the numbers for all 25

Each check is a percentile across the 25 (100 = best). 'n/a' means the check doesn't apply and was skipped, not scored as zero.

| # | Ticker | Stage 1 | Piotroski | Earnings quality | Cash yield after stock pay | Strength | Delivery | Fwd growth | Checks used | Checks | **Stage 2** | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | VRT | 89.1 | 54 | 77 | 67 | 61 | 49 | 88 | 6 | 66.1 | **79.9** | Selected |
| 2 | BKNG | 88.0 | 68 | 37 | 95 | 59 | 76 | 40 | 6 | 62.6 | **77.9** | Selected |
| 3 | COST | 83.8 | 80 | 96 | 24 | 57 | 45 | 32 | 6 | 55.6 | **72.5** | Selected |
| 4 | LLY | 73.5 | 98 | 38 | 19 | 75 | 84 | 84 | 6 | 66.4 | **70.7** | Selected |
| 5 | NFLX | 72.6 | 80 | 74 | 71 | 72 | 18 | 80 | 6 | 65.9 | **69.9** | Selected |
| 6 | FICO | 76.4 | 98 | 47 | 86 | 55 | 41 | 16 | 6 | 57.0 | **68.7** | Selected |
| 7 | NVO | 87.4 | 24 | 83 | 81 | 20 | 26 | 4 | 6 | 39.8 | **68.3** | Selected |
| 8 | ADBE | 69.9 | 80 | 44 | 100 | 55 | 64 | 44 | 6 | 64.5 | **67.7** | Selected |
| 9 | ISRG | 71.8 | 54 | 53 | 29 | 100 | 65 | 56 | 6 | 59.4 | **66.8** | Selected |
| 10 | PGR | 78.7 | 64 | 60 | n/a | n/a | 61 | 8 | 4 | 48.2 | **66.5** | Selected |
| 11 | VST | 82.2 | 24 | 35 | 76 | 7 | 6 | 100 | 6 | 41.3 | **65.8** | Selected |
| 12 | FCX | 67.7 | 24 | 65 | 38 | 55 | 73 | 92 | 6 | 57.8 | **63.7** | Selected |
| 13 | WPC | 68.0 | 92 | 37 | n/a | n/a | 20 | 72 | 4 | 55.3 | **62.9** | Selected |
| 14 | JPM | 64.5 | 44 | 70 | n/a | n/a | 80 | 48 | 4 | 60.4 | **62.8** | Selected |
| 15 | CEG | 73.1 | 54 | 12 | 14 | 36 | 92 | 68 | 6 | 46.1 | **62.3** | Selected |
| 16 | TJX | 63.7 | 80 | 82 | 62 | 48 | 53 | 36 | 6 | 60.0 | **62.2** | Bench |
| 17 | HSY | 61.9 | 24 | 53 | 90 | 44 | 86 | 76 | 6 | 62.3 | **62.0** | Bench |
| 18 | META | 75.0 | 24 | 26 | 10 | 80 | 57 | 52 | 6 | 41.4 | **61.5** | Bench |
| 19 | GOOGL | 64.0 | 80 | 41 | 5 | 84 | 24 | 96 | 6 | 55.0 | **60.4** | Bench |
| 20 | LIN | 71.7 | 54 | 51 | 33 | 25 | 68 | 24 | 6 | 42.5 | **60.0** | Bench |
| 21 | GE | 69.3 | 24 | 8 | 43 | 30 | 88 | 60 | 6 | 42.1 | **58.4** | Bench |
| 22 | EQIX | 70.3 | 24 | 41 | n/a | 34 | 8 | 64 | 5 | 34.2 | **55.9** | Bench |
| 23 | SYK | 60.1 | 24 | 32 | 57 | 64 | 72 | 28 | 6 | 46.1 | **54.5** | Bench |
| 24 | YUM | 63.3 | 24 | 60 | 52 | 43 | 14 | 20 | 6 | 35.6 | **52.2** | Bench |
| 25 | JNJ | 55.9 | 4 | 38 | 48 | 48 | 30 | 12 | 6 | 29.9 | **45.5** | Bench |

The raw metrics behind the percentiles:

| Ticker | Fiscal year | Piotroski (signals used) | Adj vs GAAP gap, 5y | Stock pay % revenue | FCF yield | after stock pay | Altman Z | Current ratio | Avg EPS surprise, 4y | Beats | Fwd EPS growth |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VRT | 2025 | 6.0 (6/9) | 7.3% | 0.5% | 3.9% | 3.9% | 6.5 | 1.55 | 0.8% | 3/4 | 69.3% |
| BKNG | 2025 | 6.8 (6/8) | 20.2% | 2.3% | 7.4% | 7.0% | 6.9 | 1.33 | 1.6% | 4/4 | 14.6% |
| COST | 2026 | 7.0 (7/9) | 1.8% | 0.3% | 1.9% | 1.8% | 9.1 | 1.06 | 0.7% | 3/4 | 9.8% |
| LLY | 2025 | 8.0 (8/9) | 27.6% | 1.0% | 1.5% | 1.5% | 8.4 | 1.58 | 3.1% | 4/4 | 45.7% |
| NFLX | 2025 | 7.0 (7/9) | 2.4% | 0.8% | 4.3% | 4.2% | 13.3 | 1.19 | -1.0% | 2/4 | 41.9% |
| FICO | 2026 | 8.0 (8/9) | 4.0% | 7.3% | 6.6% | 5.7% | 12.4 | 0.99 | 0.2% | 3/4 | 3.1% |
| NVO | 2025 | 5.0 (5/9) | 3.1% | 0.5% | 5.8% | 5.6% | 3.9 | 0.80 | 0.1% | 2/4 | -1.1% |
| ADBE | 2025 | 7.0 (7/9) | 3.7% | 8.3% | 10.9% | 8.8% | 12.1 | 1.00 | 0.7% | 4/4 | 16.9% |
| ISRG | 2025 | 6.0 (6/9) | 1.9% | 8.0% | 2.3% | 1.9% | 28.6 | 4.87 | 2.7% | 3/4 | 25.5% |
| PGR | 2025 | 6.4 (5/7) | 30.1% | 0.1% | 11.1% | n/a | n/a | n/a | 1.8% | 3/4 | 0.4% |
| VST | 2025 | 5.0 (5/9) | 73.6% | 0.6% | 5.8% | 5.5% | 1.7 | 0.78 | -372.6% | 1/4 | 282.1% |
| FCX | 2025 | 5.0 (5/9) | 12.2% | 0.5% | 2.3% | 2.1% | 3.2 | 2.29 | 5.7% | 3/4 | 75.1% |
| WPC | 2025 | 7.7 (6/7) | 15.2% | 2.3% | -5.2% | n/a | n/a | n/a | -0.7% | 2/4 | 35.6% |
| JPM | 2025 | 5.4 (3/5) | 1.6% | 2.0% | n/a | n/a | n/a | n/a | 2.1% | 4/4 | 19.7% |
| CEG | 2025 | 6.0 (6/9) | 51.9% | n/a | 1.3% | 1.3% | 1.7 | 1.53 | 12.0% | 4/4 | 31.4% |
| TJX | 2026 | 7.0 (7/9) | 5.4% | 0.3% | 3.9% | 3.8% | 6.8 | 1.14 | 1.2% | 3/4 | 12.1% |
| HSY | 2025 | 5.0 (5/9) | 20.8% | 0.6% | 6.1% | 5.9% | 5.8 | 1.19 | 3.1% | 4/4 | 38.4% |
| META | 2025 | 5.0 (5/9) | 14.1% | 10.2% | 1.8% | 0.5% | 7.1 | 2.60 | 1.4% | 3/4 | 23.5% |
| GOOGL | 2025 | 7.0 (7/9) | 7.9% | 6.2% | 0.6% | -0.1% | 9.8 | 2.01 | -0.2% | 2/4 | 81.0% |
| LIN | 2025 | 6.0 (6/9) | 26.9% | 0.5% | 2.1% | 2.0% | 4.7 | 0.88 | 0.8% | 4/4 | 8.8% |
| GE | 2025 | 5.0 (5/9) | 61.1% | n/a | 2.3% | 2.3% | 3.6 | 1.04 | 4.9% | 4/4 | 28.1% |
| EQIX | 2025 | 5.0 (5/9) | 9.9% | 5.4% | -2.7% | n/a | 2.8 | 1.32 | -8.9% | 1/4 | 31.4% |
| SYK | 2025 | 5.0 (5/9) | 35.5% | 1.0% | 3.8% | 3.7% | 6.4 | 1.89 | 1.3% | 4/4 | 8.9% |
| YUM | 2025 | 5.0 (5/9) | 7.5% | 0.8% | 3.7% | 3.6% | 3.5 | 1.35 | -0.6% | 1/4 | 6.1% |
| JNJ | 2025 | 4.0 (4/9) | 23.9% | 1.4% | 3.0% | 2.8% | 7.5 | 1.03 | 0.3% | 2/4 | 3.1% |

Full detail, including which Piotroski signals each company passed and failed, is in `scores_stage2.csv`.

## Robustness

The selection was re-run with the Stage 1 / Stage 2 split moved either way.

| Split (Stage 1 / checks) | Of the base 15 kept | Comes in | Drops out |
|---|---|---|---|
| 60/40 (base) | 15 of 15 | none | none |
| 80/20 | 13 of 15 | LIN META | FCX JPM |
| 40/60 | 13 of 15 | HSY TJX | CEG VST |

- **Borderline holdings:** VST, FCX, JPM, CEG. FCX and JPM rely on their Stage 2 checks; VST and CEG rely on their Stage 1 scores.
- **Solid:** the other 11 are picked under all three splits.
- **First in line from the bench:** TJX and HSY (40/60), META and LIN (80/20).

**What if the cash-yield check were scored for the insurer and the REITs?** The spec skips it for PGR, WPC and EQIX (and JPM has no free cash flow at all). Scoring it anyway:

| Ticker | Stage 2 score as specified | Rank | If scored | Rank |
|---|---|---|---|---|
| PGR | 66.52 | 10 | 70.66 | 5 |
| WPC | 62.90 | 13 | 58.81 | 20 |
| EQIX | 55.88 | 22 | 54.15 | 23 |
| CEG | 62.32 | 15 | 62.75 | 14 |
| TJX | 62.21 | 16 | 62.25 | 15 |

Result: WPC out, TJX in. The other 14 are unchanged. PGR would move up to rank 5 and into the $8 group, with NFLX moving down to $7.

## The bench (in rank order)

These 10 are watched every month and are the only names that can be swapped in (Stage 4).

| Rank | Ticker | Company | Sector | Stage 1 | Checks | Stage 2 | Gap to 15th place | Limits it would hit today |
|---|---|---|---|---|---|---|---|---|
| 16 | TJX | TJX Companies | Cons. Discretionary | 63.7 | 60.0 | 62.2 | -0.1 | none |
| 17 | HSY | Hershey | Cons. Staples | 61.9 | 62.3 | 62.0 | -0.3 | none |
| 18 | META | Meta Platforms | Comm. Services | 75.0 | 41.4 | 61.5 | -0.8 | AI/data-center limit (4 held) |
| 19 | GOOGL | Alphabet | Comm. Services | 64.0 | 55.0 | 60.4 | -1.9 | AI/data-center limit (4 held) |
| 20 | LIN | Linde | Materials | 71.7 | 42.5 | 60.0 | -2.3 | none |
| 21 | GE | GE Aerospace | Industrials | 69.3 | 42.1 | 58.4 | -3.9 | none |
| 22 | EQIX | Equinix | Real Estate | 70.3 | 34.2 | 55.9 | -6.4 | AI/data-center limit (4 held) |
| 23 | SYK | Stryker | Health Care | 60.1 | 46.1 | 54.5 | -7.8 | sector limit (3 Health Care names held) |
| 24 | YUM | Yum Brands | Cons. Discretionary | 63.3 | 35.6 | 52.2 | -10.1 | none |
| 25 | JNJ | Johnson & Johnson | Health Care | 55.9 | 29.9 | 45.5 | -16.9 | sector limit (3 Health Care names held) |

## Every cut name and why

No name was cut by a portfolio limit or a qualitative override. All 10 were cut on score: the 15 places were filled before the walk down the ranking reached them.

| Ticker | Stage 2 score | Reason | Strongest checks | Weakest checks |
|---|---|---|---|---|
| TJX | 62.2 | Rank 16: 0.1 points below the 15th place | earnings quality (82), Piotroski (80) | forward growth (36), financial strength (48) |
| HSY | 62.0 | Rank 17: 0.3 points below the 15th place | cash yield after stock pay (90), earnings delivery (86) | Piotroski (24), financial strength (44) |
| META | 61.5 | Rank 18: 0.8 points below the 15th place. Would also be blocked by the AI/data-center limit (4 held) | financial strength (80), earnings delivery (57) | cash yield after stock pay (10), Piotroski (24) |
| GOOGL | 60.4 | Rank 19: 1.9 points below the 15th place. Would also be blocked by the AI/data-center limit (4 held) | forward growth (96), financial strength (84) | cash yield after stock pay (5), earnings delivery (24) |
| LIN | 60.0 | Rank 20: 2.3 points below the 15th place | earnings delivery (68), Piotroski (54) | forward growth (24), financial strength (25) |
| GE | 58.4 | Rank 21: 3.9 points below the 15th place | earnings delivery (88), forward growth (60) | earnings quality (8), Piotroski (24) |
| EQIX | 55.9 | Rank 22: 6.4 points below the 15th place. Would also be blocked by the AI/data-center limit (4 held) | forward growth (64), earnings quality (41) | earnings delivery (8), Piotroski (24) |
| SYK | 54.5 | Rank 23: 7.8 points below the 15th place. Would also be blocked by the sector limit (3 Health Care names held) | earnings delivery (72), financial strength (64) | Piotroski (24), forward growth (28) |
| YUM | 52.2 | Rank 24: 10.1 points below the 15th place | earnings quality (60), cash yield after stock pay (52) | earnings delivery (14), forward growth (20) |
| JNJ | 45.5 | Rank 25: 16.9 points below the 15th place. Would also be blocked by the sector limit (3 Health Care names held) | financial strength (48), cash yield after stock pay (48) | Piotroski (4), forward growth (12) |

## Qualitative check: all 25

**How current this is:** Claude's own knowledge of these companies runs to roughly mid-2026. Anything later comes from web searches run on 13 Nov 2026, listed under Sources. Those are mostly news summaries of company releases and were not checked against the filings. For GOOGL, TJX, YUM, SYK and JNJ no third-quarter news was verified.

**Overrides:** none. An override needs a specific event such as a pending takeover, a restatement or a large guidance cut, and none was found. Three items came close and are worth knowing: FICO withheld fiscal 2027 guidance; Novo Nordisk will cut US list prices by about 50% (Wegovy) and 35% (Ozempic) from January 2027; Booking guided Q4 room-night growth down to 1-3%. None is a broken thesis under the rules, and each is covered by that holding's sell trigger.

**1. VRT, Vertiv** (held, $8). *Moat:* Power and cooling equipment that data centers can't run without, plus a service network competitors struggle to copy. *What would break it:* A pause in hyperscaler data-center spending. Orders would fall first, and the stock trades at 38x earnings. *Next 12 months:* Q3 sales rose 61%, organic orders more than doubled and 2026 guidance was raised (sales about $14.65B). Q4 results and 2027 guidance come in February. *Capital allocation:* Reinvests in capacity and small acquisitions; almost no net debt; token dividend. *Source:* [Vertiv Q3 2026 release, 28 Oct 2026](https://www.sec.gov/Archives/edgar/data/0001674101/000162828026067707/q32026exhibit991vrt10282026.htm)

**2. BKNG, Booking Holdings** (held, $8). *Moat:* The largest online travel agency; scale in European hotels gives it better supply and marketing efficiency than rivals. *What would break it:* A travel slowdown, or AI assistants and Google taking the booking step. Q4 guidance already slows to 1-3% room-night growth. *Next 12 months:* Q3 room nights rose 7%, ahead of guidance, but Q4 guidance is soft and revenue took a $900M cut for an FTC matter at Priceline. Q4 results in February. *Capital allocation:* Returns nearly all free cash through buybacks (shareholder yield 10.9%) and a growing dividend. *Source:* [Booking Q3 2026 results coverage, 3 Nov 2026](https://finviz.com/news/415433/booking-holdings-shares-little-changed-as-revenue-miss-and-weaker-q4-outlook-offset-earnings-beat)

**3. COST, Costco** (held, $8). *Moat:* Membership model: low prices funded by fees, and renewal rates among the highest in retail. *What would break it:* Paying 53x earnings for high-single-digit growth. Any slip in renewals or comparable sales would hit the multiple hard. *Next 12 months:* October sales rose 12.6%; fiscal 2026 sales were $297B with executive members up 9.4%. Fiscal Q1 results in December; a special dividend is possible but not announced. *Capital allocation:* Conservative: net cash, steady openings, regular dividend and occasional specials, few buybacks. *Source:* [Costco October 2026 sales release, 4 Nov 2026](https://www.morningstar.com/news/globe-newswire/9870370/costco-wholesale-corporation-reports-october-sales-results)

**4. LLY, Eli Lilly** (held, $8). *Moat:* Tirzepatide (Mounjaro, Zepbound) is the best-selling GLP-1 franchise, backed by heavy manufacturing investment and a deep pipeline. *What would break it:* Price erosion (US realized prices fell 7% in Q3), a safety signal, or oral competitors. At 36x earnings the stock needs the growth to continue. *Next 12 months:* Q3 revenue rose 39% and 2026 revenue guidance was raised to $91-92B. The oral pill orforglipron has launched but missed consensus. 2027 guidance comes in early 2027. *Capital allocation:* Reinvests heavily in plants and acquisitions; dividend grows; buybacks are secondary. *Source:* [Lilly Q3 2026 release, 29 Oct 2026](https://www.sec.gov/Archives/edgar/data/0000059478/000005947826000104/q326lillysalesandearningsp.htm)

**5. NFLX, Netflix** (held, $8). *Moat:* The largest streaming subscriber base, which lets it spread content cost over more viewers than any rival; advertising is a second engine. *What would break it:* Subscriber growth stalling in mature markets, or a return to large acquisitions. Its bid for Warner Bros. collapsed in 2026. *Next 12 months:* Q3 revenue rose 12% and net income 48%. It cut about 6% of staff before results. Ad revenue and 2027 margin guidance (January) are the catalysts. *Capital allocation:* Buybacks from rising free cash flow; no dividend. The failed Warner bid shows appetite for big deals. *Source:* [TheWrap streaming comparison (Warner bid collapsed), Aug 2026](https://www.thewrap.com/industry-news/business/netflix-disney-warner-bros-paramount-subscribers-revenue-profits-august-2026/) [NBC on Netflix Q3 2026 results and layoffs, Oct 2026](https://www.nbcbayarea.com/entertainment/entertainment-news/netflix-investors-recent-shake-ups-layoffs/4161943/)

**6. FICO, Fair Isaac** (held, $7). *Moat:* The FICO Score is the standard in US lending decisions, which gives it rare pricing power. *What would break it:* Mortgage-score regulation and competition from VantageScore, and its debt (3.9x EBITDA at Stage 1, just under the 4.0x red flag). *Next 12 months:* Fiscal Q4 revenue rose 27%, but management withheld fiscal 2027 guidance while it negotiates 2027 mortgage pricing, and the stock fell. Guidance is the next catalyst. *Capital allocation:* Buybacks funded partly with debt; now paused to repay a term loan. No dividend. *Source:* [FICO Q4 fiscal 2026 release, 4 Nov 2026](https://www.morningstar.com/news/business-wire/20261104478581/fico-announces-earnings-of-812-per-share-for-fourth-quarter-fiscal-2026) [FICO results coverage (guidance withheld, mortgage price frozen), Nov 2026](https://finviz.com/news/416440/fico-tops-estimates-and-software-accelerates-but-withheld-guidance-and-a-frozen-mortgage-price-cloud-the-scores-engine)

**7. NVO, Novo Nordisk (ADR)** (held, $7). *Moat:* Half of the GLP-1 duopoly, with decades of diabetes manufacturing scale and the first oral obesity pill on the market. *What would break it:* Price cuts outrunning volume. Wegovy prices fell 30-35% in Q3 and US list prices drop about 50% (Wegovy) and 35% (Ozempic) from 1 Jan 2027. Consensus EPS for 2026 is flat. *Next 12 months:* Raised 2026 guidance for the third time on 4 Nov; the Wegovy pill has about 80% of new US prescriptions. 2027 guidance in February is the key date. *Capital allocation:* Dividend plus buyback (shareholder yield 5.5%); debt rose after the Catalent plant purchase. *Source:* [Novo Nordisk Q3 2026 results coverage, 4 Nov 2026](https://finviz.com/news/415434/novo-nordisk-raises-2026-guidance-as-obesity-drug-sales-rise-22-and-quarterly-earnings-beat-forecasts)

**8. ADBE, Adobe** (held, $7). *Moat:* The standard tools for creative work and documents, sold by subscription to a locked-in professional base. *What would break it:* Generative AI tools taking the lower end of creative work; ARR growth slipping below 10%; a new CEO. *Next 12 months:* Q3 revenue rose 13% and fiscal 2026 targets were raised. Fiscal year-end results and 2027 targets come in December. The CEO said in March he will step down once a successor is named. *Capital allocation:* Large buybacks (shareholder yield 8.3%), but stock pay is 8.3% of revenue, the second-highest of the 25. *Source:* [Adobe Q3 fiscal 2026 release, 10 Sep 2026](https://seekingalpha.com/pr/20647784-adobe-reports-record-q3-results) [Adobe CEO transition announcement, 12 Mar 2026](https://www.businesswire.com/news/home/20260312777904/en/Shantanu-Narayen-Announces-Decision-to-Transition-as-Adobes-CEO-Once-Successor-is-Named)

**9. ISRG, Intuitive Surgical** (held, $7). *Moat:* About 12,000 da Vinci systems installed; surgeons train on it and hospitals buy instruments for every procedure. *What would break it:* Slower US procedure growth (10% in Q3, the lowest since COVID), planned 3-5% price cuts per procedure, and new robot competitors. *Next 12 months:* Q3 revenue rose 22% and adjusted EPS beat, but the stock fell on the US slowdown and a $450M antitrust settlement charge. 2027 procedure guidance comes in January. *Capital allocation:* No debt, large cash pile, steady buybacks, no dividend. *Source:* [Intuitive Q3 2026 release, 20 Oct 2026](https://www.biospace.com/press-releases/intuitive-announces-third-quarter-2026-earnings) [MassDevice on Intuitive's US slowdown and price cuts, Oct 2026](https://www.massdevice.com/intuitive-stock-slides-as-us-da-vinci-procedures-slow-despite-sales-gains/)

**10. PGR, Progressive** (held, $7). *Moat:* Best-in-class auto insurance pricing and direct distribution; it reprices faster than peers. *What would break it:* The auto cycle turning: competitors cutting rates squeezes growth and margins. Consensus EPS growth for 2026 is close to zero. *Next 12 months:* Q3 combined ratio 88.7; policies in force up 6% but premium growth has slowed to 2%. Monthly results are published, so the trend is visible early. *Capital allocation:* Small regular dividend plus a variable annual dividend tied to results; modest buybacks. *Source:* [Progressive September 2026 results, 14 Oct 2026](https://finviz.com/news/402384/progressive-reports-september-2026-results)

**11. VST, Vistra** (held, $5). *Moat:* Low-cost Texas and PJM generating fleet, including nuclear, in markets short of firm power. *What would break it:* Texas power prices and regulation. Management cut its ERCOT load-growth outlook to 4-6% and the stock hit a 52-week low; earnings swing with hedges. *Next 12 months:* Q3 adjusted EBITDA rose more than 50%; closed the Cogentrix gas-plant purchase in October; signed a 20-year, 207 MW data-center deal at Odessa. 2027 guidance update expected with Q4 results. *Capital allocation:* Aggressive buybacks alongside debt-funded acquisitions; net debt/EBITDA 2.5x. *Source:* [Vistra Q3 2026 results, 6 Nov 2026](https://finviz.com/news/418259/vistra-reports-third-quarter-2026-results)

**12. FCX, Freeport-McMoRan** (held, $5). *Moat:* Large, long-life copper mines (Grasberg, Arizona) that are hard to replicate; copper demand is rising with electrification and data centers. *What would break it:* The copper price, and Grasberg's recovery from the September 2025 mudslide slipping again. Indonesia also carries political risk. *Next 12 months:* Q3 adjusted EPS beat (88 cents vs 81) on a $6.54/lb copper price, but 2026 and 2027 sales guidance were trimmed. Grasberg should reach 80% of capacity in mid-2027. *Capital allocation:* Dividend with a variable part, buybacks when copper is high; debt is low (0.5x EBITDA). *Source:* [Freeport Q3 2026 results coverage, 28 Oct 2026](https://www.miningweekly.com/article/freeport-tops-profit-estimates-on-copper-rally-as-grasberg-recovery-continues-2026-10-28)

**13. WPC, W. P. Carey** (held, $5). *Moat:* Long net leases with built-in rent increases across industrial and retail property in the US and Europe. *What would break it:* Higher rates, which raise its funding cost and lower property values; debt is 6.3x EBITDA; tenant defaults. *Next 12 months:* Q3 AFFO rose 6.4% to $1.33 a share and 2026 AFFO guidance was raised to $5.23-5.29. Management expects a lower Q4 because of rent abatements. *Capital allocation:* REIT: pays out most cash flow as dividends and funds purchases with debt and new shares (share count rising). *Source:* [W. P. Carey Q3 2026 release, 27 Oct 2026](https://www.sec.gov/Archives/edgar/data/0001025378/000102537826000129/wpc2026q38-kerexh991.htm)

**14. JPM, JPMorgan Chase** (held, $5). *Moat:* The largest US bank, with the scale to outspend rivals on technology and a cheap deposit base. *What would break it:* A credit downturn or falling rates squeezing interest income; it trades above its own average P/E. *Next 12 months:* Q3 net income was $15.3B with net interest income up 13%; charge-offs fell. Expenses rose 12%. *Capital allocation:* Dividend growth plus large buybacks from excess capital (CET1 14.6%). *Source:* [JPMorgan Q3 2026 results coverage, Oct 2026](https://pulse2.com/jpmorgan-chase-q3-2026-results)

**15. CEG, Constellation Energy** (held, $5). *Moat:* The largest US nuclear fleet: carbon-free, always-on power that can't be built quickly by anyone else. *What would break it:* Regulatory limits on selling power directly to data centers, or lower power prices. Reported profit is far from adjusted profit (52% average gap). *Next 12 months:* On 9 Nov raised 2026 adjusted EPS guidance to $12.50-12.80 and announced a 20-year deal enabling $4.3B of nuclear uprates plus a 2,700 MW supply deal tied to Google. *Capital allocation:* Growing dividend, buybacks, and acquisitions (Calpine; now a $715M Rhode Island gas plant, pending approval). *Source:* [Constellation Q3 2026 results coverage, 9 Nov 2026](https://www.citybiz.co/?p=931445)

**16. TJX, TJX Companies** (bench). *Moat:* Off-price buying at scale: it gets branded stock cheaply when other retailers over-order, and shoppers trade down to it. *What would break it:* A shortage of excess inventory, or weaker lower-income spending. *Next 12 months:* Reports fiscal Q3 around 18 Nov 2026 (not yet out). Last fiscal year EPS was $4.73; consensus for this year is $5.30. *Capital allocation:* Steady dividend growth and buybacks.

**17. HSY, Hershey** (bench). *Moat:* Dominant US chocolate brands with pricing power. *What would break it:* Cocoa costs and volume: North America confectionery volume fell about 11 points in Q3 as higher prices bit. *Next 12 months:* Q3 adjusted EPS rose 103% (including tariff refunds) and management expects cocoa costs to fall in 2027. *Capital allocation:* Reliable dividend; modest buybacks. *Source:* [Hershey Q3 2026 release, Oct 2026](https://finviz.com/news/411196/hershey-reports-third-quarter-2026-financial-results)

**18. META, Meta Platforms** (bench). *Moat:* Three billion daily users and the second-largest digital ad business. *What would break it:* AI spending that never earns its cost. Q3 capex was $34.9B and free cash flow turned negative for the first time since 2012. *Next 12 months:* Q3 revenue beat, but 2026 capex guidance of $135-145B sent the stock down 7%. A new non-voting share class takes effect in January 2027. *Capital allocation:* Buybacks and a small dividend, now squeezed by capex. Founder control limits shareholder say. *Source:* [Meta Q3 2026 results coverage, Oct 2026](https://investinglive.com/stocks/meta-shares-fall-7-on-huge-spending-plans/)

**19. GOOGL, Alphabet** (bench). *Moat:* Search, YouTube and a fast-growing cloud business, with its own AI chips and models. *What would break it:* AI assistants eroding search, antitrust remedies, and capex outrunning cash flow (FCF yield 0.6%). *Next 12 months:* 2026 consensus EPS (19.57) is inflated by one-off gains: the 2027 estimate is 14.79. Q3 news was not verified in this check. *Capital allocation:* Buybacks and a small dividend, with capex taking most operating cash.

**20. LIN, Linde** (bench). *Moat:* Industrial gases sold on long contracts with local density; the most profitable of the big three. *What would break it:* Weak industrial volumes; revenue has grown only 0.6% a year and the price is in line with its own history. *Next 12 months:* Q3 sales rose 9% and 2026 adjusted EPS guidance is $17.82-17.92 (up 8-9%). *Capital allocation:* Dividend growth and steady buybacks; disciplined project investment. *Source:* [Linde Q3 2026 release, 29 Oct 2026](https://www.sec.gov/Archives/edgar/data/0001707925/000165495426009199/lin_ex991.htm)

**21. GE, GE Aerospace** (bench). *Moat:* The largest installed base of commercial jet engines; most profit comes from decades of servicing them. *What would break it:* A fall in flying hours, or engine durability problems; 42x earnings leaves little room. *Next 12 months:* Q3 EPS was $2.25 and 2026 guidance was raised across the board. *Capital allocation:* Buybacks and a rising dividend since the spin-offs. *Source:* [GE Aerospace Q3 2026 coverage, 20 Oct 2026](https://www.webull.com/news/15780287818181632)

**22. EQIX, Equinix** (bench). *Moat:* Network-dense interconnection data centers that customers rarely leave. *What would break it:* High debt (4.9x EBITDA) and heavy building while rates are high; EPS has missed consensus in 3 of the last 4 years. *Next 12 months:* Q3 bookings were a record and 2026 guidance was raised for the third time. *Capital allocation:* REIT: pays out most cash flow and funds growth with debt and new shares (share count rising). *Source:* [Equinix Q3 2026 release, 28 Oct 2026](https://www.sec.gov/Archives/edgar/data/0001101239/000110123926000178/a991eqix-q326xpr.htm)

**23. SYK, Stryker** (bench). *Moat:* Leading positions in orthopaedic implants and hospital equipment, including the Mako surgical robot. *What would break it:* Hospital budgets, and acquisition integration: adjusted and reported profit differ by 36% on average. *Next 12 months:* Q3 news was not verified in this check. *Capital allocation:* Acquisition-led growth; dividend; share count rising.

**24. YUM, Yum Brands** (bench). *Moat:* Franchised global brands (KFC, Taco Bell) that need little capital. *What would break it:* Weak sales at KFC and Pizza Hut, and debt (2.1x EBITDA with negative book equity). *Next 12 months:* Missed EPS consensus in 3 of the last 4 years. Q3 news was not verified in this check. *Capital allocation:* Dividends and buybacks funded partly by borrowing.

**25. JNJ, Johnson & Johnson** (bench). *Moat:* A diversified drug and medical-device group with a AAA-grade balance sheet. *What would break it:* Stelara's patent loss, talc litigation, and a price above its own history (1.45x on EV/EBITDA). *Next 12 months:* Q3 news was not verified in this check. *Capital allocation:* Dividend growth for over 60 years, buybacks, and regular acquisitions.

## Decisions for Rob

1. **WPC or TJX for one $5 place.** The brief said to skip a check that doesn't apply, and named only the bank for the cash-yield check. Before computing anything, the spec extended that to the insurer and the two REITs, because Stage 1 already treats free cash flow as not meaningful for those sectors (a REIT's 'free cash flow' subtracts property purchases). That choice was logged first, but it does decide this place: as specified WPC is in at rank 13; with the check scored, WPC falls to rank 20 and TJX comes in. The allocation file follows the spec (WPC). Say the word and it is switched and logged.
2. **Keep both names in each overlapping pair, or swap one out?** LLY/NVO and CEG/VST. The rules flag these but don't force a change. If you want to cut an overlap, the lower-scored name in each pair is NVO (rank 7) and CEG (rank 15), and the first bench names are TJX and HSY.
3. **Price data.** Stage 2 ran without momentum or correlations. The first monthly review (Stage 4) needs prices in any case. `data/stage2_25_companies/prices_monthly.xlsx` is ready to refresh on the Bloomberg terminal. If you pull it before buying, momentum and the 0.85 correlation limit can be applied first.
4. **Broker.** It must offer fractional shares for all 15, including the NVO ADR, to a US citizen with a UK address.

## Verification

Output of `/usr/local/bin/python3 -I tools/check_portfolio.py` (exit code 0):

```
PASS  columns are as specified
PASS  exactly 15 unique tickers  [15 unique]
PASS  all tickers are in the 25-name shortlist  [outside: none]
PASS  sectors match the shortlist
PASS  dollars are whole numbers
PASS  dollars sum to exactly 100  [sum 100]
PASS  every position is $4 to $10  [min 5, max 8]
PASS  no sector above $25  [largest: Health Care $22]
PASS  at least 7 sectors  [10 sectors]
PASS  at most 3 names per sector  [largest: Health Care 3]
PASS  AI/data-center: at most 4 names  [4: VRT VST FCX CEG]
PASS  AI/data-center: at most $30  [$23]
PASS  oil-linked: at most 2 names  [0]
PASS  REIT/utility income: at most 3 names  [1: WPC]
PASS  non-US ADRs: at most 3 names  [1: NVO]
PASS  AI tags in the CSV match the fixed list
PASS  ranks are 1 to 15, no repeats
PASS  a higher rank never gets fewer dollars than a lower one within the tilt  [informational if a cap moved dollars]
PASS  every row has a thesis
PASS  every row has a sell trigger

20 of 20 checks passed. Portfolio is valid.
```

## Data notes and caveats

- **No momentum, no correlations.** No price history was pulled, so the Momentum pillar (20% in the framework) is not scored and the 0.85 pair-correlation limit is not checked. Theme limits and the flagged overlaps stand in for it. No prices from other sources were used.
- **One date.** Valuations are as of 13 Nov 2026. They will have moved by the time orders are placed.
- **Stock-pay data gaps.** CEG has no SBC page and GE's SBC rows stop at 2022. For both, earnings quality uses the adjusted-vs-GAAP gap only and the cash yield is not reduced for stock pay. Neither result changes a selection: GE is rank 21.
- **Skipped checks.** JPM, PGR and WPC are scored on 4 checks (no cash yield, no Altman Z or current ratio); EQIX on 5. Their checks score rests on fewer measures and is less reliable.
- **Piotroski rescaling.** JPM is scored on 5 signals, PGR and WPC on 7, BKNG on 8 (no gross profit line), the rest on 9, all rescaled to 0-9.
- **Forward growth is distorted for three names.** GOOGL's 2026 consensus EPS (19.57) includes one-off gains (the 2027 estimate is 14.79), so its +81% is overstated. VST's +282% and FCX's +75% start from a depressed 2025. VST and CEG also show extreme EPS surprises from hedge accounting (VST 2021: -1,446%). Ranking by percentile limits the damage, and none of these changes a pick on its own: GOOGL stays on the bench either way.
- **Different fiscal years.** 'Next fiscal year' ends in Nov 2026 for ADBE but Aug or Sep 2027 for COST and FICO, so forward growth isn't measured over the same months for every name.
- **EQIX is scored on EPS**, as the spec says, though FFO is the usual REIT measure. It is rank 22 and would not be picked either way within the AI limit.
- **Qualitative notes** rest on news summaries, not filings, and cover events only up to 13 Nov 2026.
- **Not personal investment advice.** This is a rules-based educational exercise. Claude is not a licensed advisor. Past ratios don't predict returns, a 15-stock fund can lose money, and the buying decision and every order are Rob's.

## Order sheet

Rob places every trade himself. The broker needs fractional shares for all 15 names, including NVO, which is bought as the US-listed ADR.

| Ticker | Company | Action | Amount |
|---|---|---|---|
| VRT | Vertiv | Buy | $8 |
| BKNG | Booking Holdings | Buy | $8 |
| COST | Costco | Buy | $8 |
| LLY | Eli Lilly | Buy | $8 |
| NFLX | Netflix | Buy | $8 |
| FICO | Fair Isaac | Buy | $7 |
| NVO | Novo Nordisk (ADR) | Buy | $7 |
| ADBE | Adobe | Buy | $7 |
| ISRG | Intuitive Surgical | Buy | $7 |
| PGR | Progressive | Buy | $7 |
| VST | Vistra | Buy | $5 |
| FCX | Freeport-McMoRan | Buy | $5 |
| WPC | W. P. Carey | Buy | $5 |
| JPM | JPMorgan Chase | Buy | $5 |
| CEG | Constellation Energy | Buy | $5 |
| **Total** | 15 holdings | | **$100** |

After buying: log every trade in `portfolio/trade_log.csv` (date, ticker, side, quantity, price, fees, and the **USD/GBP rate** on the day, needed for UK and US tax). The purchase date starts the 1-year clock. The first monthly review follows `journal/monthly/TEMPLATE.md`.
