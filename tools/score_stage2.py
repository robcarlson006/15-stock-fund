#!/usr/bin/env python3
"""Stage 2 scoring: 25 -> 15. Implements the pre-committed spec in 03_methodology/scoring-framework.md
("Stage 2 scoring spec", 13 Nov 2026).

Usage (from the project root):
    /usr/local/bin/python3 -I tools/score_stage2.py [--score-fcf-all]

Inputs  analysis/stage1_75_to_25/scores.csv        Stage 1 score, sector, theme, FCF yield
        analysis/stage1_75_to_25/raw_long.csv       Stage 1 cash flow and market cap
        analysis/stage2_25_to_15/raw_long_stage2.csv Stage 2 Bloomberg FA numbers
        analysis/stage2_25_to_15/overrides.csv      optional: ticker,reason (qualitative exclusions)
Output  analysis/stage2_25_to_15/scores_stage2.csv  every metric, check score, final score, rank, status
        analysis/stage2_25_to_15/robustness_stage2.csv

Stage 2 score = 60% Stage 1 score + 40% average of six checks (percentiles across the 25).
--score-fcf-all is a what-if only: it scores check 3 for PGR, WPC and EQIX too (the spec skips them).
"""
import os
import re
import sys
import numpy as np
import pandas as pd

S1 = "analysis/stage1_75_to_25"
S2 = "analysis/stage2_25_to_15"
AI = {"VRT", "VST", "META", "CEG", "GOOGL", "EQIX", "FCX"}   # direct + adjacent, as tagged at Stage 1
INCOME = {"WPC", "EQIX"}                                      # REITs and regulated utilities
ADR = {"NVO"}
OIL = set()
LIMITS = {"per_sector": 3, "ai": 4, "oil": 2, "income": 3, "adr": 3, "min_sectors": 7, "n": 15}
NO_FCF_SECTORS = {"Financials", "Real Estate"}
CHECKS = ["chk_fscore", "chk_earnings_quality", "chk_sbc_fcf_yield", "chk_strength", "chk_delivery", "chk_fwd_growth"]
YEAR = re.compile(r"^(\d{4}) A$")


class Co:
    """One company's numbers from a long-format file."""

    def __init__(self, df):
        self.df = df

    def row(self, section, label, sub=None):
        x = self.df[(self.df.section == section) & (self.df.label.str.lower() == label.lower())]
        if sub:
            x = x[x["sub"] == sub]
        if x.empty:
            return pd.Series(dtype=float)
        x = x[x.occurrence == x.occurrence.min()]
        return x.drop_duplicates("col").set_index("col").value

    def annual(self, section, label, sub=None):
        s = self.row(section, label, sub)
        s = s[[c for c in s.index if YEAR.match(c)]].dropna()
        s.index = [int(YEAR.match(c).group(1)) for c in s.index]
        return s.sort_index()

    def first_annual(self, *options):
        for o in options:
            s = self.annual(*o)
            if len(s):
                return s
        return pd.Series(dtype=float)

    def point(self, section, label, cols, sub=None):
        s = self.row(section, label, sub)
        for c in cols:
            if c in s.index and pd.notna(s[c]):
                return s[c]
        return np.nan


def at(s, y):
    return s.get(y, np.nan) if len(s) else np.nan


def company_metrics(t, sector, kind, c2, c1, fcf_yield):
    m = {"ticker": t}
    ta = c2.annual("Standardized", "Total Assets")
    ni = c2.annual("GAAP", "Net Income, GAAP")
    ni_gaap = c2.annual("GAAP", "Net Income Avail to Common, GAAP")
    ni_adj = c2.annual("GAAP", "Net Income Avail to Common, Adj")
    rev = c2.first_annual(("GAAP", "Revenue"), ("GAAP", "Net Revenue"))
    gp = c2.first_annual(("GAAP", "Gross Profit"), ("GAAP", "Gross Profit + Other Operating"))
    sh = c2.annual("GAAP", "Diluted Weighted Avg Shares")
    ltd = c2.annual("Liquidity", "Long-Term Debt/Total Assets")
    cr = c2.annual("Liquidity", "Current Ratio")
    at_ = c2.annual("DuPont Analysis", "Revenue/Avg Assets", "Asset Turnover")
    cfo = c1.annual("Standardized", "Cash from Operating Activities")
    y = int(ta.index.max())
    m["fiscal_year"] = y

    # ---- 1. Piotroski F-score
    roa = lambda yy: at(ni, yy) / at(ta, yy - 1)
    gm = lambda yy: at(gp, yy) / at(rev, yy)
    sig = {
        "roa_pos": (roa(y), lambda v: v > 0),
        "cfo_pos": (at(cfo, y), lambda v: v > 0),
        "roa_up": (roa(y) - roa(y - 1), lambda v: v > 0),
        "cfo_gt_ni": (at(cfo, y) - at(ni, y), lambda v: v > 0),
        "ltd_down": (at(ltd, y) - at(ltd, y - 1), lambda v: v < 0),
        "cr_up": (at(cr, y) - at(cr, y - 1), lambda v: v > 0),
        "shares_not_up": (at(sh, y) - at(sh, y - 1), lambda v: v <= 0),
        "gm_up": (gm(y) - gm(y - 1), lambda v: v > 0),
        "turnover_up": (at(at_, y) - at(at_, y - 1), lambda v: v > 0),
    }
    if kind == "bank":
        sig["cfo_pos"] = sig["cfo_gt_ni"] = (np.nan, None)
    used = [k for k, (v, _) in sig.items() if pd.notna(v)]
    pts = [k for k in used if sig[k][1](sig[k][0])]
    m["f_points"], m["f_signals_used"] = len(pts), len(used)
    m["f_score_0_9"] = round(len(pts) / len(used) * 9, 2) if used else np.nan
    m["f_signals_passed"] = " ".join(pts)
    m["f_signals_failed"] = " ".join(k for k in used if k not in pts)
    m["f_signals_skipped"] = " ".join(k for k in sig if k not in used)
    m["roa_pct"] = round(roa(y) * 100, 2)
    m["cfo"], m["net_income_gaap"] = at(cfo, y), at(ni, y)

    # ---- 2. Earnings quality
    both = pd.concat([ni_adj, ni_gaap], axis=1, keys=["a", "g"]).dropna().iloc[-5:]
    gap = np.where(both.g > 0, np.minimum((both.a / both.g - 1).abs(), 1.0), 1.0)
    m["adj_gaap_gap_5y_pct"] = round(float(gap.mean()) * 100, 2) if len(gap) else np.nan
    m["adj_gaap_years"] = len(gap)
    sbc_pre = c2.annual("SBC & Amort", "Pre-Tax", "Stock Based Compensation")
    m["sbc_pct_revenue"] = round(at(sbc_pre, y) / at(rev, y) * 100, 2) if len(sbc_pre) else np.nan

    # ---- 3. SBC-adjusted FCF yield
    sbc_at = c2.point("SBC & Amort", "After-Tax", ["Current/LTM", f"{y} A"], "Stock Based Compensation")
    mcap = c1.point("Yield Analysis", "Market Capitalization", ["Current"])
    m["fcf_yield_s1"] = fcf_yield
    m["sbc_after_tax_ltm"], m["market_cap"] = sbc_at, mcap
    m["sbc_yield_pct"] = round(sbc_at / mcap * 100, 2) if pd.notna(sbc_at) else np.nan
    if sector in NO_FCF_SECTORS:
        m["sbc_adj_fcf_yield"] = np.nan
        m["whatif_sbc_adj_fcf_yield"] = round(fcf_yield - m["sbc_yield_pct"], 2) if pd.notna(fcf_yield) else np.nan
    else:
        m["sbc_adj_fcf_yield"] = round(fcf_yield - (m["sbc_yield_pct"] if pd.notna(sbc_at) else 0), 2)
        m["whatif_sbc_adj_fcf_yield"] = m["sbc_adj_fcf_yield"]

    # ---- 4. Financial strength
    m["altman_z"] = c2.point("Liquidity", "Altman's Z-Score", ["Current", f"{y} A"])
    m["current_ratio"] = c2.point("Liquidity", "Current Ratio", ["Current", f"{y} A"])

    # ---- 5 & 6. Earnings delivery and forward growth
    block = "FFO Per Share" if t == "WPC" else "Earnings Per Share"
    slabel = "FFO Per Share Surprise %" if t == "WPC" else "EPS Surprise %"
    sur = c2.annual("Earnings", slabel, block).iloc[-4:]
    m["eps_block"] = block
    m["surprise_avg_4y_pct"] = round(sur.mean(), 2) if len(sur) else np.nan
    m["beats_of_4"] = int((sur > 0).sum()) if len(sur) else np.nan
    m["surprise_years"] = " ".join(f"{k}:{v:+.1f}" for k, v in sur.items())
    act = c2.annual("Earnings", "Comparable Actual", block)
    ly = int(act.index.max())
    est = c2.point("Earnings", "Consensus Estimate", [f"Estimate:{ly + 1} A"], block)
    m["eps_last_fy"], m["eps_last_fy_year"], m["eps_next_fy_consensus"] = act[ly], ly, est
    m["fwd_eps_growth_pct"] = round((est / act[ly] - 1) * 100, 2) if act[ly] > 0 and pd.notna(est) else np.nan
    return m


def pct(s, higher_is_better=True):
    return (s if higher_is_better else -s).rank(pct=True) * 100


def add_checks(m):
    m = m.copy()
    m["chk_fscore"] = pct(m.f_score_0_9)
    m["chk_earnings_quality"] = pd.concat([pct(m.adj_gaap_gap_5y_pct, False), pct(m.sbc_pct_revenue, False)], axis=1).mean(axis=1)
    m["chk_sbc_fcf_yield"] = pct(m.sbc_adj_fcf_yield)
    m["chk_strength"] = pd.concat([pct(m.altman_z), pct(m.current_ratio)], axis=1).mean(axis=1)
    m["chk_delivery"] = pd.concat([pct(m.surprise_avg_4y_pct), pct(m.beats_of_4)], axis=1).mean(axis=1)
    m["chk_fwd_growth"] = pct(m.fwd_eps_growth_pct)
    m["checks_used"] = m[CHECKS].notna().sum(axis=1)
    m["checks_skipped"] = m[CHECKS].apply(lambda r: " ".join(c[4:] for c in CHECKS if pd.isna(r[c])), axis=1)
    m["stage2_checks"] = m[CHECKS].mean(axis=1)
    return m


def select(m, w1, excluded=()):
    """Walk down the ranking. Returns (ranked frame with score/rank, {ticker: status})."""
    m = m.copy()
    m["stage2_score"] = w1 * m.stage1_score + (1 - w1) * m.stage2_checks
    m = m.sort_values(["stage2_score", "stage1_score"], ascending=False).reset_index(drop=True)
    m["stage2_rank"] = m.index + 1
    picked, status = [], {}
    L = LIMITS
    for _, r in m.iterrows():
        t = r.ticker
        if t in excluded:
            status[t] = "override: excluded"
            continue
        if len(picked) >= L["n"]:
            status[t] = "bench"
            continue
        sectors = [m.loc[m.ticker == p, "sector"].iloc[0] for p in picked]
        why = None
        if sectors.count(r.sector) >= L["per_sector"]:
            why = f"sector limit (3 in {r.sector})"
        elif t in AI and sum(p in AI for p in picked) >= L["ai"]:
            why = "AI/data-center limit (4)"
        elif t in OIL and sum(p in OIL for p in picked) >= L["oil"]:
            why = "oil limit (2)"
        elif t in INCOME and sum(p in INCOME for p in picked) >= L["income"]:
            why = "rate-sensitive income limit (3)"
        elif t in ADR and sum(p in ADR for p in picked) >= L["adr"]:
            why = "ADR limit (3)"
        else:
            n_sec = len(set(sectors) | {r.sector})
            if L["n"] - len(picked) - 1 < L["min_sectors"] - n_sec:
                why = "7-sector minimum"
        if why:
            status[t] = f"bench: blocked by {why}"
        else:
            picked.append(t)
            status[t] = "selected"
    m["status"] = m.ticker.map(status)
    return m, picked


def build(score_fcf_all=False):
    s1 = pd.read_csv(f"{S1}/scores.csv")
    s1 = s1[s1.selected].copy()
    r1 = pd.read_csv(f"{S1}/raw_long.csv")
    r1["t"] = r1.file.str.replace(".pdf", "", regex=False)
    r2 = pd.read_csv(f"{S2}/raw_long_stage2.csv")
    r2["t"] = r2.file.str.replace("_FA.pdf", "", regex=False)
    rows = []
    for _, r in s1.iterrows():
        rows.append(company_metrics(r.ticker, r.sector, r.kind, Co(r2[r2.t == r.ticker]), Co(r1[r1.t == r.ticker]), r.fcf_yield))
    m = pd.DataFrame(rows)
    base = s1[["ticker", "sector", "kind", "theme", "score", "sector_rank"]].rename(
        columns={"score": "stage1_score", "sector_rank": "stage1_sector_rank"})
    m = base.merge(m, on="ticker")
    if score_fcf_all:
        m["sbc_adj_fcf_yield"] = m.whatif_sbc_adj_fcf_yield
    return add_checks(m)


def main():
    what_if = "--score-fcf-all" in sys.argv
    m = build(what_if)
    excluded = {}
    if os.path.exists(f"{S2}/overrides.csv"):
        o = pd.read_csv(f"{S2}/overrides.csv")
        excluded = dict(zip(o.ticker, o.reason))
    out, picked = select(m, 0.6, excluded)
    out["override_reason"] = out.ticker.map(excluded).fillna("")
    rob = {"60/40 (base)": picked}
    for w in (0.8, 0.4):
        rob[f"{int(w * 100)}/{int(round((1 - w) * 100))}"] = select(m, w, excluded)[1]
    alt = [k for k in rob if k != "60/40 (base)"]
    out["picked_80_20"] = out.ticker.isin(rob[alt[0]])
    out["picked_40_60"] = out.ticker.isin(rob[alt[1]])
    out["borderline"] = (out.status == "selected") & ~(out.picked_80_20 & out.picked_40_60)
    num = out.select_dtypes("number").columns
    out[num] = out[num].round(2)
    if what_if:
        print("WHAT-IF (check 3 scored for PGR, WPC, EQIX): nothing written")
    else:
        out.to_csv(f"{S2}/scores_stage2.csv", index=False)
        pd.DataFrame([{"split": k, "picked": " ".join(v), "kept_from_base": len(set(v) & set(picked)),
                       "added": " ".join(sorted(set(v) - set(picked))), "dropped": " ".join(sorted(set(picked) - set(v)))}
                      for k, v in rob.items()]).to_csv(f"{S2}/robustness_stage2.csv", index=False)
    show = out[["stage2_rank", "ticker", "sector", "stage1_score", "stage2_checks", "checks_used", "stage2_score", "status", "borderline"]]
    print(show.to_string(index=False))
    for k, v in rob.items():
        print(f"{k:14} kept {len(set(v) & set(picked))}/15  +{sorted(set(v) - set(picked))} -{sorted(set(picked) - set(v))}")
    return out


if __name__ == "__main__":
    main()
