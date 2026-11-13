#!/usr/bin/env python3
"""Stage 3 sizing: dollar weights for the 15. Implements 03_methodology/scoring-framework.md, Stage 3.

Usage (from the project root): /usr/local/bin/python3 -I tools/size_stage3.py
Reads  analysis/stage2_25_to_15/scores_stage2.csv, tools/stage2_notes.py
Writes portfolio/target_allocation.csv

Top 5 by Stage 2 score $8, middle 5 $7, bottom 5 $5. If a cap binds, $1 at a time moves from the lowest-ranked
name in the breaching group to the highest-ranked name outside it that hasn't yet received a dollar.
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_stage2 import AI, INCOME, ADR
from stage2_notes import COMPANY, HOLD

POS_MIN, POS_MAX, SECTOR_MAX, AI_MAX, TOTAL = 4, 10, 25, 30, 100


def tag(t, theme):
    tags = [theme] if isinstance(theme, str) and theme else []
    if t in INCOME:
        tags.append("REIT income")
    if t in ADR:
        tags.append("ADR")
    return "; ".join(tags)


def breaches(p):
    out = [("sector " + s, set(g.ticker)) for s, g in p.groupby("sector") if g.target_usd.sum() > SECTOR_MAX]
    if p.loc[p.ticker.isin(AI), "target_usd"].sum() > AI_MAX:
        out.append(("AI/data-center", set(p.ticker) & AI))
    return out


def size(p):
    p = p.sort_values("stage2_rank").reset_index(drop=True)
    p["target_usd"] = [8] * 5 + [7] * 5 + [5] * 5
    moves, got = [], set()
    while breaches(p):
        name, group = breaches(p)[0]
        donors = p[p.ticker.isin(group) & (p.target_usd > POS_MIN)].sort_values("stage2_rank", ascending=False)
        takers = p[~p.ticker.isin(group) & ~p.ticker.isin(got) & (p.target_usd < POS_MAX)].sort_values("stage2_rank")
        ok = None
        for _, r in takers.iterrows():
            if donors.empty:
                break
            trial = p.copy()
            trial.loc[trial.ticker == donors.ticker.iloc[0], "target_usd"] -= 1
            trial.loc[trial.ticker == r.ticker, "target_usd"] += 1
            # the taker must not push any other group over its cap
            if {b[0] for b in breaches(trial)} <= {b[0] for b in breaches(p)}:
                ok = (donors.ticker.iloc[0], r.ticker, trial)
                break
        if donors.empty or ok is None:
            raise SystemExit(f"cannot resolve {name} cap")
        moves.append(f"$1 from {ok[0]} to {ok[1]} ({name} cap)")
        got.add(ok[1])
        p = ok[2]
    return p, moves


def main():
    s = pd.read_csv("analysis/stage2_25_to_15/scores_stage2.csv")
    p = s[s.status == "selected"].copy()
    p["stage2_rank"] = p.stage2_score.rank(ascending=False, method="first").astype(int)
    p, moves = size(p)
    assert p.target_usd.sum() == TOTAL
    out = pd.DataFrame({
        "ticker": p.ticker, "company": p.ticker.map(COMPANY), "sector": p.sector,
        "theme_tag": [tag(t, th) for t, th in zip(p.ticker, p.theme)], "stage2_rank": p.stage2_rank,
        "target_usd": p.target_usd, "thesis_one_line": p.ticker.map(lambda t: HOLD[t][0]),
        "sell_trigger": p.ticker.map(lambda t: HOLD[t][3])})
    out.to_csv("portfolio/target_allocation.csv", index=False)
    print(out[["stage2_rank", "ticker", "sector", "theme_tag", "target_usd"]].to_string(index=False))
    print("Moves:", moves or "none (no cap binds)")
    return out, moves


if __name__ == "__main__":
    main()
