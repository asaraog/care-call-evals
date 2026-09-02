# care-call-evals

**In July, a human reviewed 50 real test calls against a healthcare voice agent and logged
16 failures. This pipeline finds them automatically.**

A patient-care rubric, deterministic graders, and a scorecard per call — run against real
transcripts of phone calls my adversarial harness
([Voice Bot Bug Finder](https://saraogee.com/VoiceBotBugFinder)) placed against my own demo
clinic agent. Failures detected by systems, not discovered by people.

## Result

Validated against the July human review:

```
in-rubric bugs: 12   caught: 11   missed: 1   recall: 11/12
```

- The one miss is an NLU name-acceptance loop — judge-model territory, and the report says so
  rather than stretching a regex to fake it.
- 4 of the 16 human findings are out of rubric (UX completeness, medication accuracy) and are
  listed loudly, not silently excluded.
- The pipeline also surfaced **11 findings the human review never logged** — including the
  failed-transfer-to-test-line pattern in 5 additional calls where the human had only written
  it up twice. Systematic detection beats sampling.

## The rubric

`rubric.yaml` defines 11 patient-care dimensions — identity verification, PHI discipline,
insurance/eligibility before booking (the surprise-bill dimension), clinical red-flag
escalation, transfer follow-through, cancellation-policy disclosure, wrong-service
clarification, loop detection, language access — each with a severity weighted by downstream
cost to the patient, not by how broken the transcript looks. A deflection ("I don't have the
policy details") does not count as a disclosure. A caller's own question does not count as
the agent stating network status.

Tone/empathy is defined as a judge dimension and **ships disabled**: judge dimensions stay
off until validated against human labels.

## Run it

```bash
pip install -e .
care-call-evals data/transcripts --quiet --validate     # aggregate + recall table
care-call-evals data/transcripts --call 09              # one call's scorecard
```

## Data

34 real call transcripts (Azure STT output, with its real mess: unreliable diarization,
mid-call corrections, a Hindi-language call). Both sides of every call are mine — synthetic
caller personas against my own demo agent for a fictional clinic. **No PHI anywhere.** The
ground truth is the original July bug report, unedited.

## Honest limits

- Graders are content- and order-based because diarization on this corpus is unreliable;
  every scorecard says so when it applies.
- The rubric encodes one clinic's expectations; a real deployment derives it from each
  partner's SOP.
- EXTRA findings are labeled "new or false positive — review", because a pipeline that
  cannot say "review this" inflates its own precision.

BSD 3-Clause.
