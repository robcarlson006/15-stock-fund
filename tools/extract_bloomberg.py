#!/usr/bin/env python3
"""Parse Bloomberg 'Financial Statement Analysis' PDFs into one long CSV.

Usage: python3 -I tools/extract_bloomberg.py <pdf_dir> <out_csv>

Each output row = one number: ticker, section, subsection, label, occurrence,
column header (e.g. '2024 A', 'Current/LTM', 'Estimate:2027 A'), period end, value.
Numbers are assigned to columns by their position on the page (pdftotext -layout),
so blank years stay blank instead of shifting values left.
"""
import csv, glob, os, re, subprocess, sys

SECTIONS = {"Adj Highlights", "Enterprise Value", "Multiples", "Standardized", "Profitability",
            "Growth", "Credit", "Yield Analysis", "CAPEX & Depreciation",
            # Stage 2 templates
            "GAAP", "Earnings", "Liquidity", "DuPont Analysis", "SBC & Amort"}
# Sub-headers that wrap over several lines (Stage 2 SBC & Amort page); later lines are appended to them
MULTILINE_SUBS = {"Earnings Per Share", "Stock Based", "Amortization of", "Amortization of Total"}
SUBHEADERS = {"Returns", "Margins", "Additional", "1 Year Growth", "5 Year Growth", "Sequential Growth",
              "Reference Items", "Trailing 12 Month", "Values for Ratios", "Cash from Operating",
              "Cash From Operating", "Cash from Investing", "Cash From Investing", "Cash from Financing",
              "Cash From Financing", "T12 Cash Flows to", "T12 Cash Flows to the",
              # Stage 2: DuPont components and SBC page blocks
              "Tax Burden", "Adjustment Factor", "Interest Burden", "Operating Margin", "Asset Turnover",
              "Leverage Ratio", "Earnings Per Share", "Stock Based", "Amortization of", "Amortization of Total"}
# Block titles on the Stage 2 Earnings page; only treated as sub-headers inside that section
EARNINGS_BLOCKS = {"Revenue", "Earnings Per Share", "EBIT", "EBITDA", "Gross Margin %", "Pretax Income (Loss)",
                   "Net Income", "FFO Per Share"}
SKIP = re.compile(r"This report may not|Countries”\)|do not provide investment|Financial Statement Analysis|"
                  r"^Ticker:|^Filing:|^Bloomberg ®")
NUM = re.compile(r"(?<![\w.])-?\d[\d,]*\.?\d*(?![\w])")


def tokens_with_pos(line, pattern):
    return [(m.group(0), m.start(), m.end()) for m in pattern.finditer(line)]


def parse_pdf(path):
    text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    lines = text.splitlines()
    tk = re.search(r"Ticker:\s*(.+?) Equity", text).group(1).strip()
    rows, cols = [], []          # cols: list of (header, period_end, right_edge)
    section = sub = None
    pending_hdr = None           # header line text waiting for its 'For the period ending' line
    last = None                  # last emitted row-group (to append wrapped labels)
    parent = ""                  # last main label, for Average/High/Low rows
    occ = {}
    conts = 0                    # continuation lines already appended to `last`
    sub_fresh = False            # True between a sub-header and the first number row under it
    page_top = False             # True between a page header and that page's column header
    for raw in lines:
        if not raw.strip():
            last = None          # a wrapped label never continues across a blank line
            continue
        if SKIP.search(raw.strip()):
            if raw.strip().startswith(("Ticker:", "Filing:")):
                page_top = True      # section titles only ever appear here, above the column header
            continue
        s = raw.strip()
        if "Original:" in s or "Restated:" in s or "Current" in s and "Estimate:" in s:
            pending_hdr = [t for t in re.split(r"\s{2,}", s) if t]
            continue
        if s.startswith("For the period ending"):
            dates = list(re.finditer(r"\d{4}-\d{1,2}-\d{1,2}", raw))
            hdr = pending_hdr or [""] * len(dates)
            hdr = [h.replace("Original:", "").replace("Restated:", "") for h in hdr]
            if len(hdr) != len(dates):
                hdr = [""] * len(dates)
            cols = [(h, d.group(0), d.end()) for h, d in zip(hdr, dates)]
            last, page_top = None, False
            continue
        nums = tokens_with_pos(raw, NUM)
        # label = text before first number (numbers start well right of the label)
        first_num = next((n for n in nums if n[1] > 20), None)
        label = raw[: first_num[1]].strip() if first_num else s
        if not first_num:
            if s in SECTIONS and page_top:
                section, sub, last = s, None, None
                continue
            if s in SUBHEADERS or (section == "Earnings" and s in EARNINGS_BLOCKS):
                sub, last, sub_fresh = s, None, True
                continue
            if last is not None and (conts == 0 or s in ("Growth", "Average")):  # wrapped label
                old = last[0]["label"]
                for r in last:
                    r["label"] = (r["label"] + " " + s).strip()
                if parent == old:                 # keep Average/High/Low tied to the full label
                    parent = last[0]["label"]
                conts += 1
                continue
            last = None                   # a value-less row: stop any further appending
            if sub and sub_fresh and (sub.startswith(("Cash", "T12")) or sub.split(" | ")[0] in MULTILINE_SUBS
                        or any(sub.startswith(x + " ") for x in MULTILINE_SUBS)):   # wrapped sub-header
                sub = sub + " " + s
            continue
        vals = [n for n in nums if n[1] >= first_num[1]]
        if not cols:
            continue
        if label in ("Average", "High", "Low"):
            label = f"{parent} | {label}"
        else:
            parent = label
        group = []
        for v, st, en in vals:
            ci = min(range(len(cols)), key=lambda i: abs(cols[i][2] - en))
            if abs(cols[ci][2] - en) > 12:
                continue
            group.append({"bb_ticker": tk, "section": section, "sub": sub or "", "label": label,
                          "col": cols[ci][0], "period_end": cols[ci][1],
                          "value": float(v.replace(",", ""))})
        if group:
            last, conts, sub_fresh = group, 0, False
            rows.extend(group)
    # occurrence index per (section, sub, label) so repeated labels stay distinct
    seen = {}
    out = []
    prev_key = None
    for r in rows:
        key = (r["section"], r["sub"], r["label"])
        ck = key + (r["period_end"], r["col"])
        n = seen.get(ck, 0)
        seen[ck] = n + 1
        r["occurrence"] = n
        out.append(r)
    return out


def main(pdf_dir, out_csv):
    fields = ["file", "bb_ticker", "section", "sub", "label", "occurrence", "col", "period_end", "value"]
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for p in sorted(glob.glob(os.path.join(pdf_dir, "*.pdf"))):
            for r in parse_pdf(p):
                r["file"] = os.path.basename(p)
                w.writerow(r)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
