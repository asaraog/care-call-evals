# care-call-evals

Score healthcare voice-agent calls against a patient-care rubric, automatically.

In July I reviewed 50 test calls against my own demo clinic agent by hand and wrote up
[16 issues](data/july_manual_review.md). This is the automated version: a
[rubric](rubric.yaml) of patient-care dimensions and one script that checks every call
against it.

```bash
pip install pyyaml
python evals.py data/transcripts
```

```
34 calls · 10 dimensions · 26 findings

  required_intake_steps       6 of  6 applicable calls failed
  policy_disclosure           8 of  8 applicable calls failed
  transfer_follow_through     7 of 11 applicable calls failed
  language_access             2 of  2 applicable calls failed
  ...
```

The interesting part is [rubric.yaml](rubric.yaml): each dimension says what it checks,
why it matters for patient care, and a severity weighted by the downstream cost to the
patient — a skipped insurance check reads as a perfectly pleasant call and turns into a
surprise bill three weeks later. My manual review logged that pattern a couple of times;
the script shows it in every call it applies to.

## Honest limits

- **The data is rough.** These are real Azure STT transcripts of real phone calls (my test
  harness phoning my own demo agent — no PHI, both sides are mine), and STT output is messy:
  diarization usually collapses to one speaker, words get misheard ("pretty good AI" came
  out "printed AI"). Graders are regex-over-text, so treat findings as flags to review, not
  verdicts.
- The rubric encodes one imaginary clinic's expectations. A real deployment derives it from
  each partner's actual protocols.
- Fuzzy dimensions (tone, empathy) need a judge model validated against human labels; the
  rubric lists one, disabled.

BSD 3-Clause.
