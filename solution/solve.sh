#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Step 1: consolidate the authoritative effective rate table (#TAR-7370) --
# The shipped /app/data/effective_rate_table.json fell behind the docket.
# Rebuild it from the filed base tariff plus the approved amendment filings and
# write it back to that path; no bill is correct until this is done.

python3 "${SCRIPT_DIR}/consolidate_rate_table.py"

# --- Step 2: restore the biller and issue the itemised bills -----------------

cp "${SCRIPT_DIR}/rate_bill_fixed.py" /app/workflow/rate_bill.py
python3 /app/workflow/rate_bill.py --output-dir /app/output
