"""Compare pipeline findings against the July human bug report (ground truth).

The report is honest in both directions: recall on the human findings, and the
pipeline findings the human never wrote down. Bugs whose category maps to no rubric
dimension are listed as out-of-rubric rather than silently excluded.
"""
from __future__ import annotations

import re
from pathlib import Path

BUG_RE = re.compile(r"^#### Bug #(\d+) -- (\w+): (.+)$")

# ground-truth category text -> rubric dimension (None = rubric does not cover it)
CATEGORY_MAP = [
    (re.compile(r"medication", re.I), None),          # needs a judge; out of rubric
    (re.compile(r"cancellation|policy", re.I), "policy_disclosure"),
    (re.compile(r"transfer.*(fail|dropp)|failed transfer|handoff", re.I), "transfer_follow_through"),
    (re.compile(r"routing", re.I), "wrong_service_handling"),
    (re.compile(r"identity|nlu", re.I), "identity_verification"),
    (re.compile(r"insurance|billing", re.I), "required_intake_steps"),
    (re.compile(r"language", re.I), "language_access"),
    (re.compile(r"safety|clinical|escalat", re.I), "safety_escalation"),
    (re.compile(r"verif|privacy|identity|hipaa|phi", re.I), "phi_discipline"),
    (re.compile(r"loop|repeat|stuck", re.I), "loop_detection"),
    (re.compile(r"transfer|human|handoff", re.I), "transfer_appropriateness"),
]


def parse_ground_truth(path: Path):
    bugs, cur = [], None
    for line in path.read_text().splitlines():
        m = BUG_RE.match(line.strip())
        if m:
            cur = {"num": int(m.group(1)), "severity": m.group(2),
                   "title": m.group(3), "category": "", "call": "??"}
            bugs.append(cur)
            continue
        if cur is None:
            continue
        if line.strip().startswith("- **Category:**"):
            cur["category"] = line.split("**Category:**")[1].strip()
        m2 = re.search(r"call_(\d+)_", line)
        if m2 and cur["call"] == "??":
            cur["call"] = m2.group(1)
    return bugs


def map_dimension(category: str, title: str):
    for rx, dim in CATEGORY_MAP:
        if rx.search(category) or rx.search(title):
            return dim
    return None  # unmapped -> out of rubric, listed loudly


def validate(bugs, records, all_findings):
    flagged = set()   # (scenario, dimension)
    for rec, findings in zip(records, all_findings):
        for f in findings:
            flagged.add((rec.scenario, f.dimension))

    caught, missed, out_of_rubric = [], [], []
    for b in bugs:
        dim = map_dimension(b["category"], b["title"])
        if dim is None:
            out_of_rubric.append(b)
        elif (b["call"], dim) in flagged:
            caught.append((b, dim))
        else:
            missed.append((b, dim))

    matched_pairs = {(b["call"], d) for b, d in caught}
    extra = sorted({(s, d) for (s, d) in flagged if (s, d) not in matched_pairs})

    in_scope = len(caught) + len(missed)
    lines = ["=" * 74, "VALIDATION vs July human review (16 findings)", "=" * 74]
    lines.append(f"in-rubric bugs: {in_scope}   caught: {len(caught)}   missed: {len(missed)}"
                 f"   recall: {len(caught)}/{in_scope}")
    lines.append(f"out-of-rubric bugs (rubric has no dimension for these): {len(out_of_rubric)}")
    for b, d in caught:
        lines.append(f"  CAUGHT  #{b['num']:02d} [{b['severity']}] call {b['call']} -> {d}: {b['title'][:70]}")
    for b, d in missed:
        lines.append(f"  MISSED  #{b['num']:02d} [{b['severity']}] call {b['call']} -> {d}: {b['title'][:70]}")
    for b in out_of_rubric:
        lines.append(f"  OUT     #{b['num']:02d} [{b['severity']}] call {b['call']} ({b['category'][:40]}): {b['title'][:60]}")
    if extra:
        lines.append("pipeline findings with no matching human bug (new or false positive - review):")
        for s, d in extra:
            lines.append(f"  EXTRA   scenario {s} -> {d}")
    return "\n".join(lines)
