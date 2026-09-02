# Evaluating Healthcare Voice Agents with a Patient-Care Rubric

This project automatically evaluates voice-agent phone calls against the dimensions that
matter for patient care. In July, 50 test calls were placed against a demo clinic agent
using an adversarial harness ([Voice Bot Bug Finder](https://saraogee.com/VoiceBotBugFinder))
and reviewed by hand, producing [16 written findings](data/july_manual_review.md). Here, a
[rubric](rubric.yaml) of ten deterministic patient-care dimensions and a
[single script](evals.py) score every call instead, each dimension weighted by downstream
cost to the patient: a skipped insurance check reads as a pleasant call and becomes a
surprise bill three weeks later. The transcripts are real Azure Speech-to-Text output
(synthetic personas against my own demo agent, so no PHI) with the real mess of production
STT (diarization collapses to one speaker, words are misheard). Across 34 calls the script
produced 26 findings, rediscovering 10 of the 12 hand-logged issues the rubric covers and
surfacing patterns, such as omitting the cancellation policy, that the manual review had
logged only two or three times.

## Files

*evals.py:* \
Parses transcripts and checks each call against every rubric dimension.

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
