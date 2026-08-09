#!/usr/bin/env python3
"""Consolidate the base tariff with the approved amendment filings.

Implements the commission's final consolidation decision (#TAR-7370 in
/app/incident/tariff_governance_log.md), which supersedes the #TAR-7208 draft
and revises the #TAR-7231 interim: only approved filings consolidate, filings
are applied in ascending (effective_date, filed_on, filing_id) order, a later
filing supersedes an earlier one for the same bracket, a retired bracket is
reinstated by a later add filing, filing bookkeeping never reaches the table,
and one schedule version is emitted per distinct effective date carrying the
cumulative state of the tariff on that date.
"""

from __future__ import annotations

import json
from pathlib import Path

BASE_TARIFF_PATH = Path("/app/data/base_tariff.json")
AMENDMENT_PATH = Path("/app/data/amendment_filings.json")
RATE_TABLE_PATH = Path("/app/data/effective_rate_table.json")

BRACKET_FIELDS = ("bracket_id", "upper_kwh", "rate_per_kwh_cents")


def _norm(value: object) -> str:
    return str(value).strip().lower()


def _bracket(raw: dict) -> dict:
    upper = raw.get("upper_kwh")
    return {
        "bracket_id": str(raw.get("bracket_id", "")).strip(),
        "upper_kwh": None if upper is None else int(upper),
        "rate_per_kwh_cents": int(raw.get("rate_per_kwh_cents", 0)),
    }


def _sort_brackets(brackets: list[dict]) -> list[dict]:
    # ascending upper_kwh, the unbounded bracket last, ties broken by bracket_id.
    return sorted(
        brackets,
        key=lambda b: (1, 0, b["bracket_id"])
        if b["upper_kwh"] is None
        else (0, b["upper_kwh"], b["bracket_id"]),
    )


def _start_state(base: dict) -> dict[str, dict]:
    return {
        _norm(name): {
            "brackets": [_bracket(b) for b in entry.get("brackets", [])],
            "demand_rate_cents_per_kw": int(entry.get("demand_rate_cents_per_kw", 0)),
            "standing_charge_cents_per_day": int(entry.get("standing_charge_cents_per_day", 0)),
        }
        for name, entry in base.get("classes", {}).items()
    }


def _snapshot(working: dict[str, dict]) -> dict:
    snapshot = {}
    for name in sorted(working):
        entry = working[name]
        snapshot[name] = {
            "brackets": [
                {field: bracket[field] for field in BRACKET_FIELDS}
                for bracket in _sort_brackets(entry["brackets"])
            ],
            "demand_rate_cents_per_kw": entry["demand_rate_cents_per_kw"],
            "standing_charge_cents_per_day": entry["standing_charge_cents_per_day"],
        }
    return snapshot


def _apply(working: dict[str, dict], filing: dict) -> None:
    entry = working.get(_norm(filing.get("service_class", "")))
    if entry is None:
        return
    operation = _norm(filing.get("operation", ""))
    if operation == "adjust-demand-charge":
        entry["demand_rate_cents_per_kw"] = int(filing.get("demand_rate_cents_per_kw", 0))
    elif operation == "retire-bracket":
        target = str(filing.get("bracket_id", "")).strip()
        entry["brackets"] = [b for b in entry["brackets"] if b["bracket_id"] != target]
    elif operation in ("replace-bracket", "add-bracket"):
        # A later filing supersedes an earlier one for the same bracket_id, and an
        # add filing reinstates a bracket that an earlier filing retired.
        incoming = _bracket(filing.get("bracket", {}))
        entry["brackets"] = [
            b for b in entry["brackets"] if b["bracket_id"] != incoming["bracket_id"]
        ] + [incoming]


def _filing_order(filing: dict) -> tuple[str, str, str]:
    return (
        str(filing.get("effective_date", "")).strip(),
        str(filing.get("filed_on", "")).strip(),
        str(filing.get("filing_id", "")).strip(),
    )


def consolidate(base: dict, filings: list[dict]) -> dict:
    base_from = str(base.get("effective_from", "")).strip()
    approved = sorted(
        (f for f in filings if _norm(f.get("status", "")) == "approved"),
        key=_filing_order,
    )
    # One schedule version per distinct effective date, never earlier than the base.
    dates = sorted({base_from} | {max(_filing_order(f)[0], base_from) for f in approved})

    working = _start_state(base)
    schedules = []
    index = 0
    for date in dates:
        while index < len(approved) and max(_filing_order(approved[index])[0], base_from) <= date:
            _apply(working, approved[index])
            index += 1
        schedules.append({"effective_from": date, "classes": _snapshot(working)})

    return {"tariff_id": str(base.get("tariff_id", "")).strip(), "schedules": schedules}


def main() -> None:
    base = json.loads(BASE_TARIFF_PATH.read_text(encoding="utf-8"))
    filings = json.loads(AMENDMENT_PATH.read_text(encoding="utf-8"))
    table = consolidate(base, filings)
    RATE_TABLE_PATH.write_text(json.dumps(table, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
