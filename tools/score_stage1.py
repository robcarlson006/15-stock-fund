#!/usr/bin/env python3
"""Stage 1 scoring: 75 -> 25. Implements 03_methodology/scoring-framework.md, Stage 1 steps 3-4.

Usage: python3 -I tools/score_stage1.py <metrics.csv> <candidate_pool_75.csv> <out_dir> [--weights Q,V,B,G[,M]]

- Every metric becomes a percentile (0-100) inside the company's own sector, among red-flag survivors.
- Pillar score = mean of that pillar's metric percentiles present; a fully missing pillar = 50 (neutral, flagged).
- Financials use ROE-based quality and P/E, P/B-to-ROE value; REITs value on P/FFO (or EV/EBITDA) vs own history.
- Selection: top 2 per sector, then best remaining scores to 25, capped at 7 AI/data-center names.
"""
import sys
import numpy as np
import pandas as pd

AI_DIRECT = {"AVGO", "SNPS", "TSM", "MSFT", "GOOGL", "META", "VRT", "ETN", "PWR", "CEG", "VST"}
AI_ADJACENT = {"NEE", "CAT", "FCX", "PLD", "EQIX", "TXN"}
OIL = {"XOM", "CVX", "SHEL", "TTE", "COP"}
AI_CAP, OIL_CAP, TARGET = 7, 3, 25

# (column, higher_is_better)
STANDARD = {
    "Quality": [("roic_latest", True), ("roic_5y_avg", True), ("gross_profit_to_assets", True),
                ("op_margin_5y_slope", True), ("fcf_conversion_5y", True)],
    "Value": [("ev_ebitda_vs_hist", False), ("pe_vs_hist", False), ("fcf_yield", True), ("shareholder_yield", True)],
    "Balance sheet": [("net_debt_ebitda", False), ("interest_coverage", True)],
    "Growth": [("rev_cagr_3y", True), ("eps_cagr_3y", True)],
}
FINANCIALS = {
    "Quality": [("roe_latest", True), ("roe_5y_avg", True), ("roe_stability", True)],
    "Value": [("pe_vs_hist", False), ("pb_to_roe", False), ("shareholder_yield", True)],
    "Balance sheet": [("capital_strength", True)],
    "Growth": [("rev_cagr_3y", True), ("eps_cagr_3y", True)],
}
REAL_ESTATE = {
    "Quality": [("roic_latest", True), ("roic_5y_avg", True), ("op_margin_5y_slope", True)],
    "Value": [("value_vs_hist", False), ("shareholder_yield", True)],
    "Balance sheet": [("net_debt_ebitda", False), ("interest_coverage", True)],
    "Growth": [("rev_cagr_3y", True), ("eps_cagr_3y", True)],
}
DEFAULT_W = {"Quality": 30, "Value": 20, "Balance sheet": 15, "Growth": 15}  # momentum 20 dropped, rescaled


def theme(t):
    return "AI direct" if t in AI_DIRECT else "AI adjacent" if t in AI_ADJACENT else "Oil" if t in OIL else ""


def prep(m):
    m = m.copy()
    m["roe_stability"] = -m["roe_5y_std"]
    m["pb_to_roe"] = np.where(m.roe_latest > 0, m.pb_now / m.roe_latest, np.nan)
    m["value_vs_hist"] = m.p_ffo_vs_hist.fillna(m.ev_ebitda_vs_hist).fillna(m.pe_vs_hist)
    # capital strength: banks on Tier 1 common, others on (inverse) debt/equity; each ranked in its own group
    cs = pd.Series(np.nan, index=m.index)
    fin = m.sector == "Financials"
    banks = fin & (m.kind == "bank")
    other = fin & ~banks
    cs[banks] = m.loc[banks, "tier1_common_pct"].rank(pct=True)
    cs[other] = (-m.loc[other, "debt_to_equity"]).rank(pct=True)
    m["capital_strength"] = cs
    return m


def score(m, weights):
    m = prep(m)
    live = m[m.red_flags.isna()].copy()
    rows = []
    for sector, g in live.groupby("sector"):
        spec = FINANCIALS if sector == "Financials" else REAL_ESTATE if sector == "Real Estate" else STANDARD
        g = g.copy()
        for pillar, mets in spec.items():
            pct = []
            for col, hib in mets:
                s = g[col] if hib else -g[col]
                pct.append(s.rank(pct=True) * 100 if s.notna().sum() >= 2 else pd.Series(np.nan, index=g.index))
            pdf = pd.concat(pct, axis=1)
            g[pillar] = pdf.mean(axis=1)
            g[pillar + "_n"] = pdf.notna().sum(axis=1)
            g[pillar] = g[pillar].fillna(50)
        rows.append(g)
    s = pd.concat(rows)
    tot = sum(weights.values())
    s["score"] = sum(s[p] * w for p, w in weights.items()) / tot
    s["sector_rank"] = s.groupby("sector").score.rank(ascending=False, method="first").astype(int)
    s["theme"] = s.ticker.map(theme)
    s["neutral_pillars"] = s.apply(lambda r: ", ".join(p for p in weights if r[p + "_n"] == 0), axis=1)
    return s.sort_values("score", ascending=False)


def select(s):
    picked, why = [], {}
    ai = lambda: sum(1 for t in picked if theme(t).startswith("AI"))
    oil = lambda: sum(1 for t in picked if theme(t) == "Oil")

    def can(t):
        th = theme(t)
        return not ((th.startswith("AI") and ai() >= AI_CAP) or (th == "Oil" and oil() >= OIL_CAP))

    for sector, g in s.groupby("sector"):
        n = 0
        for t in g.sort_values("score", ascending=False).ticker:
            if n == 2: break
            if can(t):
                picked.append(t); why[t] = f"Top 2 in {sector}"; n += 1
    # Fill: best remaining scores, but only from the top half of their own sector. Percentiles in a
    # 3-company sector run 33/67/100, so a weak firm in a tiny sector can outscore a strong one in a big sector.
    size = s.groupby("sector").ticker.transform("count")
    top_half = set(s.loc[s.sector_rank <= np.ceil(size / 2), "ticker"])
    for t in s.ticker:
        if len(picked) >= TARGET: break
        if t not in picked and t in top_half and can(t):
            picked.append(t); why[t] = "Best remaining score (top half of sector)"
    return picked, why


def main(metrics, pool, out_dir, weights=None):
    w = weights or DEFAULT_W
    m = pd.read_csv(metrics)
    s = score(m, w)
    picked, why = select(s)
    s["selected"] = s.ticker.isin(picked)
    s["selection_reason"] = s.ticker.map(why).fillna("")
    s.to_csv(f"{out_dir}/scores.csv", index=False)
    return s, picked


if __name__ == "__main__":
    w = None
    if "--weights" in sys.argv:
        vals = [float(x) for x in sys.argv[sys.argv.index("--weights") + 1].split(",")]
        w = dict(zip(["Quality", "Value", "Balance sheet", "Growth"], vals))
    s, p = main(sys.argv[1], sys.argv[2], sys.argv[3], w)
    print(len(p), "selected")
