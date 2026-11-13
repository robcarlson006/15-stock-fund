#!/usr/bin/env python3
"""Turn raw_long.csv (from extract_bloomberg.py) into one row of Stage 1 metrics per company.

Usage: python3 -I tools/compute_metrics.py <raw_long.csv> <candidate_pool_75.csv> <file_index.csv> <out_metrics.csv>

Rules follow 03_methodology/scoring-framework.md (Stage 1, steps 1-2).
'LTM' = the report's Current/LTM (or Current) column; 'annual' = reported fiscal years ('2024 A').
"""
import re, sys
import numpy as np
import pandas as pd

BANKS = {"JPM", "WFC", "GS"}
INSURERS = {"PGR", "CB"}
FIN_SERVICES = {"V", "MA", "CME", "SPGI"}
REITS = {"O", "WPC", "PLD", "EQIX"}
BEING_ACQUIRED = {"D": "Being acquired by NextEra (merger-spread trade, not a 1-year holding)"}


def kind(t, sector):
    if t in BANKS: return "bank"
    if t in INSURERS: return "insurer"
    if t in FIN_SERVICES: return "fin_services"
    if t in REITS: return "reit"
    if sector == "Utilities": return "utility"
    return "standard"


class Co:
    def __init__(self, df):
        self.d = df

    def series(self, section, label, sub=None):
        x = self.d[(self.d.section == section) & (self.d.label == label) & (self.d.occurrence == 0)]
        if sub is not None:
            x = x[x["sub"].fillna("") == sub]
        return x

    def ltm(self, section, label, sub=None):
        x = self.series(section, label, sub)
        x = x[x.col.isin(["Current/LTM", "Current"])]
        return float(x.value.iloc[0]) if len(x) else np.nan

    def annual(self, section, label, sub=None, n=None):
        """Reported fiscal years, oldest -> newest, as a pandas Series indexed by year."""
        x = self.series(section, label, sub)
        x = x[x.col.str.match(r"^\d{4} A$", na=False)].copy()
        x["yr"] = x.col.str[:4].astype(int)
        s = x.drop_duplicates("yr").set_index("yr").value.sort_index()
        return s.iloc[-n:] if n else s

    def first(self, *options, how="ltm"):
        for sec, lab in options:
            v = self.ltm(sec, lab) if how == "ltm" else self.annual(sec, lab)
            if (how == "ltm" and not np.isnan(v)) or (how != "ltm" and len(v)):
                return v
        return np.nan if how == "ltm" else pd.Series(dtype=float)


def cagr(s, years=3):
    s = s.dropna()
    if len(s) < years + 1: return np.nan
    a, b = s.iloc[-years - 1], s.iloc[-1]
    if a <= 0 or b <= 0: return np.nan
    return ((b / a) ** (1 / years) - 1) * 100


def slope(s):
    s = s.dropna()
    if len(s) < 3: return np.nan
    return float(np.polyfit(range(len(s)), s.values, 1)[0])


def hist_ratio(c, label, n=5):
    """Current multiple divided by the MEDIAN of its own yearly averages over the last n fiscal years.
    Median, not mean, so one freak year (e.g. BKNG's 2021 EV/EBITDA of 4,811x on COVID-depressed EBITDA)
    can't distort the baseline."""
    now = c.ltm("Multiples", label)
    avg = c.annual("Multiples", f"{label} | Average", n=n)
    avg = avg[avg > 0]
    if np.isnan(now) or now <= 0 or len(avg) < 3: return now, np.nan, np.nan
    base = float(avg.median())
    return now, base, now / base


def metrics(t, sector, c):
    k = kind(t, sector)
    m = {"ticker": t, "sector": sector, "kind": k}
    # --- Quality
    m["roic_latest"] = c.ltm("Profitability", "Return on Invested Capital")
    roic = c.annual("Profitability", "Return on Invested Capital", n=5)
    m["roic_5y_avg"] = roic.mean() if len(roic) >= 3 else np.nan
    m["roe_latest"] = c.ltm("Profitability", "Return on Common Equity")
    roe = c.annual("Profitability", "Return on Common Equity", n=5)
    m["roe_5y_avg"] = roe.mean() if len(roe) >= 3 else np.nan
    m["roe_5y_std"] = roe.std() if len(roe) >= 3 else np.nan
    ni_ltm = c.first(("Standardized", "+ Net Income"), ("Standardized", "Net Income"))
    roa = c.ltm("Profitability", "Return on Assets")
    gp = c.ltm("Adj Highlights", "Gross Profit, Adj")
    # Total assets aren't in the 9 templates: back them out of ROA (preferred) or debt/assets.
    total_assets = np.nan
    td, td_ta = c.ltm("Credit", "Total Debt"), c.ltm("Credit", "Total Debt/Total Assets")
    if roa > 2 and ni_ltm > 0:
        total_assets = ni_ltm / (roa / 100)
    elif td > 0 and 5 <= td_ta <= 100:
        total_assets = td / (td_ta / 100)
    m["total_assets_est"] = total_assets
    m["gross_profit_to_assets"] = gp / total_assets * 100 if gp == gp and total_assets == total_assets else np.nan
    m["op_margin_latest"] = c.ltm("Profitability", "Operating Margin")
    m["op_margin_5y_slope"] = slope(c.annual("Profitability", "Operating Margin", n=5))
    fcf_a = c.first(("Adj Highlights", "Free Cash Flow"), ("Standardized", "Free Cash Flow"), how="annual")
    ni_a = c.first(("Standardized", "+ Net Income"), ("Standardized", "Net Income"), how="annual")
    both = pd.concat([fcf_a, ni_a], axis=1, keys=["f", "n"]).dropna().iloc[-5:]
    m["fcf_conversion_5y"] = both.f.sum() / both.n.sum() if len(both) >= 3 and both.n.sum() > 0 else np.nan
    # --- Value
    m["ev_ebitda_now"], m["ev_ebitda_5y_avg"], m["ev_ebitda_vs_hist"] = hist_ratio(c, "EV/EBITDA")
    m["pe_now"], m["pe_5y_avg"], m["pe_vs_hist"] = hist_ratio(c, "P/E")
    # One-off check: LTM EPS is 'distorted' if >40% away from the median of
    # (last fiscal-year EPS, next two estimates). Then value the P/E on that median.
    m["pe_basis"] = "LTM"
    eps_ltm = c.first(("Adj Highlights", "EPS, Adj"))
    eps_fy = c.first(("Adj Highlights", "EPS, Adj"), how="annual")
    s = c.series("Adj Highlights", "EPS, Adj")
    est = s[s.col.str.startswith("Estimate", na=False)].value.tolist()[:2]
    price = c.ltm("Multiples", "Price/Share")
    if len(eps_fy) and len(est) == 2 and eps_ltm == eps_ltm and price == price:
        norm = float(np.median([eps_fy.iloc[-1]] + est))
        if norm > 0 and abs(eps_ltm / norm - 1) > 0.40:
            m["pe_now"] = price / norm
            m["pe_basis"] = f"normalised EPS {norm:g} (median of FY{eps_fy.index[-1]} + 2 estimates); LTM EPS {eps_ltm:g} looks one-off"
            m["pe_vs_hist"] = m["pe_now"] / m["pe_5y_avg"] if m["pe_5y_avg"] == m["pe_5y_avg"] else np.nan
    m["pb_now"], m["pb_5y_avg"], m["pb_vs_hist"] = hist_ratio(c, "P/Book")
    m["ptbv_now"] = c.ltm("Multiples", "P/Tangible Book")
    m["p_ffo_now"], m["p_ffo_5y_avg"], m["p_ffo_vs_hist"] = hist_ratio(c, "Price/T12M FFO per Share")
    m["fcf_yield"] = c.ltm("Yield Analysis", "Free Cash Flow Yield")
    m["shareholder_yield"] = c.ltm("Yield Analysis", "T12 Shareholder Yield, Ex Debt")
    # --- Balance sheet
    m["net_debt_ebitda"] = c.ltm("Credit", "Net Debt/EBITDA")
    cov = c.ltm("Credit", "EBIT to Interest Expense")
    if np.isnan(cov):
        cov = c.ltm("Credit", "EBITDA to Interest Expense")
    m["interest_coverage"] = cov
    m["debt_to_equity"] = c.ltm("Credit", "Total Debt/Equity")
    m["tier1_common_pct"] = c.ltm("Adj Highlights", "Tier 1 Common Eqty %")
    m["combined_ratio"] = c.ltm("Adj Highlights", "Combined Ratio (NL)")
    # --- Growth
    rev = c.first(("Adj Highlights", "Revenue, Adj"), ("Adj Highlights", "Net Revenue, Adj"), how="annual")
    # Structural break (spin-off / big divestiture): a >40% one-year revenue drop restarts the window.
    m["growth_note"] = ""
    r = rev.dropna()
    breaks = [i for i in range(1, len(r)) if r.iloc[i] < 0.6 * r.iloc[i - 1]]
    if breaks and 3 <= len(r) - breaks[-1] <= 3:   # only when the break falls inside the 3-year window
        r = r.iloc[breaks[-1]:]
        m["growth_note"] = f"revenue break in {r.index[0]}; growth measured from then"
    m["rev_cagr_3y"] = cagr(r, years=min(3, len(r) - 1))
    eps = c.first(("Adj Highlights", "EPS, Adj"), ("Adj Highlights", "FFO/Sh, Diluted"), how="annual")
    m["eps_cagr_3y"] = cagr(eps)
    m["eps_or_ffo"] = "FFO/sh" if k == "reit" and len(c.annual("Adj Highlights", "FFO/Sh, Diluted")) else "EPS"
    m["capex_to_revenue"] = c.ltm("CAPEX & Depreciation", "CAPEX/Sales")
    m["capex_to_revenue_3y_change"] = (lambda s: s.iloc[-1] - s.iloc[0] if len(s) >= 3 else np.nan)(
        c.annual("CAPEX & Depreciation", "CAPEX/Sales", n=4))
    # --- Momentum (filled later from the price file)
    m["ret_12_1m"] = m["ret_6_1m"] = np.nan
    # --- Red flags (framework Stage 1, step 2)
    flags = []
    f3 = fcf_a.dropna().iloc[-3:]
    m["fcf_neg_years_of_last3"] = int((f3 < 0).sum()) if len(f3) else np.nan
    if k in ("standard", "fin_services") and len(f3) == 3 and (f3 < 0).sum() >= 2:
        flags.append("FCF negative in 2 of last 3 years")
    nde = m["net_debt_ebitda"]
    if k in ("standard", "fin_services") and nde > 4.0:
        flags.append(f"Net debt/EBITDA {nde:.1f}x > 4.0x")
    if k == "utility" and nde > 6.0:
        flags.append(f"Net debt/EBITDA {nde:.1f}x > 6.0x (utility limit)")
    if k in ("standard", "fin_services") and cov < 3:   # utilities/REITs exempt (amended 13 Nov 2026)
        flags.append(f"Interest coverage {cov:.1f}x < 3x")
    e5 = eps.dropna().iloc[-6:]
    eps_falls = int((e5.diff().dropna() < 0).sum())
    if eps_falls >= 3 and m["rev_cagr_3y"] < 0:
        flags.append(f"EPS fell in {eps_falls} of last 5 years and revenue shrinking")
    if t in BEING_ACQUIRED:
        flags.append(BEING_ACQUIRED[t])
    m["red_flags"] = "; ".join(flags)
    return m


def main(raw, pool, index, out):
    d = pd.read_csv(raw)
    pool = pd.read_csv(pool)
    idx = pd.read_csv(index)
    idx = idx[~idx.file.str.startswith("_")]
    rows = []
    for _, p in pool.iterrows():
        f = idx[idx.pool_ticker == p.ticker].file.iloc[0]
        m = metrics(p.ticker, p.sector, Co(d[d.file == f]))
        m["source_file"] = f
        m["report_currency"] = idx[idx.pool_ticker == p.ticker].report_currency.iloc[0]
        rows.append(m)
    df = pd.DataFrame(rows)
    df.insert(3, "data_date", "2026-11-13")
    num = df.select_dtypes("number").columns
    df[num] = df[num].round(3)
    core = ["roic_latest", "roe_latest", "gross_profit_to_assets", "op_margin_5y_slope", "fcf_conversion_5y",
            "ev_ebitda_vs_hist", "pe_vs_hist", "fcf_yield", "shareholder_yield", "net_debt_ebitda",
            "interest_coverage", "rev_cagr_3y", "eps_cagr_3y"]
    df["missing_fields"] = df[core].apply(lambda r: ", ".join(c for c in core if pd.isna(r[c])), axis=1)
    df.to_csv(out, index=False)
    print(f"wrote {len(df)} rows -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
