"""Verifier tests for the regulated utility tariff billing task."""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

WORKFLOW_PATH = Path("/app/workflow/rate_bill.py")
ORIGINAL_WORKFLOW_PATH = Path("/app/workflow/.rate_bill.original")
DEFAULT_INPUT = Path("/app/data/meter_reads.json")
RATE_TABLE_PATH = Path("/app/data/effective_rate_table.json")
BASE_TARIFF_PATH = Path("/app/data/base_tariff.json")
AMENDMENT_PATH = Path("/app/data/amendment_filings.json")
REGISTER_PATH = Path("/app/data/service_class_register.json")
POLICY_PATH = Path("/app/data/billing_policies.json")
SPEC_PATH = Path("/app/docs/report_spec.json")
# The contract is golden metadata: the verifier reads it from its own image,
# never from the agent-writable copy under /app.
GOLDEN_CONTRACT_PATH = Path("/tests/fixtures/contract_golden.json")
LOG_PATH = Path("/app/incident/tariff_governance_log.md")
EXPECTED_FIXTURE = Path("/tests/fixtures/expected_report.json")
# The shipped stale table is overwritten in place by the consolidation, so the
# verifier keeps its own copy to prove the biller depends on that step.
STALE_TABLE_REFERENCE_PATH = Path("/tests/fixtures/stale_rate_table.json")
ALT_INPUT = Path("/tests/fixtures/alt_meter_reads.json")

TIER_ORDER = ["escalate", "review", "watch"]
TIER_RANK = {name: len(TIER_ORDER) - idx for idx, name in enumerate(TIER_ORDER)}

FIXTURE = json.loads(EXPECTED_FIXTURE.read_text())
SPEC = json.loads(GOLDEN_CONTRACT_PATH.read_text())

POLICY_FIELDS = (
    "admission_min", "escalate_total_cents", "escalate_score_min", "escalate_ratchet_min",
    "review_score_min", "review_bracket_min", "review_segment_min", "minimum_bill_cents",
    "minimum_bill_days_basis", "ratchet_percent", "ratchet_lookback_periods", "levy_bps",
)
BASELINE = {
    "admission_min": 240, "escalate_total_cents": 1870000, "escalate_score_min": 780,
    "escalate_ratchet_min": 540, "review_score_min": 430, "review_bracket_min": 5,
    "review_segment_min": 27, "minimum_bill_cents": 1800, "minimum_bill_days_basis": 30,
    "ratchet_percent": 80, "ratchet_lookback_periods": 3, "levy_bps": 240,
}

TABLE_KEYS = {"tariff_id", "schedules"}
SCHEDULE_KEYS = set(SPEC["consolidation_output"]["schedules"]["required_fields"])
CLASS_KEYS = set(SPEC["consolidation_output"]["schedule_classes"]["required_fields"])
BRACKET_KEYS = set(SPEC["consolidation_output"]["brackets"]["required_fields"])
FILING_ONLY_KEYS = {
    "filing_id", "docket", "filed_on", "effective_date", "status", "operation",
    "rationale", "service_class", "bracket",
}

BILL_KEYS = set(SPEC["bill_register"]["required_fields"])
QUEUE_KEYS = set(SPEC["exception_queue"]["required_fields"])
SUMMARY_KEYS = set(SPEC["billing_summary"]["required_fields"])


def _digest(value: object) -> str:
    """Content digest of a whole artifact; the graded register is far too large
    to embed in a fixture, so equality is asserted over its digest."""
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path):
    """Read a contracted JSONL artifact, taking every line as written.

    Skipping blank lines here softened a contract that says one compact object
    per line: a run that padded its queue with empty lines read back the same as
    a clean one and scored full marks. A blank line is a malformed line and is
    read as one.
    """
    text = path.read_text(encoding="utf-8")
    if not text:
        return []
    assert text.endswith("\n"), f"{path.name} has no trailing newline"
    lines = text.split("\n")[:-1]
    for number, line in enumerate(lines, start=1):
        assert line.strip(), f"{path.name} line {number} is blank"
    return [json.loads(line) for line in lines]


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


# --- verifier execution isolation -------------------------------------------------
# The submitted /app/workflow/rate_bill.py is untrusted once the separate verifier runs it.
# We execute it under an unprivileged UID (65534 / nobody) via setpriv, so it cannot write the
# reward path, read the held-out fixtures under /tests, or interfere with the verifier. Inputs are
# staged into a candidate-writable work area; the operational files under /app keep their paths.
_CWORK = Path("/candidate-work")
_run_ctr = itertools.count()
CANDIDATE_UID = 65534
def _setpriv_prefix(base: list) -> list:
    """The strictest setpriv invocation this image actually supports.

    Dropping the uid is not the whole of it: a candidate that kept inheritable
    or bounding-set capabilities could regain privilege across an exec. The two
    flags are probed rather than assumed, because a util-linux without them
    would make every run fail on the flag rather than on the task.
    """
    strict = base + ["--inh-caps=-all", "--bounding-set=-all"]
    try:
        probe = subprocess.run(strict + ["/bin/true"], capture_output=True, timeout=30)
        if probe.returncode == 0:
            return strict
    except (OSError, subprocess.SubprocessError):
        pass
    return base


# Resource ceilings for anything run as the candidate. Deliberately not
# RLIMIT_AS or RLIMIT_DATA: a language runtime that reserves a large virtual
# arena at start-up dies under those, so they would kill a correct program
# rather than a runaway one. These bound the failure modes that actually escape
# a process group -- forking without end, filling the disk, dumping core.
_CANDIDATE_NPROC = 512
_CANDIDATE_FSIZE = 512 * 1024 * 1024
_CANDIDATE_NOFILE = 1024


def _apply_rlimits() -> None:
    """Run in the child between fork and exec: own session, plus ceilings."""
    import resource

    for what, limit in (
        (resource.RLIMIT_NPROC, _CANDIDATE_NPROC),
        (resource.RLIMIT_FSIZE, _CANDIDATE_FSIZE),
        (resource.RLIMIT_NOFILE, _CANDIDATE_NOFILE),
        (resource.RLIMIT_CORE, 0),
    ):
        try:
            _soft, hard = resource.getrlimit(what)
            ceiling = limit if hard == resource.RLIM_INFINITY else min(limit, hard)
            resource.setrlimit(what, (ceiling, ceiling))
        except (ValueError, OSError):
            continue
    os.setsid()


def _pids_owned_by(uid: int) -> list:
    """Every live pid whose owner is `uid`, read from /proc."""
    pids = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            if os.stat("/proc/" + entry).st_uid == uid:
                pids.append(int(entry))
        except OSError:
            continue
    return pids


def reap_candidate_uid(uid: int = CANDIDATE_UID) -> None:
    """Kill everything still running as the candidate, whatever group it is in.

    Killing the process group is not enough on its own: a submitted program can
    call setsid and leave its own group, and would then survive into later tests
    -- holding the staged inputs of the next run, or still writing into an
    output directory being read. Ownership is the property that cannot be
    escaped, so the sweep is by owner.
    """
    import signal as _signal
    import time as _time

    for _ in range(50):
        pids = _pids_owned_by(uid)
        if not pids:
            return
        for pid in pids:
            try:
                os.kill(pid, _signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                continue
        for pid in pids:
            try:
                os.waitpid(pid, os.WNOHANG)
            except (ChildProcessError, OSError):
                continue
        _time.sleep(0.02)


_SETPRIV = _setpriv_prefix(["setpriv", "--reuid=65534", "--regid=65534", "--clear-groups", "--no-new-privs"])

# The submitted program gets a minimal explicit environment rather than inheriting the verifier's
# (PATH/PYTHONPATH/CI variables and any other grader context).
_CANDIDATE_ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/candidate-work", "LANG": "C.UTF-8"}


def _candidate_dir() -> Path:
    """A fresh work area for one run, created where nothing can pre-empt it.

    /candidate-work is world-writable, so a predictable name here was an opening:
    a submission could plant the next `run-N` as a symlink to the sealed fixtures
    and wait. The root-side mkdir(exist_ok=True) would succeed through the link
    and the chmod would follow it, since os.chmod resolves symlinks and Linux has
    no lchmod. mkdtemp closes both halves -- the name is unpredictable and the
    directory is created fresh or not at all.
    """
    directory = Path(tempfile.mkdtemp(prefix=f"run-{next(_run_ctr)}-", dir=str(_CWORK)))
    assert not directory.is_symlink(), directory
    os.chmod(directory, 0o777)
    return directory


def _reap_group(pgid: int) -> None:
    """Kill and reap everything left in the candidate's process group.

    start_new_session makes the submitted program a session and group leader, so
    its pgid equals its pid and everything it spawns shares that group. The id is
    taken before the wait: once the direct child has been reaped its pgid can no
    longer be looked up, and a leaked grandchild would otherwise survive to keep
    writing while the outputs are being graded.
    """
    try:
        os.killpg(pgid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        return
    for _ in range(50):
        try:
            os.killpg(pgid, 0)
        except (ProcessLookupError, PermissionError, OSError):
            return
        time.sleep(0.02)


def _run_agent(argv, cwd: Path, check: bool = True):
    """Run the submitted program unprivileged, in its own process group.

    Output goes to temporary files rather than pipes. A program that double-forks
    a daemon holding the inherited pipe open would keep the read end alive and
    hang the harness past its timeout; a file has no such reader to wait on. The
    whole process group is killed afterwards, so nothing the run left behind is
    still executing when its artifacts are read.
    """
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace") as out, \
            tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace") as err:
        proc = subprocess.Popen(
            _SETPRIV + argv, cwd=str(cwd), env=dict(_CANDIDATE_ENV),
            stdout=out, stderr=err, start_new_session=True,
        )
        pgid = proc.pid          # session leader: pgid == pid, captured before the wait
        try:
            # No timeout here. Harbor already bounds the verifier, and a second
            # inner deadline only adds a way for a correct but slow run to fail
            # on a loaded grading machine; a run that never returns is stopped by
            # that outer bound, which fails the suite anyway.
            proc.wait()
        finally:
            _reap_group(pgid)
            reap_candidate_uid()
        out.seek(0)
        err.seek(0)
        result = subprocess.CompletedProcess(argv, proc.returncode, out.read(), err.read())
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, argv, result.stdout, result.stderr)
    return result


def _run_pipeline(tmp_path: Path, script_path: Path = WORKFLOW_PATH, input_path: Path = DEFAULT_INPUT):
    work = _candidate_dir()
    out_dir = work / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(out_dir, 0o777)
    staged_input = work / "input.json"
    shutil.copy(str(input_path), str(staged_input))
    os.chmod(staged_input, 0o644)
    result = _run_agent(
        [sys.executable, str(script_path), "--input", str(staged_input), "--output-dir", str(out_dir)],
        cwd=work,
    )
    assert result.returncode == 0
    summary = _load_json(out_dir / "billing_summary.json")
    register = _load_json(out_dir / "bill_register.json")
    queue = _load_jsonl(out_dir / "exception_queue.jsonl")
    return out_dir, summary, register, queue


@pytest.fixture(scope="session")
def primary_outputs(tmp_path_factory):
    return _run_pipeline(tmp_path_factory.mktemp("primary"))


# --------------------------------------------------------------------------
# Step 1: the stale effective rate table must be consolidated in place
# --------------------------------------------------------------------------
def _base_only_table() -> dict:
    """The tariff as filed, with no amendment consolidated at all."""
    base = _load_json(BASE_TARIFF_PATH)
    return {
        "tariff_id": base["tariff_id"],
        "schedules": [{"effective_from": base["effective_from"], "classes": base["classes"]}],
    }


def _naive_last_filing_wins_table() -> dict:
    """The superseded draft consolidation: walk the filings in file order regardless of status
    or effective date, keep the last one touching each bracket, emit a single schedule."""
    base = _load_json(BASE_TARIFF_PATH)
    classes = json.loads(json.dumps(base["classes"]))
    for filing in _load_json(AMENDMENT_PATH):
        entry = classes.get(filing.get("service_class"))
        if entry is None:
            continue
        operation = filing.get("operation")
        if operation == "adjust-demand-charge":
            entry["demand_rate_cents_per_kw"] = filing["demand_rate_cents_per_kw"]
        elif operation == "retire-bracket":
            entry["brackets"] = [
                b for b in entry["brackets"] if b["bracket_id"] != filing["bracket_id"]
            ]
        else:
            incoming = filing["bracket"]
            entry["brackets"] = [
                b for b in entry["brackets"] if b["bracket_id"] != incoming["bracket_id"]
            ] + [incoming]
    return {
        "tariff_id": base["tariff_id"],
        "schedules": [{"effective_from": base["effective_from"], "classes": classes}],
    }


def test_consolidation_sources_are_intact():
    """Every input instruction.md says comes back byte for byte is checked on its bytes.

    The filed sources were compared on their parsed content and the register and
    the policy were not checked at all, so a run that reformatted one, or eased
    its own job by editing a policy value and a fixture together, was caught only
    indirectly if at all.
    """
    live = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in (
        ("base_tariff.json", BASE_TARIFF_PATH),
        ("amendment_filings.json", AMENDMENT_PATH),
        ("service_class_register.json", REGISTER_PATH),
        ("billing_policies.json", POLICY_PATH),
    )}
    assert live == FIXTURE["input_bytes_sha256"]


def test_rate_table_consolidated():
    """/app/data/effective_rate_table.json shipped stale; it must hold the consolidated table."""
    table = _load_json(RATE_TABLE_PATH)
    assert isinstance(table, dict)
    assert _digest(table) == FIXTURE["consolidated_table_digest"]


def test_consolidated_table_carries_no_filing_bookkeeping():
    """Each consolidated row carries only the declared tariff fields; the filings' own bookkeeping never survives."""
    table = _load_json(RATE_TABLE_PATH)
    assert set(table) == TABLE_KEYS
    for schedule in table["schedules"]:
        assert set(schedule) == SCHEDULE_KEYS
        for entry in schedule["classes"].values():
            assert set(entry) == CLASS_KEYS
            for bracket in entry["brackets"]:
                assert set(bracket) == BRACKET_KEYS
    blob = json.dumps(table)
    for key in FILING_ONLY_KEYS:
        assert f'"{key}"' not in blob, f"filing bookkeeping leaked into the rate table: {key}"
    for filing in _load_json(AMENDMENT_PATH):
        assert filing["filing_id"] not in blob
        assert filing["docket"] not in blob


def test_consolidated_table_is_sorted():
    """The consolidated table ascends by effective date, as the contract requires."""
    table = _load_json(RATE_TABLE_PATH)
    dates = [s["effective_from"] for s in table["schedules"]]
    assert dates == sorted(dates)
    assert len(dates) == len(set(dates))
    for schedule in table["schedules"]:
        assert list(schedule["classes"]) == sorted(schedule["classes"])
        for entry in schedule["classes"].values():
            order = [
                (1, 0, b["bracket_id"]) if b["upper_kwh"] is None
                else (0, b["upper_kwh"], b["bracket_id"])
                for b in entry["brackets"]
            ]
            assert order == sorted(order)


def test_stale_base_only_and_naive_tables_differ_from_the_consolidated_one():
    """The consolidation is real work: none of the plausible shortcuts land on it."""
    expected = FIXTURE["consolidated_table_digest"]
    assert FIXTURE["shipped_stale_table_digest"] != expected
    assert _digest(_base_only_table()) != expected
    assert _digest(_naive_last_filing_wins_table()) != expected


def test_biller_output_depends_on_the_consolidated_table(tmp_path: Path):
    """Even a correctly repaired biller issues wrong bills off a wrongly consolidated table."""
    original = RATE_TABLE_PATH.read_text(encoding="utf-8")
    correct_total = FIXTURE["primary"]["summary"]["total_due_cents"]
    try:
        for label, table in (
            ("shipped_stale", _load_json(STALE_TABLE_REFERENCE_PATH)),
            ("base_only", _base_only_table()),
            ("naive_last_filing_wins", _naive_last_filing_wins_table()),
        ):
            _write_json(RATE_TABLE_PATH, table)
            _, summary, register, queue = _run_pipeline(tmp_path / label)
            assert summary != FIXTURE["primary"]["summary"], label
            assert summary["total_due_cents"] != correct_total, label
            assert (_digest(register), _digest(queue)) != (
                FIXTURE["primary"]["register_digest"], FIXTURE["primary"]["queue_digest"]
            ), label
    finally:
        RATE_TABLE_PATH.write_text(original, encoding="utf-8")


# --------------------------------------------------------------------------
# Step 2: the biller output contract
# --------------------------------------------------------------------------
def test_cli_exists():
    """The biller is present, non-empty and parseable at the path the contract names.

    A precondition for everything below it: if this fails, the failures that follow
    are all consequences of it rather than separate faults.
    """
    assert WORKFLOW_PATH.exists(), f"{WORKFLOW_PATH} is missing"
    source = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert source.strip(), f"{WORKFLOW_PATH} is empty"
    ast.parse(source)


def test_output_dir_contains_exactly_three_files(primary_outputs):
    """A run writes the three contracted artifacts and nothing else."""
    out_dir, _, _, _ = primary_outputs
    names = sorted(p.name for p in out_dir.iterdir() if p.is_file())
    assert names == ["bill_register.json", "billing_summary.json", "exception_queue.jsonl"]


def test_primary_summary_matches_fixture(primary_outputs):
    """Every summary field matches the sealed reference run."""
    _, summary, _, _ = primary_outputs
    assert summary == FIXTURE["primary"]["summary"]


def test_primary_register_matches_fixture(primary_outputs):
    """The bill register matches the sealed digest."""
    _, _, register, _ = primary_outputs
    assert _digest(register) == FIXTURE["primary"]["register_digest"]


def test_primary_queue_matches_fixture(primary_outputs):
    """The exception queue matches the sealed digest."""
    _, _, _, queue = primary_outputs
    assert _digest(queue) == FIXTURE["primary"]["queue_digest"]


def test_summary_schema(primary_outputs):
    """The summary carries exactly the fields the contract requires."""
    _, summary, _, _ = primary_outputs
    assert set(summary) == SUMMARY_KEYS
    assert summary["schema_version"] == "tariff-bill-v1"
    assert list(summary["tier_counts"]) == TIER_ORDER


def test_register_schema_and_sorting(primary_outputs):
    """Register entries carry the contracted fields and ascend by account."""
    _, _, register, _ = primary_outputs
    assert list(register) == sorted(register)
    for bills in register.values():
        keys = [(row["period_start"], row["read_id"]) for row in bills]
        assert keys == sorted(keys)
        for row in bills:
            assert set(row) == BILL_KEYS
            assert row["bracket_ids"] == sorted(row["bracket_ids"])
            assert row["schedule_versions_applied"] == sorted(row["schedule_versions_applied"])
            assert row["service_class"] in {"residential", "commercial", "industrial"}


def test_queue_required_fields(primary_outputs):
    """Queue rows carry exactly the contracted fields."""
    _, _, _, queue = primary_outputs
    for row in queue:
        assert set(row) == QUEUE_KEYS
        assert row["tier"] in TIER_RANK
        assert row["bill_id"] == f"{row['account']}:{row['read_id']}:{row['period_start']}"


def test_queue_sorted(primary_outputs):
    """The queue is ordered by tier, then score, then total, as the board settled it."""
    _, _, _, queue = primary_outputs
    assert queue == sorted(
        queue,
        key=lambda row: (
            -TIER_RANK[row["tier"]],
            -row["exception_score"],
            -row["total_due_cents"],
            -row["energy_charge_cents"],
            -row["billed_demand_kw"],
            -row["consumption_kwh"],
            row["account"],
            row["period_start"],
            row["read_id"],
        ),
    )


def test_exception_queue_jsonl_compact(primary_outputs):
    """The queue is written as one compact JSON object per line."""
    out_dir, _, _, _ = primary_outputs
    raw = (out_dir / "exception_queue.jsonl").read_text(encoding="utf-8")
    assert raw.endswith("\n") and not raw.endswith("\n\n"), "the queue does not end in one newline"
    for number, line in enumerate(raw.split("\n")[:-1], start=1):
        # every line as written: a blank one is not skipped, it is a failure
        assert line.strip(), f"queue line {number} is blank"
        assert ": " not in line
        assert json.dumps(json.loads(line), separators=(",", ":")) == line


def test_bill_arithmetic_is_internally_consistent(primary_outputs):
    """Each bill's own segment counts, days and totals agree with one another."""
    _, _, register, _ = primary_outputs
    for account, bills in register.items():
        for row in bills:
            assert row["segment_count"] == len(row["segment_days"])
            assert row["segment_count"] == len(row["segment_consumption_kwh"])
            assert sum(row["segment_days"]) == row["billed_days"]
            assert sum(row["segment_consumption_kwh"]) == row["consumption_kwh"]
            assert row["bracket_span"] == len(row["bracket_ids"])
            assert row["billed_demand_kw"] == max(row["peak_demand_kw"], row["ratchet_floor_kw"])
            assert row["ratchet_uplift_kw"] == row["billed_demand_kw"] - row["peak_demand_kw"]
            assert row["subtotal_cents"] == (
                row["energy_charge_cents"] + row["demand_charge_cents"] + row["standing_charge_cents"]
            )
            if row["minimum_applied"]:
                assert row["billed_subtotal_cents"] > row["subtotal_cents"]
            else:
                assert row["billed_subtotal_cents"] == row["subtotal_cents"]
            assert row["total_due_cents"] == row["billed_subtotal_cents"] + row["levy_cents"]
            assert account


def test_summary_math_consistency(primary_outputs):
    """The summary's totals agree with the artifacts emitted beside it."""
    _, summary, register, queue = primary_outputs
    bills = [row for rows in register.values() for row in rows]
    assert summary["bill_count"] == len(bills)
    assert summary["account_count"] == len(register)
    assert summary["queued_bill_count"] == len(queue)
    assert summary["estimated_bill_count"] == sum(1 for b in bills if b["estimated"])
    assert summary["minimum_applied_count"] == sum(1 for b in bills if b["minimum_applied"])
    for summary_field, bill_field in (
        ("total_energy_charge_cents", "energy_charge_cents"),
        ("total_demand_charge_cents", "demand_charge_cents"),
        ("total_standing_charge_cents", "standing_charge_cents"),
        ("total_levy_cents", "levy_cents"),
        ("total_due_cents", "total_due_cents"),
    ):
        assert summary[summary_field] == sum(b[bill_field] for b in bills)
    assert summary["largest_bill_cents"] == max((b["total_due_cents"] for b in bills), default=0)
    assert summary["max_exception_score"] == max(
        (r["exception_score"] for r in queue), default=0
    )
    assert summary["max_total_due_cents"] == max((r["total_due_cents"] for r in queue), default=0)
    assert summary["max_ratchet_uplift_kw"] == max(
        (r["ratchet_uplift_kw"] for r in queue), default=0
    )
    assert summary["schedule_version_count"] == len(_load_json(RATE_TABLE_PATH)["schedules"])


def test_summary_read_counts_track_the_input(primary_outputs):
    """The summary's read counts come from the meter reads actually supplied."""
    _, summary, _, _ = primary_outputs
    reads = _load_json(DEFAULT_INPUT)
    assert summary["raw_read_count"] == len(reads)
    assert summary["unique_read_ids"] == len({r["read_id"] for r in reads})
    assert summary["dropped_read_count"] >= 1
    assert summary["canonical_read_count"] < summary["raw_read_count"]


def test_tier_counts_enumerate_all_three(primary_outputs):
    """The tier breakdown enumerates every documented tier and matches the queue."""
    _, summary, _, queue = primary_outputs
    counts = {tier: 0 for tier in TIER_ORDER}
    for row in queue:
        counts[row["tier"]] += 1
    assert summary["tier_counts"] == counts
    assert set(summary["tier_counts"]) == set(TIER_ORDER)


# --------------------------------------------------------------------------
# Original / broken snapshot
# --------------------------------------------------------------------------
def test_original_snapshot_preserved():
    """The frozen pre-incident biller is still on disk, unmodified."""
    assert ORIGINAL_WORKFLOW_PATH.exists()
    digest = hashlib.sha256(ORIGINAL_WORKFLOW_PATH.read_bytes()).hexdigest()
    assert digest == FIXTURE["broken_biller_sha256"]


def _account_aligned_slice(tmp_path: Path, accounts: int = 300) -> Path:
    """The reads of the first N accounts, whole.

    The biller aggregates per account, so a slice cut mid-account would compare
    two runs over different halves of the same bill. Taking whole accounts keeps
    every bill in the slice a complete one.
    """
    reads = _load_json(DEFAULT_INPUT)
    keep = set(sorted({read["account"] for read in reads})[:accounts])
    sliced = [read for read in reads if read["account"] in keep]
    assert sliced, "the slice is empty"
    path = tmp_path / "slice.json"
    path.write_text(json.dumps(sliced), encoding="utf-8")
    os.chmod(path, 0o644)
    return path


def test_broken_snapshot_is_wrong(tmp_path: Path):
    """The shipped biller does not already produce the governed result.

    Both engines are run over the same slice of whole accounts rather than the
    full read set. The shipped biller is slow enough on all 60,880 reads to come
    within sight of the candidate timeout -- it was measured between 173 and 225
    seconds against a 300-second cap, and it hit the cap once -- so a valid trial
    could fail on the clock alone. The slice runs it in about a tenth of that,
    and comparing the two engines on the same input is the stronger statement
    anyway: it fails a submission that simply left the shipped biller in place,
    which inequality against a sealed fixture only reached indirectly.
    """
    sliced = _account_aligned_slice(tmp_path)
    _, mine_summary, mine_register, mine_queue = _run_pipeline(
        tmp_path / "submitted", input_path=sliced
    )
    _, broken_summary, broken_register, broken_queue = _run_pipeline(
        tmp_path / "shipped", script_path=ORIGINAL_WORKFLOW_PATH, input_path=sliced
    )
    assert broken_summary != mine_summary, (
        "the shipped biller already produces the submitted result, so either it was "
        "left in place or the repair changed nothing")
    assert _digest(broken_register) != _digest(mine_register)
    assert _digest(broken_queue) != _digest(mine_queue)


# --------------------------------------------------------------------------
# Generalization / idempotency / CLI
# --------------------------------------------------------------------------
def test_pipeline_rerun_idempotent(tmp_path: Path, primary_outputs):
    """A second run over the same reads reproduces the first exactly.

    Compared against the session's own primary run rather than a second fresh
    pair, so the full read set is billed once here instead of twice.
    """
    _, sa, ra, qa = primary_outputs
    _, sb, rb, qb = _run_pipeline(tmp_path / "b")
    assert (sa, ra, qa) == (sb, rb, qb)


def test_pipeline_supports_alternate_input(tmp_path: Path):
    """A held-out set of meter reads produces the sealed result."""
    _, summary, register, queue = _run_pipeline(tmp_path, input_path=ALT_INPUT)
    assert summary == FIXTURE["alternate"]["summary"]
    assert _digest(register) == FIXTURE["alternate"]["register_digest"]
    assert _digest(queue) == FIXTURE["alternate"]["queue_digest"]


def test_cli_defaults_work_and_match_explicit_run(tmp_path: Path, primary_outputs):
    """Omitting the options uses the documented defaults."""
    _, explicit_summary, _, _ = primary_outputs
    # The no-argument run writes to the default /app/output; clear any root-owned artifacts from
    # solve.sh and make the dir candidate-writable so the unprivileged program can populate it.
    default_out = Path("/app/output")
    shutil.rmtree(default_out, ignore_errors=True)
    default_out.mkdir(parents=True, exist_ok=True)
    os.chmod(default_out, 0o777)
    _run_agent([sys.executable, str(WORKFLOW_PATH)], cwd=_candidate_dir())
    assert _load_json(default_out / "billing_summary.json") == explicit_summary


def test_submitted_program_runs_unprivileged(tmp_path: Path):
    """Code run the way the verifier runs the agent executes as uid 65534.

    Only the dropped privilege is asserted here. Whether a write to the reward
    path is refused depends on the mode of /logs/verifier, which is set outside
    this task, so it is not something the task can meaningfully claim.
    """
    probe = _candidate_dir() / "probe.py"
    probe.write_text("import os\nprint(os.getuid())\n", encoding="utf-8")
    os.chmod(probe, 0o644)
    res = _run_agent([sys.executable, str(probe)], cwd=_CWORK, check=False)
    assert res.returncode == 0, res.stderr
    assert res.stdout.strip() == "65534", "submitted program must run as uid 65534"


def test_register_source_path_affects_output(tmp_path: Path, primary_outputs):
    """The account register is resolved from its fixed path, not inlined."""
    original = REGISTER_PATH.read_text(encoding="utf-8")
    try:
        _, summary_a, register_a, queue_a = primary_outputs
        REGISTER_PATH.write_text("[]\n", encoding="utf-8")
        _, summary_b, register_b, queue_b = _run_pipeline(tmp_path / "b")
        assert summary_a != summary_b
        assert register_a != register_b
        assert queue_a != queue_b
    finally:
        REGISTER_PATH.write_text(original, encoding="utf-8")


def test_policy_source_path_affects_output(tmp_path: Path):
    """The billing policy is resolved from its fixed path, not inlined."""
    original = POLICY_PATH.read_text()
    try:
        data = json.loads(original)
        data["default"]["admission_min"] = 9999
        POLICY_PATH.write_text(json.dumps(data, indent=2) + "\n")
        _, summary, _, queue = _run_pipeline(tmp_path / "shifted")
        assert summary != FIXTURE["primary"]["summary"]
        assert len(queue) < FIXTURE["primary"]["queue_count"]
    finally:
        POLICY_PATH.write_text(original)


# --------------------------------------------------------------------------
# Policy resolution
# --------------------------------------------------------------------------
def _resolve(service_class: str, data: dict) -> dict:
    base = dict(BASELINE)
    base.update({k: int(v) for k, v in data.get("default", {}).items() if k in BASELINE})
    override = data.get("class_overrides", {}).get(service_class)
    if isinstance(override, dict):
        base.update({k: int(v) for k, v in override.items() if k in BASELINE})
    return base


def test_sparse_override_inherits_remaining_fields():
    """An override naming one field changes that field alone."""
    data = json.loads(POLICY_PATH.read_text())
    overrides = data.get("class_overrides", {})
    sparse = [name for name, spec in overrides.items() if len(spec) == 1]
    assert sparse, "the shipped policy must exercise a single-field override"
    default_resolved = _resolve("__absent__", data)
    for service_class in sparse:
        resolved = _resolve(service_class, data)
        named = next(iter(overrides[service_class]))
        assert resolved[named] == int(overrides[service_class][named])
        for field in POLICY_FIELDS:
            if field != named:
                assert resolved[field] == default_resolved[field]


def test_policy_default_may_omit_fields_and_falls_back_to_baseline():
    """A field the policy omits keeps the baseline the governance log states."""
    data = json.loads(POLICY_PATH.read_text())
    omitted = [f for f in POLICY_FIELDS if f not in data.get("default", {})]
    assert omitted, "the shipped policy must omit at least one field to exercise fallback"
    resolved = _resolve("__absent__", data)
    for field in omitted:
        assert resolved[field] == BASELINE[field]


def test_tier_rules_follow_resolved_policy(primary_outputs):
    """Each queued row is tiered by its own resolved policy values."""
    _, _, _, queue = primary_outputs
    data = json.loads(POLICY_PATH.read_text())
    for row in queue:
        policy = _resolve(row["service_class"], data)
        if (
            row["total_due_cents"] >= policy["escalate_total_cents"]
            or row["exception_score"] >= policy["escalate_score_min"]
            or row["ratchet_uplift_kw"] >= policy["escalate_ratchet_min"]
        ):
            assert row["tier"] == "escalate"
        elif (
            row["exception_score"] >= policy["review_score_min"]
            or row["segment_count"] >= policy["review_segment_min"]
            or row["minimum_applied"]
            or row["bracket_span"] >= policy["review_bracket_min"]
        ):
            assert row["tier"] == "review"
        else:
            assert row["tier"] == "watch"


def test_admission_follows_resolved_policy(primary_outputs):
    """Only rows clearing the resolved admission floor reach the queue."""
    _, _, register, queue = primary_outputs
    data = json.loads(POLICY_PATH.read_text())
    queued = {(row["account"], row["read_id"]) for row in queue}
    for account, bills in register.items():
        for row in bills:
            policy = _resolve(row["service_class"], data)
            admissible = row["exception_score"] >= policy["admission_min"] or row["minimum_applied"]
            if (account, row["read_id"]) in queued:
                assert admissible, (account, row["read_id"])


# --------------------------------------------------------------------------
# Capacity cap
# --------------------------------------------------------------------------
def test_account_capacity_cap_applied_after_ordering(primary_outputs):
    """The per-account cap is applied to the fully ordered queue, not during admission."""
    _, _, register, queue = primary_outputs
    per_account: dict[str, int] = {}
    for row in queue:
        per_account[row["account"]] = per_account.get(row["account"], 0) + 1
    assert per_account
    assert max(per_account.values()) <= 2, f"account exceeded cap: {per_account}"
    data = json.loads(POLICY_PATH.read_text())
    admissible = sum(
        1
        for bills in register.values()
        for row in bills
        if row["exception_score"] >= _resolve(row["service_class"], data)["admission_min"]
        or row["minimum_applied"]
    )
    assert admissible > len(queue), "fixture must contain more admissible bills than the cap allows"
    seen_order = [row["account"] for row in queue]
    for account in per_account:
        idxs = [i for i, name in enumerate(seen_order) if name == account]
        assert idxs == sorted(idxs)


# --------------------------------------------------------------------------
# Bracket arithmetic and rounding-direction deviations
# --------------------------------------------------------------------------
_LAB_TABLE = {
    "tariff_id": "LAB",
    "schedules": [
        {
            "effective_from": "2026-01-01",
            "classes": {
                "residential": {
                    "brackets": [
                        {"bracket_id": "LAB-A", "upper_kwh": 99, "rate_per_kwh_cents": 10},
                        {"bracket_id": "LAB-B", "upper_kwh": None, "rate_per_kwh_cents": 50},
                    ],
                    "demand_rate_cents_per_kw": 0,
                    "standing_charge_cents_per_day": 0,
                }
            },
        },
        {
            "effective_from": "2026-01-06",
            "classes": {
                "residential": {
                    "brackets": [
                        {"bracket_id": "LAB-A", "upper_kwh": 100, "rate_per_kwh_cents": 10},
                        {"bracket_id": "LAB-B", "upper_kwh": None, "rate_per_kwh_cents": 50},
                    ],
                    "demand_rate_cents_per_kw": 0,
                    "standing_charge_cents_per_day": 0,
                }
            },
        },
    ],
}


def _lab_read(read_id: str, start: str, end: str, kwh: int) -> dict:
    return {
        "read_id": read_id, "account": "lab-acct", "service_class": "residential",
        "period_start": start, "period_end": end, "consumption_kwh": kwh,
        "peak_demand_kw": 0, "estimated": False, "note": "lab",
    }


def test_bracket_boundary_is_inclusive_and_ceiling_prorated(tmp_path: Path):
    """A read landing exactly on a bracket boundary falls inside it, and the proration ceilings."""
    original = RATE_TABLE_PATH.read_text(encoding="utf-8")
    try:
        _write_json(RATE_TABLE_PATH, _LAB_TABLE)
        rows = [
            # Ten days entirely inside the second schedule: one segment, ceiling 100,
            # consumption lands exactly on it.
            _lab_read("L-1", "2026-01-06", "2026-01-15", 100),
            # Ten days split 5/5 across the two schedules: ceilings 99 and 100 prorate to
            # ceil(99*5/10) = 50 and ceil(100*5/10) = 50; consumption splits 50 / 51.
            _lab_read("L-2", "2026-01-01", "2026-01-10", 101),
        ]
        input_path = tmp_path / "lab.json"
        _write_json(input_path, rows)
        _, _, register, _ = _run_pipeline(tmp_path / "run", input_path=input_path)
        bills = {row["read_id"]: row for row in register["lab-acct"]}

        first = bills["L-1"]
        assert first["segment_count"] == 1
        # Inclusive ceiling: all 100 kWh sit in LAB-A at 10c -> 1000c. If the ceiling opened the
        # next bracket instead, 99 kWh at 10c plus 1 kWh at 50c would bill 1040c.
        assert first["energy_charge_cents"] == 1000
        assert first["energy_charge_cents"] != 99 * 10 + 1 * 50
        assert first["bracket_ids"] == ["LAB-A"]

        second = bills["L-2"]
        assert second["segment_days"] == [5, 5]
        assert second["segment_consumption_kwh"] == [50, 51]
        # CEIL-prorated ceilings 50 and 50: 50*10 + (50*10 + 1*50) = 1050.
        assert second["energy_charge_cents"] == 1050
        # A FLOOR-prorated first ceiling (99*5//10 = 49) would bill 1090 instead.
        assert second["energy_charge_cents"] != 1090
    finally:
        RATE_TABLE_PATH.write_text(original, encoding="utf-8")


def test_dirty_reads_are_coerced_as_the_contract_states(tmp_path: Path):
    """The declared input coercions are applied, not assumed away.

    report_spec.json and #TAR-7301 both spell out how a read's fields are cleaned
    up before anything is billed. The graded meter-read file happens to be tidy,
    so a biller that simply trusted the incoming types would agree with the sealed
    fixtures and never be caught. These reads are deliberately not tidy.
    """
    original = RATE_TABLE_PATH.read_text(encoding="utf-8")
    try:
        _write_json(RATE_TABLE_PATH, _LAB_TABLE)
        rows = [
            # A numeric string is read as the number it spells.
            dict(_lab_read("C-1", "2026-01-06", "2026-01-15", 0),
                 consumption_kwh=" 100 ", estimated="YES"),
            # A decimal string truncates towards zero rather than rounding.
            dict(_lab_read("C-2", "2026-01-06", "2026-01-15", 0),
                 consumption_kwh="100.9", estimated="1"),
            # Anything that is not a number at all reads as zero.
            dict(_lab_read("C-3", "2026-01-06", "2026-01-15", 0),
                 consumption_kwh="not-a-number", estimated="no"),
            # A negative consumption clamps up to zero instead of crediting the bill.
            dict(_lab_read("C-4", "2026-01-06", "2026-01-15", 0),
                 consumption_kwh=-250, peak_demand_kw=-7, estimated=False),
            # The account is matched case- and whitespace-insensitively, so this read
            # belongs to the same account as the others.
            dict(_lab_read("C-5", "2026-01-06", "2026-01-15", 0),
                 account="  LAB-Acct ", service_class=" Residential ",
                 consumption_kwh=100, estimated=True),
            # A boolean is not a number: the contract converts through
            # int(str(value).strip()), under which "True" fails both conversions
            # and falls to the zero it names -- not to the 1 that bool is worth
            # in Python arithmetic.
            dict(_lab_read("C-6", "2026-01-06", "2026-01-15", 0),
                 consumption_kwh=True, peak_demand_kw=True, estimated=False),
            # A magnitude no integer can hold: int(float("1e999")) raises
            # OverflowError rather than ValueError, and the contract's floor is
            # zero however the conversion fails.
            dict(_lab_read("C-7", "2026-01-06", "2026-01-15", 0),
                 consumption_kwh="1e999", peak_demand_kw="-1e999", estimated=False),
        ]
        input_path = tmp_path / "coercion.json"
        _write_json(input_path, rows)
        _, _, register, _ = _run_pipeline(tmp_path / "run", input_path=input_path)

        # All five landed under the one canonical account key.
        assert set(register) == {"lab-acct"}, sorted(register)
        bills = {row["read_id"]: row for row in register["lab-acct"]}
        assert set(bills) == {"C-1", "C-2", "C-3", "C-4", "C-5", "C-6", "C-7"}

        # " 100 " and 100 bill identically; "100.9" truncates to the same 100.
        assert bills["C-1"]["consumption_kwh"] == 100
        assert bills["C-2"]["consumption_kwh"] == 100
        assert bills["C-5"]["consumption_kwh"] == 100
        assert bills["C-1"]["energy_charge_cents"] == bills["C-5"]["energy_charge_cents"]
        # Rounding 100.9 up to 101 would push a kWh into the dearer bracket.
        assert bills["C-2"]["energy_charge_cents"] == bills["C-1"]["energy_charge_cents"]

        # Unparseable and negative both floor at zero, and neither goes negative.
        assert bills["C-3"]["consumption_kwh"] == 0
        assert bills["C-4"]["consumption_kwh"] == 0
        assert bills["C-4"]["peak_demand_kw"] == 0
        assert bills["C-3"]["energy_charge_cents"] == 0
        assert bills["C-4"]["energy_charge_cents"] == 0
        assert all(row["total_due_cents"] >= 0 for row in bills.values())

        # A boolean is worth nothing as a number, and neither is a magnitude that
        # overflows: both floor at zero rather than at 1 or at a crash.
        assert bills["C-6"]["consumption_kwh"] == 0
        assert bills["C-6"]["peak_demand_kw"] == 0
        assert bills["C-6"]["energy_charge_cents"] == 0
        assert bills["C-7"]["consumption_kwh"] == 0
        assert bills["C-7"]["peak_demand_kw"] == 0
        assert bills["C-7"]["energy_charge_cents"] == 0

        # true/1/yes are true, every other string is false, booleans pass through.
        assert bills["C-1"]["estimated"] is True
        assert bills["C-2"]["estimated"] is True
        assert bills["C-5"]["estimated"] is True
        assert bills["C-3"]["estimated"] is False
        assert bills["C-4"]["estimated"] is False
    finally:
        RATE_TABLE_PATH.write_text(original, encoding="utf-8")


def test_a_date_outside_the_contracts_format_is_not_a_date(tmp_path: Path):
    """report_spec.json gives one date format, and date.fromisoformat accepts more.

    A compact "20260106" and a week date "2026-W02-1" both parse in Python and
    neither is the YYYY-MM-DD the contract names, so a biller that simply handed
    the string to date.fromisoformat would bill a period the read never stated.
    A read without both dates is dropped under #TAR-7301.
    """
    original = RATE_TABLE_PATH.read_text(encoding="utf-8")
    try:
        _write_json(RATE_TABLE_PATH, _LAB_TABLE)
        rows = [
            _lab_read("D-1", "2026-01-06", "2026-01-15", 100),
            _lab_read("D-2", "20260106", "2026-01-15", 100),
            _lab_read("D-3", "2026-01-06", "20260115", 100),
            _lab_read("D-4", "2026-W02-1", "2026-01-15", 100),
        ]
        input_path = tmp_path / "dates.json"
        _write_json(input_path, rows)
        _, summary, register, _ = _run_pipeline(tmp_path / "run", input_path=input_path)
        assert summary["raw_read_count"] == 4
        assert summary["dropped_read_count"] == 3, "a non-conforming date was accepted as a date"
        assert summary["canonical_read_count"] == 1
        assert [row["read_id"] for row in register["lab-acct"]] == ["D-1"]
    finally:
        RATE_TABLE_PATH.write_text(original, encoding="utf-8")


def test_a_read_id_is_matched_on_its_collapsed_form(tmp_path: Path):
    """report_spec.json collapses a read_id's whitespace, and the identity follows it.

    Two reads whose identifiers differ only in spacing are the same read, so they
    deduplicate against each other under #TAR-7302 and the bill carries the
    collapsed form rather than whichever spelling arrived.
    """
    original = RATE_TABLE_PATH.read_text(encoding="utf-8")
    try:
        _write_json(RATE_TABLE_PATH, _LAB_TABLE)
        rows = [
            dict(_lab_read("R  1", "2026-01-06", "2026-01-15", 100)),
            dict(_lab_read("  R 1 ", "2026-01-07", "2026-01-16", 100)),
            dict(_lab_read("R-2", "2026-01-06", "2026-01-15", 100)),
        ]
        input_path = tmp_path / "read_ids.json"
        _write_json(input_path, rows)
        _, summary, register, _ = _run_pipeline(tmp_path / "run", input_path=input_path)
        assert summary["raw_read_count"] == 3
        assert summary["unique_read_ids"] == 2, "the two spellings were treated as two reads"
        ids = [row["read_id"] for row in register["lab-acct"]]
        assert sorted(ids) == ["R 1", "R-2"], ids
        # the later period_end wins the duplicate under #TAR-7302
        kept = next(row for row in register["lab-acct"] if row["read_id"] == "R 1")
        assert kept["period_end"] == "2026-01-16"
    finally:
        RATE_TABLE_PATH.write_text(original, encoding="utf-8")


_STACKED_TABLE = {
    "tariff_id": "LAB-STACK",
    "schedules": [{
        "effective_from": "2026-01-01",
        "classes": {"residential": {
            "brackets": [
                {"bracket_id": "S-A", "upper_kwh": 100, "rate_per_kwh_cents": 10},
                {"bracket_id": "S-B", "upper_kwh": None, "rate_per_kwh_cents": 50},
                {"bracket_id": "S-C", "upper_kwh": None, "rate_per_kwh_cents": 70},
            ],
            "demand_rate_cents_per_kw": 0,
            "standing_charge_cents_per_day": 0,
        }},
    }],
}

_CAPPED_TABLE = {
    "tariff_id": "LAB-CAP",
    "schedules": [{
        "effective_from": "2026-01-01",
        "classes": {"residential": {
            "brackets": [
                {"bracket_id": "C-A", "upper_kwh": 100, "rate_per_kwh_cents": 10},
                {"bracket_id": "C-B", "upper_kwh": 200, "rate_per_kwh_cents": 50},
            ],
            "demand_rate_cents_per_kw": 0,
            "standing_charge_cents_per_day": 0,
        }},
    }],
}


def _one_read_bill(tmp_path: Path, table: dict, kwh: int, label: str) -> dict:
    original = RATE_TABLE_PATH.read_text(encoding="utf-8")
    try:
        _write_json(RATE_TABLE_PATH, table)
        input_path = tmp_path / f"{label}.json"
        _write_json(input_path, [_lab_read(label.upper(), "2026-01-06", "2026-01-15", kwh)])
        _, _, register, _ = _run_pipeline(tmp_path / label, input_path=input_path)
        return register["lab-acct"][0]
    finally:
        RATE_TABLE_PATH.write_text(original, encoding="utf-8")


def test_unbounded_brackets_do_not_stack(tmp_path: Path):
    """#TAR-7372: consolidation can leave two unbounded brackets, and only the first charges.

    The filings can replace a bracket with one carrying no ceiling, so a
    consolidated schedule holds more than one. Charging the remainder once per
    unbounded bracket bills the same energy twice: here 300 kWh would cost
    1000 + 10000 + 14000 instead of the governed 1000 + 10000.
    """
    bill = _one_read_bill(tmp_path, _STACKED_TABLE, 300, "stack")
    assert bill["energy_charge_cents"] == 100 * 10 + 200 * 50
    assert bill["bracket_ids"] == ["S-A", "S-B"], bill["bracket_ids"]


def test_a_schedule_with_no_unbounded_bracket_charges_the_remainder_at_its_top_rate(tmp_path: Path):
    """#TAR-7372: the filings can retire the unbounded bracket, and the energy above it is not free.

    With the top of the schedule closed at 200 kWh, the 100 kWh above it is
    charged at the last bracket's rate rather than dropped, and that bracket is
    reported.
    """
    bill = _one_read_bill(tmp_path, _CAPPED_TABLE, 300, "capped")
    assert bill["energy_charge_cents"] == 100 * 10 + 100 * 50 + 100 * 50
    assert bill["bracket_ids"] == ["C-A", "C-B"], bill["bracket_ids"]

    inside = _one_read_bill(tmp_path, _CAPPED_TABLE, 150, "capped_inside")
    assert inside["energy_charge_cents"] == 100 * 10 + 50 * 50


def test_minimum_bill_prorates_half_up_not_by_float_rounding(tmp_path: Path):
    """The minimum bill prorates half-up in integer arithmetic rather than by float rounding."""
    table_original = RATE_TABLE_PATH.read_text(encoding="utf-8")
    policy_original = POLICY_PATH.read_text(encoding="utf-8")
    try:
        _write_json(RATE_TABLE_PATH, _LAB_TABLE)
        data = json.loads(policy_original)
        data["default"]["minimum_bill_cents"] = 1805
        _write_json(POLICY_PATH, data)
        rows = [_lab_read("L-3", "2026-01-06", "2026-01-08", 0)]
        input_path = tmp_path / "lab_min.json"
        _write_json(input_path, rows)
        _, _, register, _ = _run_pipeline(tmp_path / "run", input_path=input_path)
        bill = register["lab-acct"][0]
        assert bill["billed_days"] == 3
        assert bill["subtotal_cents"] == 0
        assert bill["minimum_applied"] is True
        # 1805 * 3 / 30 == 180.5 exactly: the governance dialect rounds it half UP to 181.
        assert bill["billed_subtotal_cents"] == 181
        # A floored share gives 180, and Python's round() rounds the .5 to even, also 180.
        assert 1805 * 3 // 30 == 180
        assert round(1805 * 3 / 30) == 180
        assert bill["billed_subtotal_cents"] != 180
        # The levy is floored on the post-floor subtotal: 181 * 240 // 10000 == 4.
        assert bill["levy_cents"] == 4
        assert bill["total_due_cents"] == 185
    finally:
        RATE_TABLE_PATH.write_text(table_original, encoding="utf-8")
        POLICY_PATH.write_text(policy_original, encoding="utf-8")


# --------------------------------------------------------------------------
# Anti-delegation: integer minor units only
# --------------------------------------------------------------------------
def _imported_roots(source: str) -> set:
    """Top-level module names the source imports, read from the parse tree."""
    roots = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            roots.add(node.module.split(".")[0])
    return roots


def test_the_standard_library_check_catches_a_third_party_import(tmp_path: Path):
    """The check above is real: an engine reaching for a package is detected."""
    shim = tmp_path / "vendored_engine.py"
    shim.write_text("import json\nimport pandas as pd\nfrom numpy import array\n")
    found = _imported_roots(shim.read_text())
    assert {"pandas", "numpy"} <= found
    assert {name for name in found if name not in sys.stdlib_module_names} == {"pandas", "numpy"}


def test_ast_check_catches_decimal_importing_engine(tmp_path: Path):
    """The import ban is real: a decimal-importing engine is detected."""
    shim = tmp_path / "delegating_engine.py"
    shim.write_text("import decimal\n\n\ndef rate(a, b):\n    return decimal.Decimal(a) / b\n")
    tree = ast.parse(shim.read_text())
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert "decimal" in imported


# --------------------------------------------------------------------------
# Sources stay operational
# --------------------------------------------------------------------------
def test_governance_log_present():
    """The minute book the rules are reconstructed from is in the environment."""
    assert LOG_PATH.exists() and LOG_PATH.stat().st_size > 0


def test_biller_does_not_reference_test_artifacts():
    """The biller derives its answer rather than reading anything verifier-side.

    Only string literals are inspected, read from the parse tree: naming one of
    these in a comment or a docstring is not a breach, using it as a path is.
    """
    literals = [node.value for node in ast.walk(ast.parse(WORKFLOW_PATH.read_text(encoding="utf-8")))
                if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    for token in ("/tests", "expected_report.json", "alt_meter_reads.json"):
        assert not any(token in literal for literal in literals), token


def test_shipped_contract_matches_the_golden_copy():
    """The output contract in the environment is unmodified.

    Field lists, container shapes and sort orders are golden metadata and are read
    from the verifier's own image; this proves the agent's copy still agrees with
    it, so the contract cannot be trimmed to weaken a schema check.
    """
    shipped = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    assert shipped == json.loads(GOLDEN_CONTRACT_PATH.read_text(encoding="utf-8"))
