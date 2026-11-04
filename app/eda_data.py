"""PhiUSIIL summary for the data page. Built by scripts/build_phiusiil_summary.py."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

SUMMARY_PATH = Path(__file__).resolve().parent.parent / "data" / "phiusiil_summary.json"
PUBLIC_PATH = Path(__file__).resolve().parent.parent / "data" / "public_sets.json"


@lru_cache(maxsize=1)
def summarize() -> dict[str, object]:
    if not SUMMARY_PATH.exists():
        return {
            "available": False,
            "source_name": "PhiUSIIL Phishing URL Dataset",
            "source_url": "https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset",
            "citation": "Prasad, A. and Chandra, S. PhiUSIIL Phishing URL Dataset. UCI Machine Learning Repository, 2024.",
            "license": "CC BY 4.0",
            "n": 0,
            "phishing_n": 0,
            "legitimate_n": 0,
            "skipped": 0,
            "signal": {},
            "numeric": [],
            "binary": [],
            "indicators": [],
            "gaps": [],
            "samples": [],
            "glossary": [],
            "length_sentence": "",
            "note": "The summary file has not been built yet.",
        }
    data = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    data["available"] = True
    return data


@lru_cache(maxsize=1)
def public_sets() -> dict[str, object]:
    if not PUBLIC_PATH.exists():
        return {"available": False, "built": "", "sets": []}
    data = json.loads(PUBLIC_PATH.read_text(encoding="utf-8"))
    data["available"] = True
    return data
