#!/usr/bin/env python3
"""Write the Stage 2 + 3 investment committee memo: analysis/stage2_25_to_15/final_15.md.

Usage (from the project root): /usr/local/bin/python3 -I tools/write_final15.py
Every number comes from scores_stage2.csv, robustness_stage2.csv, Stage 1 scores.csv or target_allocation.csv.
Prose (theses, risks, sell triggers, qualitative notes, sources) comes from tools/stage2_notes.py.
"""
import contextlib
import io
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_stage2 as S
import check_portfolio as C
from stage2_notes import COMPANY, QUAL, HOLD, SOURCES

A2 = "analysis/stage2_25_to_15"
s = pd.read_csv(f"{A2}/scores_stage2.csv")
s1 = pd.read_csv("analysis/stage1_75_to_25/scores.csv").set_index("ticker")
alloc = pd.read_csv("portfolio/target_allocation.csv")
rob = pd.read_csv(f"{A2}/robustness_stage2.csv").fillna("")
usd = dict(zip(alloc.ticker, alloc.target_usd))
sel = s[s.status == "selected"]
bench = s[s.status != "selected"]
picked = list(sel.ticker)
CHECK_NAME = {"chk_fscore": "Piotroski", "chk_earnings_quality": "earnings quality", "chk_sbc_fcf_yield": "cash yield after stock pay",
              "chk_strength": "financial strength", "chk_delivery": "earnings delivery", "chk_fwd_growth": "forward growth"}
f1 = lambda v, suf="": "n/a" if pd.isna(v) else f"{v:.1f}{suf}"
f2 = lambda v, suf="": "n/a" if pd.isna(v) else f"{v:.2f}{suf}"
f0 = lambda v: "n/a" if pd.isna(v) else f"{v:.0f}"


def key_numbers(t):
    a, b = s1.loc[t], s.set_index("ticker").loc[t]
    out = []
    if pd.notna(a.roic_latest) and a.kind in ("standard", "utility"):
        out.append(f"ROIC {a.roic_latest:.1f}%")
    elif pd.notna(a.roe_latest):
        out.append(f"ROE {a.roe_latest:.1f}%")
    if pd.notna(a.p_ffo_vs_hist):
        out.append(f"P/FFO {a.p_ffo_now:.1f}x ({a.p_ffo_vs_hist:.2f}x own history)")
    elif pd.notna(a.pe_now):
        out.append(f"P/E {a.pe_now:.1f}x ({a.pe_vs_hist:.2f}x own history)")
    if pd.notna(b.sbc_adj_fcf_yield):
        out.append(f"FCF yield after stock pay {b.sbc_adj_fcf_yield:.1f}%")
    out.append(f"Piotroski {b.f_score_0_9:.1f}/9")
    out.append(f"{'FFO' if t == 'WPC' else 'EPS'} beats {int(b.beats_of_4)}/4")
    if pd.notna(b.fwd_eps_growth_pct):
        out.append(f"consensus {'FFO' if t == 'WPC' else 'EPS'} growth {b.fwd_eps_growth_pct:+.0f}%")
    return ", ".join(out)


def would_block(t):
    """Limits a bench name would hit if a place opened up with the current 15 minus nobody."""
    r = s.set_index("ticker").loc[t]
    why = []
    if (sel.sector == r.sector).sum() >= 3:
        why.append(f"sector limit (3 {r.sector} names held)")
    if t in S.AI and sel.ticker.isin(S.AI).sum() >= 4:
        why.append("AI/data-center limit (4 held)")
    return why


def weakest(t, n=2):
    r = s.set_index("ticker").loc[t][S.CHECKS].dropna().astype(float).sort_values()
    return ", ".join(f"{CHECK_NAME[k]} ({v:.0f})" for k, v in r.iloc[:n].items())


def strongest(t, n=2):
    r = s.set_index("ticker").loc[t][S.CHECKS].dropna().astype(float).sort_values(ascending=False)
    return ", ".join(f"{CHECK_NAME[k]} ({v:.0f})" for k, v in r.iloc[:n].items())


# what-if: score check 3 for PGR, WPC, EQIX as well
wm = S.build(score_fcf_all=True)
w_out, w_pick = S.select(wm, 0.6)
w_in, w_outn = sorted(set(w_pick) - set(picked)), sorted(set(picked) - set(w_pick))

with contextlib.redirect_stdout(io.StringIO()) as buf:
    rc = C.main()
check_text = buf.getvalue().rstrip()
if rc != 0:
    raise SystemExit("check_portfolio failed; memo not written\n" + check_text)

cut15 = sel.stage2_score.min()
border = list(sel[sel.borderline].ticker)
sec_tab = alloc.groupby("sector").agg(names=("ticker", lambda x: ", ".join(x)), n=("ticker", "count"), usd=("target_usd", "sum")).sort_values("usd", ascending=False)
ai = alloc[alloc.ticker.isin(S.AI)]
L = []
L += ["# Final 15 and dollar weights: investment committee memo", "",
      "**Fund:** My own investment fund ($100, 15 stocks, 1-year horizon, benchmark S&P 500 total return, monthly review)  ",
      "**Data:** Bloomberg Financial Statement Analysis. Stage 1 (75 names) and Stage 2 (25 names) both pulled 13 Nov 2026  ",
      "**Method:** `03_methodology/scoring-framework.md`, Stages 2 and 3. The Stage 2 scoring spec was written into the framework before any result was computed (decision log, 13 Nov 2026)  ",
      "**Status:** for Rob's approval. This is the output of the written rules, not personal investment advice. Rob places every trade himself.", "",
      "## Summary", "",
      f"- **The 15:** {', '.join(picked)}. They cover {alloc.sector.nunique()} sectors. No portfolio limit blocked any name: the top 15 by Stage 2 score all fit.",
      f"- **Dollars:** $8 each for the top 5 ({', '.join(picked[:5])}), $7 for the middle 5 ({', '.join(picked[5:10])}), $5 for the bottom 5 ({', '.join(picked[10:])}). No cap binds, so no dollars were moved. Total $100.",
      f"- **The last place was close.** {picked[-1]} ({cut15:.2f}) beat {bench.ticker.iloc[0]} ({bench.stage2_score.iloc[0]:.2f}) and {bench.ticker.iloc[1]} ({bench.stage2_score.iloc[1]:.2f}) by less than half a point.",
      f"- **Robustness:** {rob.kept_from_base.iloc[1]} of 15 survive an 80/20 split and {rob.kept_from_base.iloc[2]} of 15 survive 40/60. Borderline: {', '.join(border)}. The other {15 - len(border)} are picked under all three splits.",
      f"- **One scoring choice changes one name.** The spec skips the cash-yield check for REITs and the insurer. If it were scored for them, {', '.join(w_outn)} would drop out and {', '.join(w_in)} would come in. See 'Decisions for Rob'.",
      "- **No qualitative overrides.** The news check found no takeover of any of the 25, no restatement and no large guidance cut.",
      "- **Two overlapping bets are both in the 15:** LLY with NVO (GLP-1 drugs) and CEG with VST (power for data centers). These are flagged for Rob, not enforced, because the correlation limit can't be checked without price data.",
      "- **Not scored:** momentum and correlations (no price file). For a 1-year horizon that is the biggest gap in this work.", "",
      "## The 15", "",
      "Scores are out of 100. Stage 2 score = 60% Stage 1 score + 40% Stage 2 checks.", "",
      "| # | Ticker | Company | Sector | Theme | $ | Stage 1 | Checks | **Stage 2** | Key numbers |",
      "|---|---|---|---|---|---|---|---|---|---|"]
for _, r in alloc.iterrows():
    b = s.set_index("ticker").loc[r.ticker]
    L.append(f"| {r.stage2_rank} | **{r.ticker}**{' †' if b.borderline else ''} | {r.company} | {r.sector} | {r.theme_tag if isinstance(r.theme_tag, str) else ''} | "
             f"**${r.target_usd}** | {b.stage1_score:.1f} | {b.stage2_checks:.1f} | **{b.stage2_score:.1f}** | {key_numbers(r.ticker)} |")
L += ["", "† Borderline: not picked under both alternative splits.", "",
      "## Each holding: thesis, risk and sell trigger", ""]
for _, r in alloc.iterrows():
    one, thesis, risk, trig = HOLD[r.ticker]
    L += [f"### {r.stage2_rank}. {r.ticker}, {r.company}: ${r.target_usd}", "",
          f"- **Thesis:** {thesis}", f"- **Key risk:** {risk}", f"- **Sell trigger:** {trig}", ""]

L += ["## Portfolio shape and limits", "",
      "| Sector | Names | Count | Dollars |", "|---|---|---|---|"]
for sec, r in sec_tab.iterrows():
    L.append(f"| {sec} | {r.names} | {r.n} | ${r.usd} |")
L += ["", "| Limit | Rule | Actual | Result |", "|---|---|---|---|",
      f"| Holdings | exactly 15 | {len(alloc)} | Pass |",
      f"| Sectors | at least 7 | {alloc.sector.nunique()} | Pass |",
      f"| Names per sector | at most 3 | {sec_tab.n.max()} (Health Care) | Pass |",
      f"| Dollars per sector | at most $25 | ${sec_tab.usd.max()} ({sec_tab.usd.idxmax()}) | Pass |",
      f"| AI/data-center names | at most 4 | {len(ai)} ({', '.join(ai.ticker)}) | Pass, at the limit |",
      f"| AI/data-center dollars | at most $30 | ${ai.target_usd.sum()} | Pass |",
      "| Oil-linked names | at most 2 | 0 | Pass |",
      f"| Rate-sensitive income names | at most 3 | {alloc.ticker.isin(S.INCOME).sum()} (WPC) | Pass |",
      f"| Non-US ADRs | at most 3 | {alloc.ticker.isin(S.ADR).sum()} (NVO) | Pass |",
      f"| Position size | $4 to $10 | ${alloc.target_usd.min()} to ${alloc.target_usd.max()} | Pass |",
      "| Pair correlation | none above 0.85 | not checkable (no price data) | Flagged below |", "",
      "**Overlapping bets (flagged, not enforced):**", "",
      f"- **LLY (${usd['LLY']}) and NVO (${usd['NVO']}):** both depend on GLP-1 obesity and diabetes drugs, and on US drug pricing. Together ${usd['LLY'] + usd['NVO']}.",
      f"- **CEG (${usd['CEG']}) and VST (${usd['VST']}):** both are merchant power producers tied to data-center demand, and both count toward the AI limit. Together ${usd['CEG'] + usd['VST']}.",
      "- **COST and TJX:** only COST is held, so this overlap doesn't arise.",
      f"- **AI/data-center as a whole:** {', '.join(ai.ticker)} = ${ai.target_usd.sum()} of $100. META, GOOGL and EQIX are on the bench and can't be added while these four are held.", "",
      "## Stage 2 checks: the numbers for all 25", "",
      "Each check is a percentile across the 25 (100 = best). 'n/a' means the check doesn't apply and was skipped, not scored as zero.", "",
      "| # | Ticker | Stage 1 | Piotroski | Earnings quality | Cash yield after stock pay | Strength | Delivery | Fwd growth | Checks used | Checks | **Stage 2** | Status |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for _, r in s.iterrows():
    L.append(f"| {r.stage2_rank} | {r.ticker} | {r.stage1_score:.1f} | {f0(r.chk_fscore)} | {f0(r.chk_earnings_quality)} | {f0(r.chk_sbc_fcf_yield)} | {f0(r.chk_strength)} | "
             f"{f0(r.chk_delivery)} | {f0(r.chk_fwd_growth)} | {r.checks_used} | {r.stage2_checks:.1f} | **{r.stage2_score:.1f}** | {'Selected' if r.status == 'selected' else 'Bench'} |")
L += ["", "The raw metrics behind the percentiles:", "",
      "| Ticker | Fiscal year | Piotroski (signals used) | Adj vs GAAP gap, 5y | Stock pay % revenue | FCF yield | after stock pay | Altman Z | Current ratio | Avg EPS surprise, 4y | Beats | Fwd EPS growth |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for _, r in s.iterrows():
    L.append(f"| {r.ticker} | {r.fiscal_year} | {r.f_score_0_9:.1f} ({r.f_points}/{r.f_signals_used}) | {f1(r.adj_gaap_gap_5y_pct, '%')} | {f1(r.sbc_pct_revenue, '%')} | {f1(r.fcf_yield_s1, '%')} | "
             f"{f1(r.sbc_adj_fcf_yield, '%')} | {f1(r.altman_z)} | {f2(r.current_ratio)} | {f1(r.surprise_avg_4y_pct, '%')} | {int(r.beats_of_4)}/4 | {f1(r.fwd_eps_growth_pct, '%')} |")
L += ["", "Full detail, including which Piotroski signals each company passed and failed, is in `scores_stage2.csv`.", "",
      "## Robustness", "",
      "The selection was re-run with the Stage 1 / Stage 2 split moved either way.", "",
      "| Split (Stage 1 / checks) | Of the base 15 kept | Comes in | Drops out |", "|---|---|---|---|"]
for _, r in rob.iterrows():
    L.append(f"| {r['split']} | {r.kept_from_base} of 15 | {r.added or 'none'} | {r.dropped or 'none'} |")
L += ["", f"- **Borderline holdings:** {', '.join(border)}. FCX and JPM rely on their Stage 2 checks; VST and CEG rely on their Stage 1 scores.",
      f"- **Solid:** the other {15 - len(border)} are picked under all three splits.",
      "- **First in line from the bench:** TJX and HSY (40/60), META and LIN (80/20).", "",
      "**What if the cash-yield check were scored for the insurer and the REITs?** The spec skips it for PGR, WPC and EQIX (and JPM has no free cash flow at all). Scoring it anyway:", "",
      "| Ticker | Stage 2 score as specified | Rank | If scored | Rank |", "|---|---|---|---|---|"]
wo = w_out.set_index("ticker")
for t in ["PGR", "WPC", "EQIX", "CEG", "TJX"]:
    b = s.set_index("ticker").loc[t]
    L.append(f"| {t} | {b.stage2_score:.2f} | {b.stage2_rank} | {wo.loc[t].stage2_score:.2f} | {wo.loc[t].stage2_rank} |")
L += ["", f"Result: {', '.join(w_outn)} out, {', '.join(w_in)} in. The other 14 are unchanged. PGR would move up to rank {wo.loc['PGR'].stage2_rank} and into the $8 group, with "
      f"{[t for t in picked[:5] if wo.loc[t].stage2_rank > 5][0]} moving down to $7.", "",
      "## The bench (in rank order)", "",
      "These 10 are watched every month and are the only names that can be swapped in (Stage 4).", "",
      "| Rank | Ticker | Company | Sector | Stage 1 | Checks | Stage 2 | Gap to 15th place | Limits it would hit today |", "|---|---|---|---|---|---|---|---|---|"]
for _, r in bench.iterrows():
    L.append(f"| {r.stage2_rank} | {r.ticker} | {COMPANY[r.ticker]} | {r.sector} | {r.stage1_score:.1f} | {r.stage2_checks:.1f} | {r.stage2_score:.1f} | {r.stage2_score - cut15:+.1f} | {'; '.join(would_block(r.ticker)) or 'none'} |")
L += ["", "## Every cut name and why", "",
      "No name was cut by a portfolio limit or a qualitative override. All 10 were cut on score: the 15 places were filled before the walk down the ranking reached them.", "",
      "| Ticker | Stage 2 score | Reason | Strongest checks | Weakest checks |", "|---|---|---|---|---|"]
for _, r in bench.iterrows():
    extra = would_block(r.ticker)
    reason = f"Rank {r.stage2_rank}: {cut15 - r.stage2_score:.1f} points below the 15th place"
    if extra:
        reason += f". Would also be blocked by the {' and the '.join(extra)}"
    L.append(f"| {r.ticker} | {r.stage2_score:.1f} | {reason} | {strongest(r.ticker)} | {weakest(r.ticker)} |")

L += ["", "## Qualitative check: all 25", "",
      "**How current this is:** Claude's own knowledge of these companies runs to roughly mid-2026. Anything later comes from web searches run on 13 Nov 2026, listed under Sources. "
      "Those are mostly news summaries of company releases and were not checked against the filings. For GOOGL, TJX, YUM, SYK and JNJ no third-quarter news was verified.", "",
      "**Overrides:** none. An override needs a specific event such as a pending takeover, a restatement or a large guidance cut, and none was found. "
      "Three items came close and are worth knowing: FICO withheld fiscal 2027 guidance; Novo Nordisk will cut US list prices by about 50% (Wegovy) and 35% (Ozempic) from January 2027; Booking guided Q4 room-night growth down to 1-3%. "
      "None is a broken thesis under the rules, and each is covered by that holding's sell trigger.", ""]
for t in list(s.ticker):
    moat, brk, cat, cap, src = QUAL[t]
    r = s.set_index("ticker").loc[t]
    refs = " ".join(f"[{SOURCES[k][0]}, {SOURCES[k][1]}]({SOURCES[k][2]})" for k in src)
    L += [f"**{r.stage2_rank}. {t}, {COMPANY[t]}** ({'held, $' + str(usd[t]) if t in usd else 'bench'}). *Moat:* {moat} *What would break it:* {brk} *Next 12 months:* {cat} *Capital allocation:* {cap}"
          + (f" *Source:* {refs}" if refs else ""), ""]

L += ["## Decisions for Rob", "",
      f"1. **WPC or TJX for one $5 place.** The brief said to skip a check that doesn't apply, and named only the bank for the cash-yield check. Before computing anything, the spec extended that to the insurer and the two REITs, "
      "because Stage 1 already treats free cash flow as not meaningful for those sectors (a REIT's 'free cash flow' subtracts property purchases). That choice was logged first, but it does decide this place: "
      f"as specified WPC is in at rank {s.set_index('ticker').loc['WPC'].stage2_rank}; with the check scored, WPC falls to rank {wo.loc['WPC'].stage2_rank} and TJX comes in. The allocation file follows the spec (WPC). Say the word and it is switched and logged.",
      "2. **Keep both names in each overlapping pair, or swap one out?** LLY/NVO and CEG/VST. The rules flag these but don't force a change. If you want to cut an overlap, the lower-scored name in each pair is NVO (rank 7) and CEG (rank 15), and the first bench names are TJX and HSY.",
      "3. **Price data.** Stage 2 ran without momentum or correlations. The first monthly review (Stage 4) needs prices in any case. `data/stage2_25_companies/prices_monthly.xlsx` is ready to refresh on the Bloomberg terminal. "
      "If you pull it before buying, momentum and the 0.85 correlation limit can be applied first.",
      "4. **Broker.** It must offer fractional shares for all 15, including the NVO ADR, to a US citizen with a UK address.", "",
      "## Verification", "",
      "Output of `/usr/local/bin/python3 -I tools/check_portfolio.py` (exit code 0):", "", "```", check_text, "```", "",
      "## Data notes and caveats", "",
      "- **No momentum, no correlations.** No price history was pulled, so the Momentum pillar (20% in the framework) is not scored and the 0.85 pair-correlation limit is not checked. Theme limits and the flagged overlaps stand in for it. No prices from other sources were used.",
      "- **One date.** Valuations are as of 13 Nov 2026. They will have moved by the time orders are placed.",
      "- **Stock-pay data gaps.** CEG has no SBC page and GE's SBC rows stop at 2022. For both, earnings quality uses the adjusted-vs-GAAP gap only and the cash yield is not reduced for stock pay. Neither result changes a selection: GE is rank 21.",
      "- **Skipped checks.** JPM, PGR and WPC are scored on 4 checks (no cash yield, no Altman Z or current ratio); EQIX on 5. Their checks score rests on fewer measures and is less reliable.",
      "- **Piotroski rescaling.** JPM is scored on 5 signals, PGR and WPC on 7, BKNG on 8 (no gross profit line), the rest on 9, all rescaled to 0-9.",
      "- **Forward growth is distorted for three names.** GOOGL's 2026 consensus EPS (19.57) includes one-off gains (the 2027 estimate is 14.79), so its +81% is overstated. "
      "VST's +282% and FCX's +75% start from a depressed 2025. VST and CEG also show extreme EPS surprises from hedge accounting (VST 2021: -1,446%). Ranking by percentile limits the damage, and none of these changes a pick on its own: GOOGL stays on the bench either way.",
      "- **Different fiscal years.** 'Next fiscal year' ends in Nov 2026 for ADBE but Aug or Sep 2027 for COST and FICO, so forward growth isn't measured over the same months for every name.",
      "- **EQIX is scored on EPS**, as the spec says, though FFO is the usual REIT measure. It is rank 22 and would not be picked either way within the AI limit.",
      "- **Qualitative notes** rest on news summaries, not filings, and cover events only up to 13 Nov 2026.",
      "- **Not personal investment advice.** This is a rules-based educational exercise. Claude is not a licensed advisor. Past ratios don't predict returns, a 15-stock fund can lose money, and the buying decision and every order are Rob's.", "",
      "## Order sheet", "",
      "Rob places every trade himself. The broker needs fractional shares for all 15 names, including NVO, which is bought as the US-listed ADR.", "",
      "| Ticker | Company | Action | Amount |", "|---|---|---|---|"]
for _, r in alloc.iterrows():
    L.append(f"| {r.ticker} | {r.company} | Buy | ${r.target_usd} |")
L += [f"| **Total** | 15 holdings | | **${alloc.target_usd.sum()}** |", "",
      "After buying: log every trade in `portfolio/trade_log.csv` (date, ticker, side, quantity, price, fees, and the **USD/GBP rate** on the day, needed for UK and US tax). "
      "The purchase date starts the 1-year clock. The first monthly review follows `journal/monthly/TEMPLATE.md`.", ""]
open(f"{A2}/final_15.md", "w").write("\n".join(L))
print(f"wrote {A2}/final_15.md ({len(L)} lines)")
