from pathlib import Path

from care_call_evals.parser import parse_dir
from care_call_evals.report import evaluate, load_rubric
from care_call_evals.validate import parse_ground_truth, map_dimension

ROOT = Path(__file__).resolve().parents[1]


def test_parses_all_transcripts():
    records = parse_dir(ROOT / "data/transcripts")
    assert len(records) == 34
    assert all(r.turns for r in records)


def test_ground_truth_has_16_bugs():
    bugs = parse_ground_truth(ROOT / "data/ground_truth.md")
    assert len(bugs) == 16
    assert all(b["call"] != "??" for b in bugs)


def test_number_is_not_a_red_flag():
    # 'phone number' must never trigger the numbness red flag (the classic substring bug)
    from care_call_evals.graders import RED_FLAG
    assert not RED_FLAG.search("I have your phone number as 555-123-4567")
    assert RED_FLAG.search("my hand has gone numb")


def test_hindi_call_fails_language_access():
    records = {r.scenario: r for r in parse_dir(ROOT / "data/transcripts")}
    rubric = load_rubric(ROOT / "rubric.yaml")
    rec = [r for r in parse_dir(ROOT / "data/transcripts") if r.scenario == "10"][0]
    results, findings = evaluate(rec, rubric)
    assert results["language_access"] == "FAIL"


def test_medication_bugs_are_out_of_rubric():
    assert map_dimension("Handling Error / Medication Safety", "anything") is None
