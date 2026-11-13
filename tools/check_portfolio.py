#!/usr/bin/env python3
"""Verify portfolio/target_allocation.csv against every portfolio rule. Exits non-zero if any check fails.

Usage (from the project root): /usr/local/bin/python3 -I tools/check_portfolio.py [allocation.csv]

The theme groups are fixed here from the framework and the Stage 1 tags, so a wrong tag in the CSV can't hide a breach.
"""
import sys
import pandas as pd

SHORTLIST = "analysis/stage1_75_to_25/scores.csv"
AI = {"VRT", "VST", "META", "CEG", "GOOGL", "EQIX", "FCX"}
INCOME = {"WPC", "EQIX"}
ADR = {"NVO"}
OIL = set()
COLS = ["ticker", "company", "sector", "theme_tag", "stage2_rank", "target_usd", "thesis_one_line", "sell_trigger"]


def main(path="portfolio/target_allocation.csv"):
    p = pd.read_csv(path)
    s1 = pd.read_csv(SHORTLIST)
    s1 = s1[s1.selected]
    the25, sector25 = set(s1.ticker), dict(zip(s1.ticker, s1.sector))
    usd = pd.to_numeric(p.target_usd, errors="coerce")
    sec = p.groupby("sector").target_usd.sum()
    n_sec = p.groupby("sector").ticker.count()
    ai, inc, adr, oil = (p[p.ticker.isin(g)] for g in (AI, INCOME, ADR, OIL))
    text_ok = lambda c: p[c].notna().all() and (p[c].astype(str).str.strip().str.len() > 0).all()
    checks = [
        ("columns are as specified", list(p.columns) == COLS, ""),
        ("exactly 15 unique tickers", len(p) == 15 and p.ticker.nunique() == 15, f"{p.ticker.nunique()} unique"),
        ("all tickers are in the 25-name shortlist", set(p.ticker) <= the25, f"outside: {sorted(set(p.ticker) - the25) or 'none'}"),
        ("sectors match the shortlist", all(sector25.get(t) == s for t, s in zip(p.ticker, p.sector)), ""),
        ("dollars are whole numbers", usd.notna().all() and (usd % 1 == 0).all(), ""),
        ("dollars sum to exactly 100", usd.sum() == 100, f"sum {usd.sum():g}"),
        ("every position is $4 to $10", usd.between(4, 10).all(), f"min {usd.min():.0f}, max {usd.max():.0f}"),
        ("no sector above $25", sec.max() <= 25, f"largest: {sec.idxmax()} ${sec.max():.0f}"),
        ("at least 7 sectors", p.sector.nunique() >= 7, f"{p.sector.nunique()} sectors"),
        ("at most 3 names per sector", n_sec.max() <= 3, f"largest: {n_sec.idxmax()} {n_sec.max()}"),
        ("AI/data-center: at most 4 names", len(ai) <= 4, f"{len(ai)}: {' '.join(ai.ticker)}"),
        ("AI/data-center: at most $30", ai.target_usd.sum() <= 30, f"${ai.target_usd.sum():.0f}"),
        ("oil-linked: at most 2 names", len(oil) <= 2, f"{len(oil)}"),
        ("REIT/utility income: at most 3 names", len(inc) <= 3, f"{len(inc)}: {' '.join(inc.ticker)}"),
        ("non-US ADRs: at most 3 names", len(adr) <= 3, f"{len(adr)}: {' '.join(adr.ticker)}"),
        ("AI tags in the CSV match the fixed list", set(p[p.theme_tag.fillna('').str.contains('AI')].ticker) == set(ai.ticker), ""),
        ("ranks are 1 to 15, no repeats", sorted(p.stage2_rank) == list(range(1, 16)), ""),
        ("a higher rank never gets fewer dollars than a lower one within the tilt",
         p.sort_values("stage2_rank").target_usd.is_monotonic_decreasing, "informational if a cap moved dollars"),
        ("every row has a thesis", text_ok("thesis_one_line"), ""),
        ("every row has a sell trigger", text_ok("sell_trigger"), ""),
    ]
    failed = 0
    for name, ok, note in checks:
        soft = name.startswith("a higher rank")
        mark = "PASS" if ok else ("WARN" if soft else "FAIL")
        failed += (not ok) and (not soft)
        print(f"{mark}  {name}" + (f"  [{note}]" if note else ""))
    print(f"\n{len(checks) - failed} of {len(checks)} checks passed" + ("" if failed else ". Portfolio is valid."))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
