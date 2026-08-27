"""Minimal reusable TNOA decision interface."""

from .core import Decision, DecisionRecord, Evidence, Reason, classify, classify_rows, summarize

__all__ = [
    "Decision",
    "DecisionRecord",
    "Evidence",
    "Reason",
    "classify",
    "classify_rows",
    "summarize",
]

__version__ = "0.1.0"
