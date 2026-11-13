"""Daily job: prices -> NAV -> charts -> README. Exits non-zero on any failure."""
import sys

import charts
import nav
import prices
import readme

for step in (prices, nav, charts, readme):
    code = step.main()
    if code:
        print(f"FAILED at {step.__name__}", file=sys.stderr)
        sys.exit(code)
