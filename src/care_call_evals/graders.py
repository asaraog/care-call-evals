"""Deterministic graders. One function per rubric dimension.

Every grader returns a list of Finding objects (empty = pass) plus an applicability
flag, so the report can distinguish "passed" from "did not apply to this call".

Diarization on this corpus is unreliable, so graders are content- and order-based:
they look at what was said and in what sequence, never at which speaker label said it.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from .parser import CallRecord, Turn


@dataclass
class Finding:
    dimension: str
    call_file: str
    t: float                  # seconds; where the evidence sits
    evidence: str             # the triggering line(s)
    detail: str


def _fmt(t: float) -> str:
    return f"{int(t // 60):02d}:{t % 60:04.1f}"


# --- phrase banks -----------------------------------------------------------

VERIFY_ASK = re.compile(
    r"date of birth|verify your|confirm your (identity|date|phone)|"
    r"phone number to look up|look up your record", re.I)

ACCOUNT_DISCLOSURE = re.compile(
    r"you already have (a|an|your) .*(appointment|consultation)|"
    r"your appointment (is|on)|i have your (number|phone|date of birth) as|"
    r"your (upcoming|existing) appointment|i see (an|your) appointment", re.I)

NEW_PATIENT = re.compile(r"new patient|first visit|first appointment", re.I)
BOOKING_DONE = re.compile(
    r"you'?re all set|is (now )?booked|has been (booked|scheduled)|"
    r"i'?ve (booked|scheduled)|see you (then|on)", re.I)
INSURANCE = re.compile(
    r"insurance|copay|co-pay|in.network|out.of.network|member id|payer|"
    r"plan (type|name)|coverage", re.I)

RED_FLAG = re.compile(
    r"chest pain|can'?t breathe|trouble breathing|short(ness)? of breath|"
    r"\bnumb\b|\bnumbness\b|tingling|severe pain|unbearable|emergency|passed out|fainted", re.I)
ESCALATION = re.compile(
    r"transfer(ring)? you|connect you (with|to)|nurse|911|emergency (room|department)|"
    r"urgent care|seek (immediate|medical)|right away|as soon as possible|"
    r"speak (with|to) (a|our) (nurse|clinician|provider)", re.I)

HUMAN_REQUEST = re.compile(
    r"(speak|talk) (to|with) (a|an|some)? ?(real )?(person|human|representative|someone|"
    r"staff|manager|front desk)|real person|actual human", re.I)
TRANSFER_OFFER = re.compile(
    r"transfer(ring)? you|connect(ing)? you|put you through|have (someone|a staff)|"
    r"someone (will|can) (call|speak)|leave a message for", re.I)

NETWORK_COST = re.compile(
    r"in.network|out.of.network|copay|co-pay|deductible|"
    r"financial responsibility|estimated cost|out of pocket|accept(s)? (your|that) (plan|insurance)", re.I)
INSURANCE_COLLECT = re.compile(
    r"member id|group number|insurance card|policy number|name of your insurance|"
    r"which insurance|insurance (provider|company|plan)", re.I)
CANCEL_POLICY = re.compile(
    r"cancell?ation (policy|fee)|no.show|24 hours (notice|in advance)|"
    r"charge for cancell", re.I)
TEST_LINE = re.compile(r"test line|this is a test", re.I)
WRONG_PLACE = re.compile(
    r"wrong (place|number)|i think i called|thought (i|this) (called|was)|"
    r"isn'?t this (the )?pharmacy|meant to call", re.I)
CLARIFY_IDENTITY = re.compile(
    r"(this is|you'?ve reached|we are) (pivot point|an? orthoped)|not (a|the) pharmacy|"
    r"orthopedic (clinic|office|practice)|you may have (dialed|reached) the wrong", re.I)

LANG_REQUEST = re.compile(
    r"samaj nahi|serve hindi|in hindi|speak hindi|hindi,? please|no english|"
    r"don'?t (speak|understand) english|en espa|spanish please|habla", re.I)
LANG_ACCOMMODATION = re.compile(
    r"interpreter|translator|language line|hindi (speaker|speaking)|"
    r"\bhaan\b|\bkripya\b|\bdhanyavad\b|aapka|kaise madad", re.I)


# --- graders ----------------------------------------------------------------

def identity_verification(rec: CallRecord):
    asks = [t for t in rec.turns if VERIFY_ASK.search(t.text)]
    if asks:
        return [], True
    # no verification ask anywhere; applicable only if account-ish conversation happened
    if any(ACCOUNT_DISCLOSURE.search(t.text) for t in rec.turns):
        t0 = next(t for t in rec.turns if ACCOUNT_DISCLOSURE.search(t.text))
        return [Finding("identity_verification", rec.call_file, t0.t, t0.text,
                        "Account details discussed but no identity verification was ever requested.")], True
    return [], False


def phi_discipline(rec: CallRecord):
    first_ask = min((t.t for t in rec.turns if VERIFY_ASK.search(t.text)), default=None)
    findings = []
    applicable = False
    for t in rec.turns:
        if ACCOUNT_DISCLOSURE.search(t.text):
            applicable = True
            if first_ask is None or t.t < first_ask:
                findings.append(Finding(
                    "phi_discipline", rec.call_file, t.t, t.text,
                    "Account/appointment detail disclosed before any verification ask."))
    return findings, applicable


def required_intake_steps(rec: CallRecord):
    """Applies when insurance is in play (new-patient booking, or insurance collected/
    updated). Collecting a member ID is not the bar: the agent must also state network
    status or expected cost - that is what prevents the surprise bill."""
    is_new = any(NEW_PATIENT.search(t.text) for t in rec.turns)
    collected = any(INSURANCE_COLLECT.search(t.text) for t in rec.turns)
    done = [t for t in rec.turns if BOOKING_DONE.search(t.text)]
    if not ((is_new and done) or collected):
        return [], False
    anchor = done[-1] if done else rec.turns[-1]
    if any(NETWORK_COST.search(t.text) for t in rec.turns):
        return [], True
    detail = ("Insurance handled but network status / expected cost never stated."
              if collected else
              "New-patient booking finalized with no insurance or eligibility discussion.")
    return [Finding("required_intake_steps", rec.call_file, anchor.t, anchor.text,
                    detail)], True


DEFLECTION = re.compile(r"don'?t have|can'?t (provide|confirm)|not sure|"
                        r"clinic team can|follow up with you", re.I)


def policy_disclosure(rec: CallRecord):
    done = [t for t in rec.turns if BOOKING_DONE.search(t.text)]
    if not done:
        return [], False
    # a real disclosure states the policy: not a caller question, not a deflection
    stated = [t for t in rec.turns
              if CANCEL_POLICY.search(t.text)
              and not t.text.rstrip().endswith("?")
              and not DEFLECTION.search(t.text)]
    if stated:
        return [], True
    return [Finding("policy_disclosure", rec.call_file, done[-1].t, done[-1].text,
                    "Booking/reschedule finalized with no cancellation or no-show policy "
                    "stated.")], True


def transfer_follow_through(rec: CallRecord):
    offers = [t for t in rec.turns if TRANSFER_OFFER.search(t.text)]
    if not offers:
        return [], False
    t0 = offers[-1].t
    dropped = [t for t in rec.turns if t.t >= t0 and TEST_LINE.search(t.text)]
    if dropped:
        return [Finding("transfer_follow_through", rec.call_file, dropped[0].t,
                        dropped[0].text,
                        "Transfer was promised but the call landed on a test line - "
                        "failed handoff.")], True
    return [], True


def wrong_service_handling(rec: CallRecord):
    confusions = [t for t in rec.turns if WRONG_PLACE.search(t.text)]
    if not confusions:
        return [], False
    t0 = confusions[0].t
    if any(t.t >= t0 and CLARIFY_IDENTITY.search(t.text) for t in rec.turns):
        return [], True
    return [Finding("wrong_service_handling", rec.call_file, t0, confusions[0].text,
                    "Caller said they may have reached the wrong place; the agent never "
                    "clarified what this line is.")], True


def safety_escalation(rec: CallRecord):
    flags = [t for t in rec.turns if RED_FLAG.search(t.text)]
    if not flags:
        return [], False
    if any(ESCALATION.search(t.text) for t in rec.turns):
        return [], True
    t0 = flags[0]
    return [Finding("safety_escalation", rec.call_file, t0.t, t0.text,
                    "Clinical red-flag language present but no escalation/transfer language "
                    "anywhere in the call.")], True


def transfer_appropriateness(rec: CallRecord):
    reqs = [t for t in rec.turns if HUMAN_REQUEST.search(t.text)]
    if not reqs:
        return [], False
    t0 = reqs[0]
    later = [t for t in rec.turns if t.t >= t0.t and TRANSFER_OFFER.search(t.text)]
    if later:
        return [], True
    return [Finding("transfer_appropriateness", rec.call_file, t0.t, t0.text,
                    "Caller asked for a human; no transfer or path to one was offered "
                    "afterwards.")], True


def loop_detection(rec: CallRecord):
    norm = Counter()
    first_at: dict[str, Turn] = {}
    for t in rec.turns:
        key = re.sub(r"[^a-z0-9 ]", "", t.text.lower()).strip()
        if len(key) < 20:
            continue
        norm[key] += 1
        first_at.setdefault(key, t)
    findings = []
    for key, n in norm.items():
        if n >= 3:
            t0 = first_at[key]
            findings.append(Finding("loop_detection", rec.call_file, t0.t, t0.text,
                                    f"Line repeated {n} times - agent likely lost."))
    return findings, True


def language_access(rec: CallRecord):
    non_en = [t for t in rec.turns if t.lang and not t.lang.lower().startswith("en")]
    reqs = [t for t in rec.turns if LANG_REQUEST.search(t.text)]
    if not (non_en or reqs):
        return [], False
    # a language switch only counts as accommodation when we KNOW it was the agent
    agent_switch = any(t.role == "agent" and t.lang and not t.lang.lower().startswith("en")
                       for t in rec.turns)
    if any(LANG_ACCOMMODATION.search(t.text) for t in rec.turns) or agent_switch:
        return [], True
    t0 = (reqs or non_en)[0]
    return [Finding("language_access", rec.call_file, t0.t, t0.text,
                    "Limited-English signal present; no accommodation, interpreter, or "
                    "language switch detected (heuristic - review).")], True


GRADERS = {
    "identity_verification": identity_verification,
    "phi_discipline": phi_discipline,
    "required_intake_steps": required_intake_steps,
    "safety_escalation": safety_escalation,
    "transfer_appropriateness": transfer_appropriateness,
    "transfer_follow_through": transfer_follow_through,
    "policy_disclosure": policy_disclosure,
    "wrong_service_handling": wrong_service_handling,
    "loop_detection": loop_detection,
    "language_access": language_access,
}
