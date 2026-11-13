# How to build a small stock fund properly

Research notes, 13 Nov 2026. Each section ends with what it means for this fund. General information, not financial or tax advice.

---

## 1. Is 15 stocks enough?

- **The classic answer says yes for everyday volatility.** Textbook work finds about 90% of the diversification benefit comes from 12 to 18 stocks, and a 1968 study found benefits mostly exhausted near 10 ([Morningstar](https://my.morningstar.com/my/news/162930/how-many-stocks-would-you-need.aspx)).
- **Newer work says no for long horizons and bad outcomes.** Domian, Louton and Racine (2003) find 8 to 20 stocks may be too few for long-term holders ([Emerald](https://emerald.com/insight/content/doi/10.1108/eb028774/full/html)). Alexeev and Tapon find more than 73 stocks are needed for most of the benefit across five developed markets ([UTAS PDF](https://utas-prod-web.squiz.cloud/__data/assets/pdf_file/0020/436511/2013-16_Alexeev-and-Tapon-Equity-portfolio-diversification.pdf)).
- **Why it matters: returns are skewed.** Bessembinder found that just 4.3% of US stocks created all the net wealth above T-bills from 1926 to 2016, and most single stocks lost to T-bills over their lives ([ASU W. P. Carey](https://wpcarey.asu.edu/department-finance/faculty-research/do-stocks-outperform-treasury-bills)). A 15-stock fund can easily miss the few big winners.

**For this fund:** 15 is fine as long as the 15 are genuinely different bets. Fifteen stocks that all ride one theme behave like three or four. Diversifying across sectors and themes matters more than the stock count. Our pool already has a known trap: 17 of 75 names depend on AI and data-center spending.

## 2. How to weight the 15

- **Concentration alone doesn't win.** Morningstar's study of 5,800 funds found little link between how concentrated a fund is and whether it beats the market ([Morningstar via CFS](https://cfsmanagedaccounts.morningstar.com.au/post/?post=849)).
- **Best ideas do carry the skill.** CFA Institute research on fund holdings finds managers' high-conviction overweights are the only bucket that delivers stock-picking alpha ([CFA Institute blog](https://blogs.cfainstitute.org/investor/2019/10/03/the-active-manager-paradox-high-conviction-overweight-positions)).
- **But big tilts can backfire.** Shrinking the low-conviction names too far can erase the edge ([Klement](https://klementoninvesting.substack.com/p/the-arithmetic-of-high-conviction)). DeMiguel, Garlappi and Uppal (2009, *Review of Financial Studies*) also showed plain 1/N equal weighting is hard to beat with optimized weights, because return estimates are so noisy (from background knowledge, not fetched this session).

**For this fund:** start at equal weight ($6.67 each), then tilt modestly by score. Hard limits: **no stock below $4 or above $10**, and weights in whole dollars that add up to $100. This keeps the best ideas a little bigger without letting one opinion dominate.

## 3. How to pick: factors with evidence behind them

- **Quality / profitability.** Novy-Marx (2013) found gross profit over assets predicts returns about as well as value metrics, and it works best combined with value ([Novy-Marx paper](https://www.ivey.uwo.ca/media/3775548/novy-marx.pdf)).
- **Value plus a financial-health check.** The Piotroski F-score (9 accounting signals) improves value picks by filtering out cheap firms that are deteriorating ([IDEAS/RePEc](https://ideas.repec.org/a/kap/rqfnac/v51y2018i3d10.1007_s11156-017-0689-y.html)).
- **Momentum.** Combining profitability, value and 12-month-minus-1-month momentum was the best long-only mix in Novy-Marx's tests, per a secondary summary ([CXO Advisory](https://www.cxoadvisory.com/fundamental-valuation/optimal-quality-and-value-combination/)).
- **Caveat:** popular factors can get crowded, which lowers future returns ([HumbleDollar](https://humbledollar.com/money-guide/profitability-effect/)).

**For this fund:** score every company on quality, value, balance sheet and growth, plus momentum if a price history is available. Rank companies only against their own sector, because a bank and a software firm can't be judged on the same ratios. Full rules are in [`03_methodology/scoring-framework.md`](../03_methodology/scoring-framework.md).

## 4. Write the rules down first (Investment Policy Statement)

Professional funds run on a short written policy: goal, horizon, risk limits, how picks are made, when to rebalance and when to sell. Its job is to commit you in advance to the uncomfortable trades, like holding through a drawdown or trimming a winner ([Beancount guide](https://beancount.io/blog/2026/10/25/investment-policy-statement-explained-goals-risk-allocation-rebalancing-guide); [Evensky template](https://resources.evensky.com/hubfs/Basic%20Guide%20For%20Building%20An%20Investment%20Policy%20Statement.pdf)). Common practice is a calendar review plus a drift threshold: check quarterly, rebalance only when a position has drifted past a band ([Ryan O'Connell](https://ryanoconnellfinance.com/portfolio-rebalancing/)).

**For this fund:** a draft IPS is in [`02_policy/investment-policy-statement.md`](../02_policy/investment-policy-statement.md). Two blanks need your answers: time horizon and benchmark.

## 5. Practical setup with $100

- **You need fractional shares.** $6.67 won't buy one share of most of these companies.
- **Broker coverage differs a lot.** Schwab's Stock Slices covers only S&P 500 stocks, from $5. Per IBKR's table, Interactive Brokers covers about 10,500 US names and Fidelity about 7,000 ([NerdWallet](https://nerdwallet.com/investing/best/best-brokers-for-fractional-shares); [IBKR](https://interactivebrokers.ie/en/trading/fractional-trading.php)). **This matters:** the ADRs in our pool (SAP, TSM, SONY, NVO, SHEL, TTE) are not in the S&P 500, so Schwab can't buy them fractionally.
- **Costs.** At $100, a $1 commission is 1% of the whole fund. Use a $0-commission broker, and watch the currency-conversion fee if you fund the account in pounds.
- **Fractional shares carry no voting rights** at IBKR ([IBKR](https://interactivebrokers.ie/en/trading/fractional-trading.php)). Small point, but true.

## 6. Tax: US citizen living in the UK

- **Hold individual stocks, not non-US funds.** Almost any non-US pooled fund counts as a PFIC for US tax, which is punishing. Directly held stocks generally do not ([Experts for Expats](https://www.expertsforexpats.com/advice/expat-money-and-finance/investment-options-for-american-citizens-living-in-the-uk); [Schroders](https://www.schroders.com/en-us/us/wealth-management/insights/why-is-it-so-difficult-for-us-citizens-to-invest-while-living-in-the-uk/)). A 15-stock fund avoids the problem by design.
- **The two countries count cost basis differently.** The US uses FIFO lot matching; the UK uses an averaged pool ([Buzzacott](https://www.buzzacott.co.uk/insights/stepping-stones-tax-on-investments-for-americans-in-the-uk)). Keep a full trade log (`portfolio/trade_log.csv`) with dates, quantities, prices and the USD/GBP rate.
- **Broker eligibility is unconfirmed.** I couldn't confirm whether Schwab or Fidelity open accounts for a US citizen with a UK address. Check with the broker directly. IBKR onboards internationally.
- At $100 the tax amounts are tiny, but the record-keeping habits are worth building now. A cross-border tax adviser should confirm anything before real money scales up.

## 7. Process lessons from professional funds

1. **Use one data date.** Pull every Bloomberg report on the same day, or the valuations aren't comparable. The 75-name notes were stale for exactly this reason.
2. **Screen before you study.** Use cheap, uniform metrics to cut 75 to 25, then do the deep work on 25 only.
3. **Write the thesis and the sell trigger at purchase.** Record why each stock is held and what would prove you wrong (`journal/`).
4. **Compare against a benchmark.** Without one you can't tell skill from market drift. The S&P 500 (or an equal-weight version) is the natural yardstick.
5. **Review on a calendar, not on the news.** Quarterly reviews, with a written decision log.
