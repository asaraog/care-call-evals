"""Scorecards and the aggregate table. Every number prints its denominator."""
from __future__ import annotations

from pathlib import Path

import yaml

from .graders import GRADERS, _fmt
from .parser import CallRecord, parse_dir


def load_rubric(path: Path) -> list[dict]:
    return yaml.safe_load(path.read_text())["dimensions"]


def evaluate(rec: CallRecord, rubric: list[dict]):
    """-> (results, findings): results maps dim id -> 'pass'|'FAIL'|'n/a'|'skipped'."""
    results, findings = {}, []
    for dim in rubric:
        if not dim.get("enabled", True) or dim["grader"] != "deterministic":
            results[dim["id"]] = "skipped"
            continue
        f, applicable = GRADERS[dim["id"]](rec)
        results[dim["id"]] = "FAIL" if f else ("pass" if applicable else "n/a")
        findings.extend(f)
    return results, findings


def scorecard(rec: CallRecord, results, findings) -> str:
    lines = [f"── {rec.call_file}  (scenario {rec.scenario})"]
    if rec.diarization_unreliable:
        lines.append("   note: diarization unreliable - graders ran content-order based")
    for dim, verdict in results.items():
        lines.append(f"   {dim:<26} {verdict}")
    for f in findings:
        lines.append(f'   ! [{_fmt(f.t)}] {f.dimension}: {f.detail}')
        lines.append(f'       "{f.evidence[:110]}"')
    return "\n".join(lines)


def aggregate(records, all_results, all_findings, rubric) -> str:
    n = len(records)
    lines = [
        "=" * 74,
        "CARE CALL EVALS - aggregate",
        f"Calls evaluated: {n}   "
        f"(diarization unreliable on {sum(r.diarization_unreliable for r in records)})",
        "=" * 74,
        f"{'dimension':<26}{'applicable':>11}{'failed':>8}{'severity':>9}",
        "-" * 54,
    ]
    sev = {d["id"]: d["severity"] for d in rubric}
    for dim in [d["id"] for d in rubric if d.get("enabled") and d["grader"] == "deterministic"]:
        app = sum(1 for res in all_results if res[dim] in ("pass", "FAIL"))
        fail = sum(1 for res in all_results if res[dim] == "FAIL")
        lines.append(f"{dim:<26}{app:>11}{fail:>8}{sev[dim]:>9}")
    skipped = [d["id"] for d in rubric if d["grader"] == "judge"]
    if skipped:
        lines.append(f"\njudge dimensions skipped (unvalidated, off by default): {', '.join(skipped)}")
    lines.append(f"\ntotal findings: {sum(len(f) for f in all_findings)} across {n} calls")
    return "\n".join(lines)
