# Voice Agent Bug Report
Generated: 2026-07-01 20:37 UTC  |  16 issues

## Summary
| Severity | Count |
|----------|-------|
| Critical | 4 |
| High | 8 |
| Medium | 4 |
| Low | 0 |
| **Total** | **16** |

### Language Handling Issues
2 issue(s) in Hindi scenario (10)

> Note: Under Title VI, federally-funded medical practices must provide language access to limited-English-proficient patients.

---

## Issues Grouped By Call Number

### Call 01

#### Bug #01 -- High: Did not collect insurance details or state in-network status and copay when booking new patient appointment

- **Category:** Missing Information / Insurance & Billing
- **Call:** call_01_CA673004_transcript.txt at 02:06.0-02:22.6

**Agent said:** Please bring your photo ID, insurance card, a list of your current medications, and any imaging discs you have. ... You're all set for your appointment.

**Expected:** For a new-patient appointment the agent should collect the caller's insurance details (payer name, plan type, member ID) and clearly state whether the clinic accepts that plan (in-network vs out-of-network) and any expected patient financial responsibility (copay/co-insurance/estimated cost) before finalizing the booking.

**Impact:** Without confirmation of insurance network status and expected costs, the patient may arrive expecting coverage that the clinic does not accept, leading to surprise bills, denied claims, appointment cancellations, or the clinic booking under incorrect financial assumptions.

---

#### Bug #02 -- High: Did not provide cancellation or rescheduling policy when booking appointment

- **Category:** Missing Information / Policy
- **Call:** call_01_CA673004_transcript.txt at 01:57.3

**Agent said:** Your first appointment is booked for Thursday, July 9th at 2:15 p.m. with Dr. Dudie Hauser at Pivot Point Orthopedics.

**Expected:** When booking an appointment, the agent should state the clinic's cancellation/rescheduling policy (required notice window and any fees) or proactively offer it, so the patient understands obligations and avoids penalties.

**Impact:** High — Patients who are not informed of cancellation/rescheduling rules may incur unexpected fees or miss required notice windows, causing patient dissatisfaction and potential revenue recovery issues for the clinic.

---

#### Bug #03 -- Medium: Provided only general instructions; no specific parking/entrance guidance for new patient visit

- **Category:** UX/Flow
- **Call:** call_01_CA673004_transcript.txt at 02:06

**Agent said:** Please bring your photo ID, insurance card, a list of your current medications, and any imaging discs you have.

**Expected:** For a new patient visit the agent should offer specific arrival logistics such as parking location/garage or lot, best entrance to use, check-in desk location, and any validation or visitor procedures that would meaningfully help the patient arrive on time and prepared.

**Impact:** Lack of parking/entrance specifics can cause confusion or delays on the day of the appointment, increasing no-shows or late arrivals and creating a poor patient experience.

---

### Call 02

#### Bug #04 -- High: Agent failed to provide cancellation/rescheduling policy when caller rescheduled

- **Category:** Missing Information / Policy
- **Call:** call_02_CA92bc7a_transcript.txt at 01:33.3

**Agent said:** I don't have the specific cancellation policy details, but the clinic team can provide that if you need.

**Expected:** When a caller is rescheduling or cancelling an appointment, the agent should state the clinic's cancellation/rescheduling policy (required notice window and any fees) or immediately provide a clear mechanism for obtaining that information (e.g., transfer to billing or read the policy). If the agent cannot retrieve it, they should offer to connect the caller to someone who can during the same call.

**Impact:** Without the cancellation/rescheduling policy (notice window and fees), the patient may unknowingly incur a cancellation fee or miss required notice windows, leading to unexpected charges or failed rescheduling.

---

### Call 03

#### Bug #05 -- Critical: Agent collapsed two distinct medications into a single incorrect summary

- **Category:** Handling Error / Medication Safety
- **Call:** call_03_CAdd3a09_transcript.txt at 03:24.5

**Agent said:** I've documented your refill request for lisinopril 10-miligrams and 20-miligrams.

**Expected:** The agent should accurately document and read back each medication requested by the caller separately and with correct names and strengths (e.g., 'lisinopril 10 mg' and 'atorvastatin 20 mg'). If additional information is needed for each medication (days remaining, symptoms, pharmacy), the agent should collect that for each drug before finishing.

**Impact:** High patient safety risk and potential medication dispensing errors: collapsing or mislabeling medications can lead to the wrong drug or wrong strength being prescribed or sent to the pharmacy, causing treatment failures or adverse drug events. This also fails to satisfy medication reconciliation and could require additional clinician/clinic follow-up, delaying needed refills.

---

### Call 04

#### Bug #06 -- High: Agent added insurance without stating in‑network status or financial expectations

- **Category:** Insurance & Billing
- **Call:** call_04_CA55a536_transcript.txt at 04:11.4-04:16.3

**Agent said:** Your Blue Shield of California PPO insurance has been added as your primary coverage.

**Expected:** When confirming that an insurance plan has been added, the agent should state whether the practice is in‑network or out‑of‑network for that specific plan and provide expected financial information (e.g., estimated co‑pay, co‑insurance, or that the office will notify the patient if any out‑of‑pocket costs apply). If the agent cannot determine network status at call time, it should explicitly say so and explain next steps and possible financial implications.

**Impact:** High risk of scheduling or billing under the wrong coverage leading to unexpected patient bills, denied claims, or administrative rework if the plan is out‑of‑network or requires prior authorization. The patient was left without clear information about their financial responsibility.

---

#### Bug #07 -- High: Promised transfer to patient support failed / call dropped to test line

- **Category:** Handling Error
- **Call:** call_04_CA601fff_transcript.txt at 02:08.3

**Agent said:** I'll connect you to our patient support team for help. Please stay on the line. Connecting you to a representative. Please wait.

**Expected:** After stating it would connect the caller to patient support, the agent should complete the transfer to a live representative or an appropriate support queue. If the transfer cannot be completed, the agent should inform the caller, offer alternatives (callback, hold and retry, or provide another contact method), and not drop the caller to an unrelated test line.

**Impact:** Caller was left disconnected / routed to an unrelated test line instead of being connected to patient support, preventing resolution of their verification/booking issue and forcing them to call again — wasted time, frustration, potential lost appointments or unmet care needs.

---

#### Bug #08 -- Medium: Agent repeated the same question asking if caller was calling for themselves

- **Category:** UX/Flow
- **Call:** call_04_CA601fff_transcript.txt at 00:13.8

**Agent said:** Are you calling for yourself or on behalf of someone else? / Are you calling for yourself or for someone else today?

**Expected:** The agent should avoid unnecessary repetition of the same question once the caller's intent is clear, or should clarify why the question is being repeated (e.g., confirming different context).

**Impact:** Repetition can confuse or annoy callers and lengthen call time, degrading user experience.

---

### Call 05

#### Bug #09 -- High: Agent collected insurance reference but did not state network/coverage or financial expectations

- **Category:** Insurance & billing / Missing Information
- **Call:** call_05_CAca31b7_transcript.txt at 02:08.5

**Agent said:** Please bring your photo ID, insurance card, a list of your current medications, and any imaging discs you have.

**Expected:** When collecting or referencing the patient's insurance, the agent should state whether the practice accepts the caller's plan (in-network vs out-of-network) and any expected patient financial responsibility (copay, coinsurance, or fee) for the scheduled visit, or offer to check coverage before finalizing the appointment.

**Impact:** High — Without clear network status or financial expectations, the patient may schedule an appointment assuming coverage that doesn't exist, leading to unexpected bills, denied claims, or appointment cancellations by the clinic.

---

#### Bug #10 -- High: Agent scheduled appointment but did not provide cancellation/rescheduling policy or notice window

- **Category:** Cancellation / reschedule policy
- **Call:** call_05_CAca31b7_transcript.txt at 02:01.3

**Agent said:** Your appointment is set for Monday, July 6th at 11 a.m. with Dr. Dougie Hauser at Pivot Point Orthopedics.

**Expected:** When booking an appointment, the agent should inform the caller of the clinic's cancellation/rescheduling policy (required notice window, any fees for late cancellation/no-show) or confirm where that policy can be found, so the patient understands obligations and avoids penalties.

**Impact:** High — Lack of a stated cancellation/rescheduling policy can lead to missed expectations, patient surprise fees for late cancellations or no-shows, and operational inefficiencies for the clinic.

---

#### Bug #11 -- Medium: Confusing/self-contradictory response about Sunday availability

- **Category:** UX/Flow
- **Call:** call_05_CAca31b7_transcript.txt at 00:38.3-01:47.0

**Agent said:** I'm looking to schedule an appointment for this Sunday at 10 a.m. ... We did help with that. ... There are no openings this Sunday, but we do have several options on Monday, July 6th. Pivot Point Orthopedics is not open on Sundays.

**Expected:** The agent should respond consistently and clearly when the caller requests a time on a day the clinic is closed. It should not give an initial reply that implies the request was already fulfilled (e.g., 'We did help with that') and then contradict that by saying the clinic is closed on Sundays. Instead, the agent should immediately clarify availability (e.g., 'We are closed on Sundays; the earliest available is Monday...').

**Impact:** Medium — Contradictory responses can confuse patients about whether an appointment was actually booked, reduce trust in the agent, and may cause callers to hang up or call back to confirm, increasing call volume and patient frustration.

---

### Call 06

#### Bug #12 -- High: Agent attempted transfer but call dropped to an unrelated test line

- **Category:** Handling Error (Failed transfer / handoff)
- **Call:** call_06_CA8aef09_transcript.txt at 01:46-02:12

**Agent said:** I can't proceed further right now, but I can make sure our clinic support team follows up with you. Would you like me to connect you to our patient support team?... Connecting you to a representative. Please wait. ... You've reached a pretty good AI test line. Goodbye.

**Expected:** When the agent says it will connect the caller to patient support, the system should either (a) successfully complete the transfer to a live representative, or (b) if transfer fails, immediately notify the caller of the failure, offer to place a callback/leave them in queue, provide an estimated wait time, or offer an alternative contact method. The agent should not drop the caller to a generic test line or disconnect without resolution.

**Impact:** Caller was disconnected from the promised support transfer and left without assistance; request was not completed and caller had to ask to be reconnected. This can result in frustrated patients, unresolved medical scheduling needs, and extra repeat calls to the clinic.

---

### Call 08

#### Bug #13 -- Medium: Vague parking information — no specific parking/entrance/validation details provided

- **Category:** UX/Flow
- **Call:** call_08_CA2706af_transcript.txt at 01:06.2

**Agent said:** Free patient parking is available.

**Expected:** When asked about parking, the agent should provide actionable, specific details such as which lot or garage to use, the nearest entrance, whether there is patient-only parking or validation, locations for accessible parking, and any time limits or costs if applicable.

**Impact:** Patients may arrive unsure where to park or which entrance to use, potentially causing confusion, delays, missed appointments, or difficulty for those needing accessible parking or validation information.

---

### Call 09

#### Bug #14 -- Critical: Agent ignored caller's report that they reached a pharmacy and proceeded to process a prescription refill as if caller reached clinic

- **Category:** Handling Error / Routing
- **Call:** call_09_CA209eb5_transcript.txt at 00:15.4

**Agent said:** I've documented your request for a prescription update and sent it to our clinic support team.

**Expected:** When the caller indicates they believe they reached a different business (e.g., 'I think I called CVS Pharmacy'), the agent should acknowledge and clarify the mismatch (e.g., 'This is Pivot Point Orthopedics, not CVS Pharmacy') and then either: a) refuse to process/route the request meant for the pharmacy and advise the caller how to reach the correct pharmacy, or b) explicitly confirm the caller wants Pivot Point to assist with a prescription refill for their provider (and obtain any required authorizations), ensuring the caller understands who will be contacted. The agent must not continue collecting and forwarding the prescription request without clarifying the apparent wrong-number/practice situation.

**Impact:** High risk of misrouting requests, privacy violations, and wasted work: the clinic may act on a refill request intended for a pharmacy, the caller may not get directed to the correct pharmacy to obtain medication, and protected health information could be handled by the wrong organization. This also fails to correct caller confusion and may lead to missed medication access or duplicated effort.

---

### Call 10

#### Bug #15 -- Critical: Agent repeatedly failed to accept/verify the caller's provided full name and DOB, then aborted without proper escalation [HINDI]

- **Category:** Identity / NLU
- **Call:** call_10_CAb59418_transcript.txt at 02:32.2

**Agent said:** Something's not right. I'm unable to verify your information at the moment, so I can't proceed with booking your appointment. Would you like me to have our clinic support team follow up with you?

**Expected:** When a caller provides full name and date of birth (caller provided 'मरिया गार्सिया' and DOB), the agent should successfully verify or, if verification fails, explicitly state why (e.g., mismatch, unclear audio) and offer an immediate remediation such as repeating back the info, offering an interpreter, transferring to live support, or creating a callback/secure message. The agent should not repeatedly prompt for the same info in English without addressing the language barrier or providing a clear escalation path.

**Impact:** Critical impact: The caller provided name and DOB multiple times but the agent failed to register/accept them and ultimately aborted the booking flow. This prevented appointment scheduling and frustrated the caller; combined with lack of interpreter offer, the user was left without resolution or a clear path to get help.

---

#### Bug #16 -- Critical: Agent failed to recognize Hindi and did not offer an interpreter / language line (Title VI access failure) [HINDI]

- **Category:** Language Handling
- **Call:** call_10_CAb59418_transcript.txt at 00:10.4-02:44.9

**Agent said:** Am I speaking with Maria? ... Can you please provide your date of birth? ... I'll need your date of birth to look up your information. ... Could you please provide that? ... I'll need your full name along with your date of birth to find your information. ... Could you please tell me your first and last name? ... Are you looking to book, reschedule, or cancel an appointment? ... Please provide your date of birth. ... I'll need both your first and last name, along with your date of birth, to look up your information. ... Could you please provide your full name? ... I still need your full name, first and last, to look up your information. ... Could you please provide your full name? ... Something's not right. I'm unable to verify your information at the moment, so I can't proceed with booking your appointment. Would you like me to have our clinic support team follow up with you? Are you still there?

**Expected:** When the caller speaks Hindi, the agent should detect the language barrier and either (a) switch to Hindi for the remainder of the interaction, or (b) immediately offer and connect the caller to an appropriate interpreter/language line before continuing. The agent should not proceed only in English when the caller is speaking another language it cannot understand.

**Impact:** High risk of access denial under Title VI: the caller (Hindi speaker) could not complete the appointment booking because the agent never accommodated the language need or offered interpreter assistance. This prevents the patient from receiving timely care, may force repeated calls, and could disproportionately impact non-English-speaking patients.

---
