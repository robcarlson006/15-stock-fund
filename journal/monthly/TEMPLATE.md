# Monthly review: YYYY-MM

Copy this file to `YYYY-MM.md` in the first week of each month. Rules: `03_methodology/scoring-framework.md`, Stage 4, and the IPS sections 6 and 7.
Rules-based output, not personal advice. Rob places every trade.

**Review date:** · **Data pull date (one date for all 25):** · **Months since first purchase:** of 12

## 0. Data Rob pulls (all 25 names, one date)
- [ ] Last price, 1-month and 12-month total return (plus SPX total return)
- [ ] Current P/E, EV/EBITDA, FCF yield
- [ ] Consensus EPS for the next 12 months, and its change over the month
- [ ] Any new quarterly results (full Bloomberg report only for companies that have just reported)
- [ ] Current value of each holding from the broker
- Saved in: `data/monthly/YYYY-MM/`

## 1. Performance
| | This month | Since inception |
|---|---|---|
| Fund (after fees) | | |
| S&P 500 total return | | |
| Difference | | |

Fund value: $ · Biggest contributors: · Biggest detractors:

## 2. Sell triggers and red flags (any hit = remove)
Triggers are in `portfolio/target_allocation.csv`. Red flags: negative FCF 2 of 3 years, net debt/EBITDA above 4.0x, interest coverage below 3x (sector exemptions apply), falling EPS with shrinking revenue, being acquired.

| Ticker | Sell trigger | Hit? | Evidence |
|---|---|---|---|
| | | | |

## 3. Re-score all 25
Same pillars and checks. Momentum and value update every month; quality, balance sheet, growth and the Stage 2 checks only change when new results come out.

| Rank | Ticker | Held or bench | Score last month | Score now | Change | Note |
|---|---|---|---|---|---|---|
| | | | | | | |

## 4. Swap test
A holding is replaced when a bench name in a permitted slot beats it by 15 points or more at two reviews in a row. Maximum 3 swaps a month. The portfolio limits still apply (3 per sector, 4 AI/data-center, 2 oil, 3 income, 3 ADRs, 7 sectors).

| Bench name | Holding it would replace | Gap now | Gap last month | Two in a row? | Fits the limits? | Swap? |
|---|---|---|---|---|---|---|
| | | | | | | |

Names 15 points ahead for the first time this month (watch next month):

## 5. Reweight
Rerun Stage 3 on the new ranks: top 5 get 8%, middle 5 get 7%, bottom 5 get 5% of the fund's current value. Caps: each position 4% to 10%, sector 25%, AI/data-center 30%.
Skip any trade where the position is within $0.50 of target (or 0.5% of fund value once it grows).

| Ticker | Rank | Current value | Target | Difference | Trade? |
|---|---|---|---|---|---|
| | | | | | |

Run `/usr/local/bin/python3 -I tools/check_portfolio.py` after updating `portfolio/target_allocation.csv`. Note: it checks a $100 total, so check the percentages if the fund value has moved.

## 6. Orders
| Ticker | Buy or sell | Amount | Reason |
|---|---|---|---|
| | | | |

- [ ] Rob placed the orders
- [ ] Logged in `portfolio/trade_log.csv` with the USD/GBP rate
- [ ] Decisions and any rule changes logged in `journal/decision-log.md`

## 7. Notes
What changed in the theses this month, and anything to watch next month.
