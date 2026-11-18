"""Blocks diagnosis, medicine, dosage, and treatment questions before any model call."""

from __future__ import annotations

import re
from dataclasses import dataclass

DISCLAIMER = (
    "NutriRAG shares general nutrition education only. "
    "It is not medical advice and does not replace a doctor or a dietitian."
)

REFUSAL = (
    "I can't help with diagnosis, medicines, dosages, or treatment. "
    "Please consult a qualified doctor or a registered dietitian."
)

_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bdiagnos",
        r"\bdo i have\b",
        r"\bwhat disease\b",
        r"\bam i sick\b",
        r"\bwhat is wrong with me\b",
        r"\bsymptom",
        r"\bmedicin",
        r"\bmedication\b",
        r"\btablet\b",
        r"\bpill\b",
        r"\bdrug\b",
        r"\bprescri",
        r"\bantibiotic",
        r"\bmetformin\b",
        r"\binsulin\b",
        r"\bdosage\b",
        r"\bdose of\b",
        r"\bhow many mg\b",
        r"\bmilligram",
        r"\btreatment\b",
        r"\btreat my\b",
        r"\bcure my\b",
        r"\bhow to cure\b",
        r"\btherapy\b",
    )
)


@dataclass(frozen=True)
class SafetyDecision:
    refused: bool
    message: str


def assess_question(question: str) -> SafetyDecision:
    """Refuse diagnosis and medicine requests before any model call."""
    text = (question or "").strip()
    if text and any(pattern.search(text) for pattern in _PATTERNS):
        return SafetyDecision(True, REFUSAL)
    return SafetyDecision(False, "")
