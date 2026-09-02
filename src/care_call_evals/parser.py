"""Parse Voice Bot Bug Finder transcript files.

Format (Azure STT export):
    TRANSCRIPT - scenario 07  |  call_07_CAxxxx.mp3
    Engine: Azure AI Speech (en-US)
    ============
    [WARN] Diarization returned a single speaker label; ...
    [MM:SS.m] Speaker 0: text
    [MM:SS.m] Speaker 0 [hi-IN]: text

Diarization is frequently unreliable (single speaker label), so downstream graders are
written to be order- and content-based, not speaker-attribution-based. The unreliability
is surfaced on every scorecard rather than silently ignored.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

TURN_RE = re.compile(
    r"^\[(?P<mm>\d+):(?P<ss>\d+(?:\.\d+)?)\]\s+Speaker\s+(?P<spk>\d+)"
    r"(?:\s+\[(?P<lang>[a-zA-Z-]+)\])?:\s*(?P<text>.*)$"
)


@dataclass
class Turn:
    t: float          # seconds from call start
    speaker: int
    lang: str | None
    text: str


@dataclass
class CallRecord:
    path: str
    call_file: str            # e.g. call_07_CAxxxx_transcript.txt
    scenario: str             # e.g. "07"
    engine: str
    warnings: list[str] = field(default_factory=list)
    turns: list[Turn] = field(default_factory=list)

    @property
    def diarization_unreliable(self) -> bool:
        return any("diarization" in w.lower() for w in self.warnings)

    @property
    def full_text(self) -> str:
        return "\n".join(t.text for t in self.turns)


def parse_file(path: Path) -> CallRecord:
    scenario = "??"
    m = re.search(r"call_(\d+)_", path.name)
    if m:
        scenario = m.group(1)
    rec = CallRecord(path=str(path), call_file=path.name, scenario=scenario, engine="")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.rstrip()
        if line.startswith("Engine:"):
            rec.engine = line.split(":", 1)[1].strip()
            continue
        if line.startswith("[WARN]"):
            rec.warnings.append(line[len("[WARN]"):].strip())
            continue
        m = TURN_RE.match(line)
        if m:
            t = int(m.group("mm")) * 60 + float(m.group("ss"))
            rec.turns.append(
                Turn(t=t, speaker=int(m.group("spk")), lang=m.group("lang"), text=m.group("text"))
            )
    return rec


def parse_dir(d: Path) -> list[CallRecord]:
    files = sorted(d.glob("*_transcript.txt"))
    return [parse_file(f) for f in files]
