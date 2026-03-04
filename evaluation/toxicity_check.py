"""Heuristic toxicity and policy-risk checks for model outputs."""

from __future__ import annotations

from typing import Iterable

RISKY_KEYWORDS = {
    "hack",
    "malware",
    "phishing",
    "bypass",
    "exploit",
    "fraud",
    "steal",
    "weapon",
    "attack",
    "ransomware",
}


def contains_risky_content(text: str, keywords: Iterable[str] = RISKY_KEYWORDS) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords)
