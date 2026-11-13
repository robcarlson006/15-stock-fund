"""Render the README charts, each in a light and a dark version.

GitHub picks the right one with <picture> + prefers-color-scheme, so every
chart sits on the exact GitHub page background in either theme.
"""
import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mtick  # noqa: E402
import pandas as pd  # noqa: E402

from common import CHARTS, CONFIG, HOLDINGS, NAV, SUMMARY  # noqa: E402

THEMES = {
    "light": dict(bg="#ffffff", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e8e7e1", axis="#c3c2b7", fund="#2a78d6", bench="#898781",
                  pos="#2a78d6", neg="#e34948", target="#0b0b0b",
                  ramp=["#86b6ef", "#3987e5", "#1c5cab"]),
    "dark": dict(bg="#0d1117", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#21262d", axis="#383835", fund="#3987e5", bench="#898781",
                 pos="#3987e5", neg="#e66767", target="#f0efec",
                 ramp=["#184f95", "#2a78d6", "#6da7ec"]),
}
FONT = ["Inter", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
W = 12  # inches; README renders at ~880px so text sizes are chosen for that


def style(th):
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": FONT,
        "figure.facecolor": th["bg"], "axes.facecolor": th["bg"],
        "savefig.facecolor": th["bg"], "text.color": th["ink"],
        "axes.edgecolor": th["axis"], "axes.labelcolor": th["ink2"],
        "xtick.color": th["muted"], "ytick.color": th["muted"],
        "xtick.labelsize": 11, "ytick.labelsize": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.spines.left": False, "axes.grid": True, "axes.axisbelow": True,
        "grid.color": th["grid"], "grid.linewidth": 0.8,
        "xtick.major.size": 0, "ytick.major.size": 0,
    })


def header(fig, th, title, sub):
    fig.text(0.012, 0.965, title, fontsize=17, fontweight="bold", color=th["ink"], va="top")
    fig.text(0.012, 0.885, sub, fontsize=12, color=th["ink2"], va="top")


def save(fig, name, theme):
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{name}-{theme}.png", dpi=170)
    plt.close(fig)


def pct(v, signed=True):
    return (f"{v:+.1%}" if signed else f"{v:.1%}").replace("-", "\u2212")


def nice_y(ax, decimals):
    ax.yaxis.set_major_locator(mtick.MaxNLocator(6, steps=[1, 2, 2.5, 5, 10]))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=decimals))


# ---------------------------------------------------------------- charts ----
def performance(nav, s, th, theme):
    fig, ax = plt.subplots(figsize=(W, 5.2))
    fig.subplots_adjust(left=0.07, right=0.86, top=0.8, bottom=0.1)
    d = pd.to_datetime(nav["date"])
    f = nav["fund_index"] / 100 - 1
    b = nav["benchmark_index"] / 100 - 1
    one = len(nav) == 1
    ax.plot(d, b, color=th["bench"], lw=2, marker="o" if one else None, ms=8, label=s["bench_name"])
    ax.plot(d, f, color=th["fund"], lw=2.4, marker="o" if one else None, ms=8, label="Fund")
    if not one:
        ax.fill_between(d, f, b, where=f >= b, color=th["pos"], alpha=0.10, lw=0, interpolate=True)
        ax.fill_between(d, f, b, where=f < b, color=th["neg"], alpha=0.10, lw=0, interpolate=True)
    ax.axhline(0, color=th["axis"], lw=1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0 if max(abs(f).max(), abs(b).max()) > 0.05 else 1))
    ax.grid(axis="x", visible=False)
    span = max(abs(f).max(), abs(b).max(), 0.02)
    ax.set_ylim(min(f.min(), b.min(), 0) - span * 0.15, max(f.max(), b.max(), 0) + span * 0.15)
    # direct end labels, nudged apart if they would collide
    yf, yb = f.iloc[-1], b.iloc[-1]
    gap = span * 0.09
    if abs(yf - yb) < gap:
        mid = (yf + yb) / 2
        yf, yb = (mid + gap / 2, mid - gap / 2) if f.iloc[-1] >= b.iloc[-1] else (mid - gap / 2, mid + gap / 2)
    for y, txt, c in [(yf, f"Fund  {pct(f.iloc[-1])}", th["fund"]),
                      (yb, f"S&P 500 TR  {pct(b.iloc[-1])}", th["bench"])]:
        ax.annotate(txt, xy=(1.005, y), xycoords=("axes fraction", "data"), fontsize=12,
                    fontweight="bold", color=th["ink"], va="center",
                    bbox=dict(boxstyle="round,pad=0.25", fc=th["bg"], ec=c, lw=1.5))
    if one:
        ax.set_xticks([d.iloc[0]])
        ax.set_xticklabels([d.iloc[0].strftime("%d %b %Y")])
        ax.text(0.5, 0.18, f"Tracking started {d.iloc[0]:%d %b %Y}. A new point is added after every US market close.",
                transform=ax.transAxes, ha="center", fontsize=11, color=th["muted"])
    else:
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d %b\n%Y" if len(nav) < 70 else "%b %Y"))
        ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(maxticks=8))
    exc = s["excess_return"]
    sub = (f"Fund vs {s['bench_name']} · inception day, {s['inception_label']}" if one else
           f"Fund vs {s['bench_name']} · {s['inception_label']} to {s['asof_label']} · "
           f"{'ahead' if exc >= 0 else 'behind'} by {abs(exc) * 100:.2f} pts")
    header(fig, th, "Cumulative return since inception", sub)
    save(fig, "performance", theme)


def holdings_return(h, th, theme):
    h = h[h["shares"] > 0].sort_values("return_pct")
    fig, ax = plt.subplots(figsize=(W, 6.4))
    fig.subplots_adjust(left=0.16, right=0.86, top=0.85, bottom=0.05)
    y = range(len(h))
    vals = h["return_pct"]
    colors = [th["pos"] if v >= 0 else th["neg"] for v in vals]
    ax.barh(y, vals, color=colors, height=0.62)
    ax.axvline(0, color=th["axis"], lw=1)
    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{t}  " for t in h["ticker"]], fontsize=11.5, fontweight="bold", color=th["ink"])
    ax.grid(axis="y", visible=False)
    span = max(vals.abs().max(), 0.01)
    ax.set_xlim(min(vals.min(), 0) - span * 0.35, max(vals.max(), 0) + span * 0.35)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0 if span > 0.05 else 1))
    for i, (v, pl) in enumerate(zip(vals, h["total_pl"])):
        ax.text(v + (span * 0.03 if v >= 0 else -span * 0.03), i, pct(v), va="center",
                ha="left" if v >= 0 else "right", fontsize=10.5, color=th["ink2"])
        ax.annotate(f"{'+' if pl >= 0 else '−'}${abs(pl):.2f}", xy=(1.01, i),
                    xycoords=("axes fraction", "data"), va="center", fontsize=10.5, color=th["ink2"])
    ax.annotate("P&L", xy=(1.01, len(h) - 0.2), xycoords=("axes fraction", "data"),
                fontsize=10.5, color=th["muted"], fontweight="bold")
    header(fig, th, "Return by holding", "Since purchase, including dividends · sorted best to worst")
    save(fig, "holdings", theme)


def allocation(h, th, theme):
    h = h[(h["shares"] > 0) | (h["target_weight"] > 0)].sort_values(["target_weight", "weight"])
    sec = h.groupby("sector")["weight"].sum().sort_values()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(W, 6.4), gridspec_kw=dict(width_ratios=[1.15, 1]))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.76, bottom=0.07, wspace=0.55)
    y = range(len(h))
    a1.barh(y, h["weight"], color=th["fund"], height=0.62, label="Current weight")
    a1.scatter(h["target_weight"], list(y), marker="|", s=260, lw=2.2, color=th["target"],
               zorder=3, label="Target")
    a1.set_yticks(list(y))
    a1.set_yticklabels(h["ticker"], fontsize=11, fontweight="bold", color=th["ink"])
    a1.xaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    a1.grid(axis="y", visible=False)
    a1.set_title("By holding", loc="left", fontsize=12.5, color=th["ink2"], pad=10)
    a1.legend(loc="lower right", frameon=False, fontsize=10, labelcolor=th["ink2"])
    y2 = range(len(sec))
    a2.barh(y2, sec.values, color=th["ramp"][1], height=0.62)
    a2.set_yticks(list(y2))
    a2.set_yticklabels(sec.index, fontsize=11, color=th["ink"])
    a2.xaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    a2.set_xlim(0, sec.max() * 1.3)
    a2.grid(axis="y", visible=False)
    for i, v in enumerate(sec.values):
        a2.text(v + sec.max() * 0.02, i, f"{v:.1%}", va="center", fontsize=10.5, color=th["ink2"])
    a2.set_title("By sector", loc="left", fontsize=12.5, color=th["ink2"], pad=10)
    header(fig, th, "Allocation", f"{int((h['shares'] > 0).sum())} holdings across {len(sec)} sectors · "
           "bars = today's weight, tick = target weight")
    save(fig, "allocation", theme)


def drawdown(nav, s, th, theme):
    fig, ax = plt.subplots(figsize=(W, 3.8))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.7, bottom=0.14)
    d = pd.to_datetime(nav["date"])
    ax.fill_between(d, nav["drawdown"], 0, color=th["neg"], alpha=0.18, lw=0)
    ax.plot(d, nav["drawdown"], color=th["neg"], lw=2, label="Fund")
    ax.plot(d, nav["benchmark_drawdown"], color=th["bench"], lw=1.6, ls="--", label=s["bench_name"])
    ax.axhline(0, color=th["axis"], lw=1)
    lo = min(nav["drawdown"].min(), nav["benchmark_drawdown"].min(), -0.02)
    ax.set_ylim(lo * 1.15, abs(lo) * 0.08)
    nice_y(ax, 0 if lo < -0.05 else 1)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="lower left", frameon=False, fontsize=10.5, labelcolor=th["ink2"], ncol=2)
    if len(nav) > 1:
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d %b\n%Y" if len(nav) < 70 else "%b %Y"))
        ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(maxticks=8))
    else:
        ax.set_xticks([d.iloc[0]])
        ax.set_xticklabels([d.iloc[0].strftime("%d %b %Y")])
    header(fig, th, "Drawdown", f"Distance below the fund's previous high · worst so far "
           f"{s['max_drawdown'] * 100:.1f}% (S&P 500 TR {s['benchmark_max_drawdown'] * 100:.1f}%)")
    save(fig, "drawdown", theme)


def funnel(th, theme):
    stages = [(75, "Candidate pool", "11 sectors, US-listed large caps and ADRs"),
              (25, "Shortlist", "Bloomberg screen: red flags, then score within sector"),
              (15, "Portfolio", "Re-scored on fuller data, capped dollar weights")]
    fig, ax = plt.subplots(figsize=(W, 3.6))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.72, bottom=0.04)
    ax.axis("off")
    ax.set_xlim(-80, 80)
    ax.set_ylim(-0.6, len(stages) - 0.4)
    for i, (n, name, note) in enumerate(stages):
        y = len(stages) - 1 - i
        ax.barh(y, n, left=-n / 2 - 40, height=0.72, color=th["ramp"][i])
        ax.text(-40, y, str(n), ha="center", va="center", fontsize=17, fontweight="bold",
                color="#ffffff" if (theme == "light" and i > 0) or theme == "dark" else th["ink"])
        ax.text(2, y + 0.12, name, va="center", fontsize=13, fontweight="bold", color=th["ink"])
        ax.text(2, y - 0.2, note, va="center", fontsize=11, color=th["ink2"])
    header(fig, th, "Selection funnel", "Every cut made by rules written before the data was seen")
    save(fig, "funnel", theme)


def main() -> int:
    nav = pd.read_csv(NAV)
    h = pd.read_csv(HOLDINGS)
    s = json.loads(SUMMARY.read_text())
    s["bench_name"] = CONFIG["benchmark"]["name"]
    s["inception_label"] = pd.Timestamp(s["inception"]).strftime("%d %b %Y")
    s["asof_label"] = pd.Timestamp(s["as_of"]).strftime("%d %b %Y")
    for theme, th in THEMES.items():
        style(th)
        performance(nav, s, th, theme)
        holdings_return(h, th, theme)
        allocation(h, th, theme)
        drawdown(nav, s, th, theme)
        funnel(th, theme)
    print(f"charts: written to {CHARTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
