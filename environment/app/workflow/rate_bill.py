#!/usr/bin/env python3
"""Regulated utility tariff biller (INCIDENT SNAPSHOT — DO NOT SHIP).

This is the biller as it stood when the mis-billing was reported. Several
stages still evaluate the January draft proposals and the February interim
decisions that the tariff commission later reversed, and it is run against a
rate table that was never consolidated, so the bills it issues are wrong.
Restore it to the commission's final decisions recorded in
/app/incident/tariff_governance_log.md.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

# Fixed absolute operational-input paths. --input selects the meter-read file
# only; the rate table, the register and the policy never become relative to it.
DEFAULT_INPUT = "/app/data/meter_reads.json"
DEFAULT_OUTPUT_DIR = "/app/output"
RATE_TABLE_PATH = "/app/data/effective_rate_table.json"
SERVICE_CLASS_REGISTER_PATH = "/app/data/service_class_register.json"
BILLING_POLICY_PATH = "/app/data/billing_policies.json"

SCHEMA_VERSION = "tariff-bill-v1"
TIER_ORDER = ["escalate", "review", "watch"]

# Draft/interim constants (pre-reversal).
DEFAULT_SERVICE_CLASS = "commercial"   # #TAR-7212 draft last-resort class
LEVY_BASIS = 10000
SCORE_TOTAL_DIV = 3000                 # #TAR-7240 draft divisor
SCORE_RATCHET_DIV = 5                  # #TAR-7240 draft divisor
ACCOUNT_CAP = 2

# Baseline billing policy (#TAR-7360). Any field the policy file omits keeps
# these values; the file may override per default and per service class.
POLICY_BASELINE = {
    "admission_min": 4,
    "escalate_total_cents": 120000,
    "escalate_score_min": 18,
    "escalate_ratchet_min": 40,
    "review_score_min": 8,
    "review_bracket_min": 3,
    "minimum_bill_cents": 1800,
    "minimum_bill_days_basis": 30,
    "ratchet_percent": 80,
    "ratchet_lookback_periods": 3,
    "levy_bps": 240,
}


def _ceil_div(numer: int, denom: int) -> int:
    """Integer ceiling for non-negative numer; ceil(x/n) == -(-x // n)."""
    return -(-numer // denom)


def _half_up_div(numer: int, denom: int) -> int:
    """Integer round-half-up for non-negative numer: add half the denominator."""
    return (numer + denom // 2) // denom


def canon_name(value: object) -> str:
    text = str(value).strip().lower()
    return text if text else "unknown"


def collapse_ws(value: object) -> str:
    return " ".join(str(value).split())


def coerce_int(value: object) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    text = str(value).strip()
    try:
        return int(text)
    except ValueError:
        try:
            return int(float(text))
        except ValueError:
            return 0


def coerce_flag(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def coerce_date(value: object) -> date | None:
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError:
        return None


# --------------------------------------------------------------------------
# Stage 1-2: canonicalize reads, drop undated reads, deduplicate (#TAR-7301/#TAR-7302)
# --------------------------------------------------------------------------
def canonicalize(raw_rows: list[dict]) -> tuple[list[dict], int]:
    rows: list[dict] = []
    dropped = 0
    for row in raw_rows:
        start = coerce_date(row.get("period_start", ""))
        end = coerce_date(row.get("period_end", ""))
        if start is None or end is None:
            dropped += 1
            continue
        rows.append(
            {
                "read_id": collapse_ws(row.get("read_id", "")),
                "account": canon_name(row.get("account", "")),
                "service_class": canon_name(row.get("service_class", "")),
                "period_start": start,
                "period_end": end,
                "consumption_kwh": max(coerce_int(row.get("consumption_kwh", 0)), 0),
                "peak_demand_kw": max(coerce_int(row.get("peak_demand_kw", 0)), 0),
                "estimated": coerce_flag(row.get("estimated", False)),
                "note": collapse_ws(row.get("note", "")),
            }
        )
    return rows, dropped


def deduplicate(rows: list[dict]) -> list[dict]:
    # #TAR-7302 interim: on a period_end tie keep the HIGHER consumption and
    # ignore whether the read was estimated (pre-#TAR-7304 reversal).
    best: dict[str, tuple] = {}
    order: dict[str, int] = {}
    for index, row in enumerate(rows):
        key = (
            row["period_end"].toordinal(),
            row["consumption_kwh"],
            -index,
        )
        read_id = row["read_id"]
        if read_id not in best or key > best[read_id]:
            best[read_id] = key
            order[read_id] = index
    keep = set(order.values())
    return [row for index, row in enumerate(rows) if index in keep]


# --------------------------------------------------------------------------
# Rate table, register and policy resolution (#TAR-7330, #TAR-7360, #TAR-7362)
# --------------------------------------------------------------------------
def load_schedules(table: dict) -> list[dict]:
    schedules = []
    for entry in table.get("schedules", []):
        effective = coerce_date(entry.get("effective_from", ""))
        if effective is None:
            continue
        classes = {}
        for name, spec in entry.get("classes", {}).items():
            classes[canon_name(name)] = {
                "brackets": [
                    {
                        "bracket_id": collapse_ws(b.get("bracket_id", "")),
                        "upper_kwh": None if b.get("upper_kwh") is None else coerce_int(b["upper_kwh"]),
                        "rate_per_kwh_cents": coerce_int(b.get("rate_per_kwh_cents", 0)),
                    }
                    for b in spec.get("brackets", [])
                ],
                "demand_rate_cents_per_kw": coerce_int(spec.get("demand_rate_cents_per_kw", 0)),
                "standing_charge_cents_per_day": coerce_int(
                    spec.get("standing_charge_cents_per_day", 0)
                ),
            }
        schedules.append({"effective_from": effective, "classes": classes})
    schedules.sort(key=lambda s: s["effective_from"])
    return schedules


def load_register(rows: list[dict]) -> dict[str, list[tuple[date, str]]]:
    register: dict[str, list[tuple[date, str]]] = {}
    for row in rows:
        effective = coerce_date(row.get("effective_from", ""))
        if effective is None:
            continue
        register.setdefault(canon_name(row.get("account", "")), []).append(
            (effective, canon_name(row.get("service_class", "")))
        )
    for entries in register.values():
        entries.sort(key=lambda item: item[0])
    return register


def schedule_for(schedules: list[dict], when: date) -> dict:
    # #TAR-7310: the latest schedule version whose effective_from is on or
    # before the day; a day before the earliest version uses the earliest.
    chosen = schedules[0]
    for schedule in schedules:
        if schedule["effective_from"] <= when:
            chosen = schedule
        else:
            break
    return chosen


def governing_class(
    account: str,
    declared: str,
    when: date,
    register: dict[str, list[tuple[date, str]]],
    schedule: dict,
) -> str:
    # #TAR-7212 draft precedence: the class declared on the read always wins and
    # the register is only a fallback.
    if declared and declared in schedule["classes"]:
        return declared
    chosen = ""
    for effective, name in register.get(account, []):
        if effective <= when:
            chosen = name
        else:
            break
    if chosen and chosen in schedule["classes"]:
        return chosen
    return DEFAULT_SERVICE_CLASS


def resolve_policy(service_class: str, policy_data: dict) -> dict:
    resolved = dict(POLICY_BASELINE)
    for field, value in policy_data.get("default", {}).items():
        if field in resolved:
            resolved[field] = coerce_int(value)
    override = policy_data.get("class_overrides", {}).get(service_class)
    if isinstance(override, dict):
        for field, value in override.items():
            if field in resolved:
                resolved[field] = coerce_int(value)
    return resolved


# --------------------------------------------------------------------------
# Stage 3: proration segments (#TAR-7310, #TAR-7312)
# --------------------------------------------------------------------------
def segment_period(
    period_start: date,
    period_end: date,
    schedules: list[dict],
    class_dates: list[date],
) -> list[tuple[date, date]]:
    bounds = {period_start}
    for candidate in [s["effective_from"] for s in schedules] + list(class_dates):
        if period_start < candidate <= period_end:
            bounds.add(candidate)
    ordered = sorted(bounds)
    segments = []
    for index, start in enumerate(ordered):
        if index + 1 < len(ordered):
            end = ordered[index + 1] - timedelta(days=1)
        else:
            end = period_end
        segments.append((start, end))
    return segments


def split_consumption(total_kwh: int, seg_days: list[int], total_days: int) -> list[int]:
    # #TAR-7216 draft: every segment rounds its own day-share half up and the
    # parts are not reconciled against the read.
    return [_half_up_div(total_kwh * days, total_days) for days in seg_days]


def bracket_charge(
    kwh: int, brackets: list[dict], seg_days: int, total_days: int
) -> tuple[int, list[str]]:
    # #TAR-7214 draft: each bounded ceiling is prorated by FLOOR and the ceiling
    # itself opens the next bracket rather than closing its own.
    charge = 0
    used: list[str] = []
    previous = 0
    for bracket in brackets:
        upper = bracket["upper_kwh"]
        if upper is None:
            take = max(kwh - previous, 0)
        else:
            prorated = upper * seg_days // total_days - 1
            take = max(min(kwh, prorated) - previous, 0)
            previous = max(previous, prorated)
        if take > 0:
            charge += take * bracket["rate_per_kwh_cents"]
            used.append(bracket["bracket_id"])
    return charge, used


# --------------------------------------------------------------------------
# Stage 4-7: the bill itself (#TAR-7320..#TAR-7350)
# --------------------------------------------------------------------------
def build_bill(
    read: dict,
    schedules: list[dict],
    register: dict[str, list[tuple[date, str]]],
    policy_data: dict,
    ratchet_floor_kw: int,
) -> dict:
    period_start = read["period_start"]
    period_end = read["period_end"]
    total_days = max((period_end - period_start).days + 1, 1)
    class_dates = [effective for effective, _ in register.get(read["account"], [])]
    segments = segment_period(period_start, period_end, schedules, class_dates)
    seg_days = [max((end - start).days + 1, 1) for start, end in segments]
    parts = split_consumption(read["consumption_kwh"], seg_days, total_days)

    billed_demand_kw = max(read["peak_demand_kw"], ratchet_floor_kw)

    energy = 0
    standing = 0
    demand = 0
    bracket_ids: set[str] = set()
    versions: set[str] = set()
    seg_classes: list[str] = []
    for (start, _end), days, kwh in zip(segments, seg_days, parts):
        schedule = schedule_for(schedules, start)
        service_class = governing_class(
            read["account"], read["service_class"], start, register, schedule
        )
        seg_classes.append(service_class)
        versions.add(schedule["effective_from"].isoformat())
        spec = schedule["classes"].get(
            service_class, {"brackets": [], "demand_rate_cents_per_kw": 0,
                            "standing_charge_cents_per_day": 0}
        )
        seg_energy, used = bracket_charge(kwh, spec["brackets"], days, total_days)
        energy += seg_energy
        bracket_ids.update(used)
        standing += days * spec["standing_charge_cents_per_day"]
        # #TAR-7222 draft: each segment's capacity charge rounds up.
        demand += _ceil_div(billed_demand_kw * spec["demand_rate_cents_per_kw"] * days, total_days)

    billed_class = seg_classes[-1]
    policy = resolve_policy(billed_class, policy_data)

    subtotal = energy + demand + standing
    # #TAR-7228 draft: the minimum bill is prorated with a floored day share.
    prorated_minimum = (
        policy["minimum_bill_cents"] * total_days // policy["minimum_bill_days_basis"]
    )
    minimum_applied = subtotal < prorated_minimum
    billed_subtotal = prorated_minimum if minimum_applied else subtotal
    # #TAR-7228 draft: the levy is charged on the subtotal before the floor.
    levy = subtotal * policy["levy_bps"] // LEVY_BASIS
    total_due = billed_subtotal + levy

    ratchet_uplift = billed_demand_kw - read["peak_demand_kw"]
    bracket_span = len(bracket_ids)
    # #TAR-7240 draft divisors.
    exception_score = (
        total_due // SCORE_TOTAL_DIV
        + ratchet_uplift // SCORE_RATCHET_DIV
        + max(bracket_span - 1, 0)
    )

    return {
        "account": read["account"],
        "read_id": read["read_id"],
        "service_class": billed_class,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "billed_days": total_days,
        "segment_count": len(segments),
        "segment_days": seg_days,
        "segment_consumption_kwh": parts,
        "consumption_kwh": read["consumption_kwh"],
        "peak_demand_kw": read["peak_demand_kw"],
        "ratchet_floor_kw": ratchet_floor_kw,
        "billed_demand_kw": billed_demand_kw,
        "ratchet_uplift_kw": ratchet_uplift,
        "bracket_ids": sorted(bracket_ids),
        "bracket_span": bracket_span,
        "schedule_versions_applied": sorted(versions),
        "energy_charge_cents": energy,
        "demand_charge_cents": demand,
        "standing_charge_cents": standing,
        "subtotal_cents": subtotal,
        "minimum_applied": minimum_applied,
        "billed_subtotal_cents": billed_subtotal,
        "levy_cents": levy,
        "total_due_cents": total_due,
        "estimated": read["estimated"],
        "exception_score": exception_score,
        "_policy": policy,
    }


def assign_tier(bill: dict, policy: dict) -> str:
    # #TAR-7244 draft tiering: no ratchet clause on escalate, and review keyed on
    # the score and the estimated flag alone.
    if (
        bill["total_due_cents"] >= policy["escalate_total_cents"]
        or bill["exception_score"] >= policy["escalate_score_min"]
    ):
        return "escalate"
    if bill["exception_score"] >= policy["review_score_min"] or bill["estimated"]:
        return "review"
    return "watch"


BILL_FIELDS = (
    "read_id",
    "service_class",
    "period_start",
    "period_end",
    "billed_days",
    "segment_count",
    "segment_days",
    "segment_consumption_kwh",
    "consumption_kwh",
    "peak_demand_kw",
    "ratchet_floor_kw",
    "billed_demand_kw",
    "ratchet_uplift_kw",
    "bracket_ids",
    "bracket_span",
    "schedule_versions_applied",
    "energy_charge_cents",
    "demand_charge_cents",
    "standing_charge_cents",
    "subtotal_cents",
    "minimum_applied",
    "billed_subtotal_cents",
    "levy_cents",
    "total_due_cents",
    "estimated",
    "exception_score",
)
QUEUE_FIELDS = ("bill_id", "account", *BILL_FIELDS, "tier")


def run(input_path: str, output_dir: str) -> None:
    raw_rows = json.loads(Path(input_path).read_text(encoding="utf-8"))
    table = json.loads(Path(RATE_TABLE_PATH).read_text(encoding="utf-8"))
    register_rows = json.loads(Path(SERVICE_CLASS_REGISTER_PATH).read_text(encoding="utf-8"))
    policy_data = json.loads(Path(BILLING_POLICY_PATH).read_text(encoding="utf-8"))

    schedules = load_schedules(table)
    register = load_register(register_rows)

    reads, dropped = canonicalize(raw_rows)
    reads = deduplicate(reads)

    by_account: dict[str, list[dict]] = {}
    for read in reads:
        by_account.setdefault(read["account"], []).append(read)

    bills: list[dict] = []
    for account in sorted(by_account):
        history: list[int] = []
        ordered = sorted(
            by_account[account],
            key=lambda r: (r["period_start"], r["period_end"], r["read_id"]),
        )
        for read in ordered:
            # #TAR-7220 interim: the ratchet carries forward the previous periods'
            # BILLED demand and floors the percentage.
            probe_class = governing_class(
                read["account"],
                read["service_class"],
                read["period_end"],
                register,
                schedule_for(schedules, read["period_end"]),
            )
            probe_policy = resolve_policy(probe_class, policy_data)
            lookback = max(probe_policy["ratchet_lookback_periods"], 0)
            window = history[-lookback:] if lookback else []
            floor_kw = max(window) * probe_policy["ratchet_percent"] // 100 if window else 0
            bill = build_bill(read, schedules, register, policy_data, floor_kw)
            bills.append(bill)
            history.append(bill["billed_demand_kw"])

    queue_rows: list[dict] = []
    for bill in bills:
        policy = bill["_policy"]
        # #TAR-7352: score floor, or any bill the minimum-bill floor lifted.
        if bill["exception_score"] < policy["admission_min"] and not bill["minimum_applied"]:
            continue
        bill["tier"] = assign_tier(bill, policy)
        bill["bill_id"] = f"{bill['account']}:{bill['read_id']}:{bill['period_start']}"
        queue_rows.append(bill)

    tier_rank = {name: len(TIER_ORDER) - index for index, name in enumerate(TIER_ORDER)}
    queue_rows.sort(
        key=lambda b: (
            -tier_rank[b["tier"]],
            -b["exception_score"],
            -b["total_due_cents"],
            -b["energy_charge_cents"],
            -b["billed_demand_kw"],
            -b["consumption_kwh"],
            b["account"],
            b["period_start"],
            b["read_id"],
        )
    )
    seen: dict[str, int] = {}
    capped: list[dict] = []
    for bill in queue_rows:
        count = seen.get(bill["account"], 0)
        if count < ACCOUNT_CAP:
            capped.append(bill)
            seen[bill["account"]] = count + 1
    queue_rows = capped

    tier_counts = {tier: 0 for tier in TIER_ORDER}
    for bill in queue_rows:
        tier_counts[bill["tier"]] += 1

    def qmax(field: str) -> int:
        return max((b[field] for b in queue_rows), default=0)

    summary = {
        "schema_version": SCHEMA_VERSION,
        "raw_read_count": len(raw_rows),
        "unique_read_ids": len({collapse_ws(r.get("read_id", "")) for r in raw_rows}),
        "dropped_read_count": dropped,
        "canonical_read_count": len(reads),
        "account_count": len({b["account"] for b in bills}),
        "bill_count": len(bills),
        "estimated_bill_count": sum(1 for b in bills if b["estimated"]),
        "schedule_version_count": len(schedules),
        "tier_counts": tier_counts,
        "total_energy_charge_cents": sum(b["energy_charge_cents"] for b in bills),
        "total_demand_charge_cents": sum(b["demand_charge_cents"] for b in bills),
        "total_standing_charge_cents": sum(b["standing_charge_cents"] for b in bills),
        "total_levy_cents": sum(b["levy_cents"] for b in bills),
        "total_due_cents": sum(b["total_due_cents"] for b in bills),
        "minimum_applied_count": sum(1 for b in bills if b["minimum_applied"]),
        "queued_bill_count": len(queue_rows),
        "max_exception_score": qmax("exception_score"),
        "max_total_due_cents": qmax("total_due_cents"),
        "max_ratchet_uplift_kw": qmax("ratchet_uplift_kw"),
        "largest_bill_cents": max((b["total_due_cents"] for b in bills), default=0),
    }

    register_out: dict[str, list[dict]] = {}
    for bill in bills:
        register_out.setdefault(bill["account"], []).append(bill)
    out_register: dict[str, list[dict]] = {}
    for account in sorted(register_out):
        rows = sorted(register_out[account], key=lambda b: (b["period_start"], b["read_id"]))
        out_register[account] = [{f: b[f] for f in BILL_FIELDS} for b in rows]

    out_queue = [{f: b[f] for f in QUEUE_FIELDS} for b in queue_rows]

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "billing_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (out / "bill_register.json").write_text(
        json.dumps(out_register, indent=2) + "\n", encoding="utf-8"
    )
    with (out / "exception_queue.jsonl").open("w", encoding="utf-8") as handle:
        for row in out_queue:
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Regulated utility tariff biller")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    run(args.input, args.output_dir)


if __name__ == "__main__":
    main()
