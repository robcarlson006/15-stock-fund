#!/usr/bin/env python3
"""Write analysis/stage1_75_to_25/shortlist_25.md from scores.csv, metrics.csv, sensitivity.csv and the pool.
Usage: python3 -I tools/write_shortlist.py   (run from the project root)"""
import pandas as pd

A = "analysis/stage1_75_to_25"
s = pd.read_csv(f"{A}/scores.csv")
m = pd.read_csv(f"{A}/metrics.csv")
sens = pd.read_csv(f"{A}/sensitivity.csv").set_index("ticker").times_selected_of_6
pool = pd.read_csv("00_context/candidate_pool_75.csv").set_index("ticker")
mi = m.set_index("ticker")


def f(x, fmt="{:.1f}", suf=""):
    return "–" if pd.isna(x) else fmt.format(x) + suf


def keynums(t):
    r = mi.loc[t]
    if r.sector == "Financials":
        return (f"ROE {f(r.roe_latest, suf='%')}, P/E {f(r.pe_now)}x ({f(r.pe_vs_hist, '{:.2f}')}× own history), "
                f"P/B {f(r.pb_now)}x, rev growth {f(r.rev_cagr_3y, suf='%')}/yr")
    val = r.p_ffo_vs_hist if pd.notna(r.p_ffo_vs_hist) else r.ev_ebitda_vs_hist
    vlab = "P/FFO" if pd.notna(r.p_ffo_vs_hist) else "EV/EBITDA"
    return (f"ROIC {f(r.roic_latest, suf='%')}, {vlab} {f(val, '{:.2f}')}× own history, FCF yield {f(r.fcf_yield, suf='%')}, "
            f"net debt/EBITDA {f(r.net_debt_ebitda)}x, rev growth {f(r.rev_cagr_3y, suf='%')}/yr")


sel = s[s.selected].sort_values("score", ascending=False).reset_index(drop=True)
L = []
L += ["# Stage 1 shortlist: 75 → 25", "",
      "**Fund:** My own investment fund ($100, 15 stocks, 1-year horizon, benchmark S&P 500 total return)  ",
      "**Data:** Bloomberg Financial Statement Analysis, all 75 pulled 13 Nov 2026  ",
      "**Method:** `03_methodology/scoring-framework.md`, Stage 1 (amendments in `journal/decision-log.md`)  ",
      "**Status:** for Rob's review. Rules-based output, not personal investment advice.", "",
      "## Summary", ""]
ai = sel[sel.theme.fillna("").str.startswith("AI")]
L += [f"- **59 of 75 passed the red-flag checks**, and the 25 below were selected from them, covering {sel.sector.nunique()} sectors. Energy is absent: all five oil names failed the falling-earnings check.",
      f"- **The shortlist is robust:** {int((sens[sel.ticker] == 6).sum())} of the 25 are selected under all six weightings tested, and {int((sens[sel.ticker] >= 4).sum())} under at least four. Borderline: "
      + ", ".join(f"{t} ({sens[t]}/6)" for t in sel.ticker if sens[t] < 4) + ".",
      f"- **AI/data-center exposure is at its cap of 7** ({', '.join(ai.ticker)}). TSMC and Caterpillar scored high enough to be included but were blocked by that cap.",
      "- **Momentum is not scored.** No price file was pulled, so the other four pillars were scaled up proportionally (Quality 37.5%, Value 25%, Balance sheet 18.75%, Growth 18.75%). Price history should be pulled at Stage 2.",
      ""]
L += ["## The 25", "",
      "Pillar scores are percentiles within the company's own sector (100 = best in sector). \"Stable\" counts how many of the six weight sets also select the name.", "",
      "| # | Ticker | Company | Sector | Theme | Quality | Value | Bal. sheet | Growth | **Score** | Stable | Why in | Key numbers |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for i, r in sel.iterrows():
    L.append(f"| {i+1} | **{r.ticker}** | {pool.loc[r.ticker,"company"].replace(" (fill)","")} | {r.sector} | {r.theme if pd.notna(r.theme) else ''} | "
             f"{r.Quality:.0f} | {r.Value:.0f} | {r['Balance sheet']:.0f} | {r.Growth:.0f} | **{r.score:.1f}** | {sens[r.ticker]}/6 | "
             f"{r.selection_reason} | {keynums(r.ticker)} |")
L += ["", "## Shape of the 25", ""]
cnt = sel.groupby("sector").size().sort_values(ascending=False)
L += ["| Sector | Names |", "|---|---|"] + [f"| {k} | {v} |" for k, v in cnt.items()] + [""]
L += [f"- **Themes:** AI/data-center {len(ai)} (direct: {', '.join(sel[sel.theme=='AI direct'].ticker)}; adjacent: {', '.join(sel[sel.theme=='AI adjacent'].ticker)}). Oil 0.",
      f"- **Non-US listings:** {', '.join(t for t in sel.ticker if t in {'SAP','SONY','TSM','NVO','SHEL','TTE'}) or 'none'} (buy as the US ADR).",
      "- **Rate-sensitive income names:** WPC, EQIX (REITs); CEG and VST are merchant power producers rather than regulated utilities.",
      "- **Clusters to manage at Stage 2:**",
      "  - CEG, VST, VRT, META and GOOGL all depend on data-center demand.",
      "  - LLY and NVO are both GLP-1 obesity-drug bets.",
      "  - TJX and COST both depend on consumers trading down to value.",
      ""]
L += ["## Borderline names and alternates", "",
      "Names whose place depends on the weighting, and the first names that would replace them:", ""]
alts = sens[(~sens.index.isin(sel.ticker))].sort_values(ascending=False)
L += ["| In the 25, but borderline | Stable | Score |", "|---|---|---|"] + \
     [f"| {t} | {sens[t]}/6 | {s.set_index('ticker').score[t]:.1f} |" for t in sel.ticker if sens[t] < 4] + [""]
size = s.groupby("sector").ticker.count()
si = s.set_index("ticker")
top_half = lambda t: si.sector_rank[t] <= -(-size[si.sector[t]] // 2)
blocked = {t for t in si.index[~si.selected] if str(si.theme[t]).startswith("AI") and top_half(t)
           and si.score[t] >= si.score[si.selected].min()}
L += ["| First alternates (not in the 25) | Picked under | Score | Note |", "|---|---|---|---|"]
for t, n in alts.head(8).items():
    sc = si.score.get(t)
    note = "blocked by AI cap" if t in blocked else "" if top_half(t) else "bottom half of sector"
    L.append(f"| {t} | {n}/6 weightings | {sc:.1f} | {note} |")
L += ["", "## Every cut name and why", "", "### Failed a red-flag check (16)", "",
      "| Ticker | Sector | Reason |", "|---|---|---|"]
for _, r in m[m.red_flags.notna()].iterrows():
    L.append(f"| {r.ticker} | {r.sector} | {r.red_flags} |")
L += ["", "### Passed the checks, not selected (34)", "",
      "| Ticker | Sector | Score | Rank in sector | Reason |", "|---|---|---|---|---|"]
for _, r in s[~s.selected].sort_values("score", ascending=False).iterrows():
    if r.ticker in blocked:
        why = "Would qualify, but the AI/data-center cap (7) was already full"
    elif r.sector_rank > -(-size[r.sector] // 2):
        why = "Bottom half of its sector"
    else:
        why = "Top half of sector, but outscored for the last open places"
    L.append(f"| {r.ticker} | {r.sector} | {r.score:.1f} | {r.sector_rank} of {size[r.sector]} | {why} |")
L += ["", "## How the scoring worked", "",
      "1. **Checks:** red-flag rules removed 16 names. Utilities and REITs are exempt from the FCF and interest-coverage rules (agreed 13 Nov).",
      "2. **Within-sector percentiles:** each metric was ranked only against the company's sector peers, so a bank is never compared with a software firm.",
      "3. **Pillars:**",
      "   - Quality: ROIC, gross profit/assets, margin trend, FCF conversion.",
      "   - Value: EV/EBITDA and P/E vs the company's own 5-year history, FCF yield, shareholder yield.",
      "   - Balance sheet: net debt/EBITDA, interest coverage.",
      "   - Growth: 3-year revenue and EPS growth.",
      "   - Financials use ROE level and stability, P/E vs history, P/B relative to ROE, and capital strength.",
      "   - REITs use P/FFO vs history.",
      "4. **Selection:** the top 2 in each sector, then the best remaining scores from the top half of their sector, with at most 7 AI/data-center names.",
      "5. **Robustness:** re-run under six weightings (base, equal, quality-heavy, value-heavy, growth-heavy, and the original pre-momentum weights).",
      "",
      "**Data adjustments** (details in `extraction_notes.md`):",
      "- The history baseline is the median of five yearly averages, so a freak year like Booking's 2021 COVID multiple can't distort it.",
      "- Normalised EPS was used where the latest 12 months contain a one-off (YUM, MRK, SNPS, NEE, MOS).",
      "- GE's revenue growth is measured after its spin-offs.",
      "",
      "## Caveats", "",
      "- **Backward-looking:** Stage 1 uses reported accounts and multiples, with no view yet on moats, catalysts or management. That is Stage 2's job.",
      "- **One date:** valuations are as of 13 Nov 2026 and will move.",
      "- **No momentum:** for a 1-year horizon, that is the largest gap in this screen.",
      "",
      "## What to pull for Stage 2 (the 25 names)", "",
      "1. **Price history:** 3 years of month-end total-return prices for the 25, plus SPX, in one sheet. Bloomberg `HP` per name, or Excel `BDH(\"<ticker> US Equity\",\"TOT_RETURN_INDEX_GROSS_DVDS\",start,end,\"Per=M\")`. This gives momentum, correlations and the benchmark comparison.",
      "2. **Templates not pulled yet:** Bal Sheet – Standardized, Income – GAAP, Ratios – DuPont, Key Stats – Earnings (estimates and surprises).",
      "3. **Analyst view:** `ANR` (consensus rating and target) and `EE` (estimate revisions over the last 3 months) for each name.",
      "4. **Latest guidance:** the most recent earnings release or call summary for each name.", ""]
open(f"{A}/shortlist_25.md", "w").write("\n".join(L))
print("written", len(sel), "names")
