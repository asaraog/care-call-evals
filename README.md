# Evaluating Healthcare Voice Agents with a Patient-Care Rubric

## Project Summary

This project aims to automatically evaluate voice-agent phone calls against the dimensions
that matter for patient care. In July, 50 test calls were placed against a demo clinic
agent using an adversarial harness ([Voice Bot Bug Finder](https://saraogee.com/VoiceBotBugFinder))
and reviewed by hand, producing [16 written findings](data/july_manual_review.md). Here,
that manual review is replaced by a [rubric](rubric.yaml) of ten deterministic patient-care
dimensions (identity verification, insurance and eligibility before booking, clinical
red-flag escalation, transfer follow-through, cancellation-policy disclosure, language
access) and a [single script](evals.py) that scores every call. Each dimension carries a
severity weighted by the downstream cost to the patient: a skipped insurance check reads as
a perfectly pleasant call and becomes a surprise bill three weeks later. The manual review
logged that class of failure a few times; the script shows it in every applicable call,
which is the difference between sampling and systematic detection.

The transcripts are real Azure Speech-to-Text output of real phone calls (both sides of
each call are mine — synthetic caller personas against my own demo agent, so no PHI) and
carry the real mess of production STT: diarization usually collapses to a single speaker
and words are misheard ("pretty good AI" transcribed as "printed AI"), so graders are
content- and order-based rather than speaker-based, and findings are flags to review
rather than verdicts. Fuzzy dimensions like tone and empathy are defined in the rubric as
judge-model dimensions and ship disabled, since a judge is only trustworthy after
validation against human labels.

## Results

34 calls · 10 dimensions · 26 findings <br>

policy_disclosure: 8 of 8 applicable calls failed <br>
transfer_follow_through: 7 of 11 applicable calls failed <br>
required_intake_steps: 6 of 6 applicable calls failed <br>
language_access: 2 of 2 applicable calls failed <br>
wrong_service_handling: 2 of 2 applicable calls failed <br>
loop_detection: 1 of 34 applicable calls failed <br>
**Every finalized booking omitted the cancellation policy, and every promised transfer that failed landed on the same test line — patterns the manual review had logged only two or three times.**

## Files

*evals.py:* \
Parses transcripts and checks each call against every rubric dimension. One file, no
framework; prints a per-dimension table and a severity-sorted findings list.

*rubric.yaml:* \
The patient-care dimensions: what each checks, why it matters, grader type, severity.

*data/transcripts:* \
34 real STT transcripts across 10 scenarios, including a Hindi-language call.

*data/july_manual_review.md:* \
The original hand-written bug report the script is compared against.

## Installation and Running

Download or git clone this project onto local machine into folder on local machine.

```
git clone https://github.com/asaraog/care-call-evals.git
cd care-call-evals
pip install pyyaml
python evals.py data/transcripts
```
