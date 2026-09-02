import argparse
import sys
from pathlib import Path

from .parser import parse_dir
from .report import aggregate, evaluate, load_rubric, scorecard
from .validate import parse_ground_truth, validate


def main():
    ap = argparse.ArgumentParser(prog="care-call-evals")
    ap.add_argument("transcripts", type=Path)
    ap.add_argument("--rubric", type=Path, default=Path("rubric.yaml"))
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--ground-truth", type=Path, default=Path("data/ground_truth.md"))
    ap.add_argument("--call", help="only this scenario number, e.g. 01")
    ap.add_argument("--quiet", action="store_true", help="aggregate only")
    a = ap.parse_args()

    rubric = load_rubric(a.rubric)
    records = parse_dir(a.transcripts)
    if a.call:
        records = [r for r in records if r.scenario == a.call]
    if not records:
        sys.exit("no transcripts found")

    all_results, all_findings = [], []
    for rec in records:
        res, f = evaluate(rec, rubric)
        all_results.append(res)
        all_findings.append(f)
        if not a.quiet:
            print(scorecard(rec, res, f), "\n")

    print(aggregate(records, all_results, all_findings, rubric))
    if a.validate:
        bugs = parse_ground_truth(a.ground_truth)
        print()
        print(validate(bugs, records, all_findings))


if __name__ == "__main__":
    main()
