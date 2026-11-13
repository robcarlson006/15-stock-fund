#!/usr/bin/env python3
"""Robustness check: re-run Stage 1 selection under six pillar weightings and count how often each name is picked.
Usage: python3 -I tools/sensitivity_stage1.py   (run from the project root)"""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_stage1 as S

A = "analysis/stage1_75_to_25"
m = pd.read_csv(f"{A}/metrics.csv")
P = list(S.DEFAULT_W)
sets = {"Base 30/20/15/15": S.DEFAULT_W,
        "Equal 25 each": dict(zip(P, [25, 25, 25, 25])),
        "Quality-heavy 50/20/15/15": dict(zip(P, [50, 20, 15, 15])),
        "Value-heavy 20/50/15/15": dict(zip(P, [20, 50, 15, 15])),
        "Growth-heavy 25/20/15/40": dict(zip(P, [25, 20, 15, 40])),
        "Original pre-momentum 35/30/20/15": dict(zip(P, [35, 30, 20, 15]))}
res = {k: set(S.select(S.score(m, w))[0]) for k, w in sets.items()}
base = res["Base 30/20/15/15"]
names = sorted(set().union(*res.values()))
out = pd.DataFrame({"ticker": names,
                    "in_base": [t in base for t in names],
                    "times_selected_of_6": [sum(t in v for v in res.values()) for t in names]})
out.sort_values(["times_selected_of_6", "in_base"], ascending=False).to_csv(f"{A}/sensitivity.csv", index=False)
for k, v in res.items():
    print(f"{k:36} +{sorted(v - base)} -{sorted(base - v)}")
