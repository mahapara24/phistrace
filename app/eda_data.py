"""PhiUSIIL summary for the data page. Built by scripts/build_phiusiil_summary.py."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

SUMMARY_PATH = Path(__file__).resolve().parent.parent / "data" / "phiusiil_summary.json"
PUBLIC_PATH = Path(__file__).resolve().parent.parent / "data" / "public_sets.json"
EVAL_PATH = Path(__file__).resolve().parent.parent / "data" / "eval_results.json"
BASELINE_PATH = Path(__file__).resolve().parent.parent / "data" / "eval_baseline.json"
V2_PATH = Path(__file__).resolve().parent.parent / "data" / "eval_v2.json"
V3_PATH = Path(__file__).resolve().parent.parent / "data" / "eval_v3.json"


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


@lru_cache(maxsize=1)
def evaluation() -> dict[str, object]:
    """Measured results written by scripts/evaluate.py (current rules and the earlier v1, v2, v3 rule sets)."""
    out: dict[str, object] = {"available": EVAL_PATH.exists()}
    if EVAL_PATH.exists():
        out["current"] = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    if BASELINE_PATH.exists():
        out["baseline"] = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    if V2_PATH.exists():
        out["v2"] = json.loads(V2_PATH.read_text(encoding="utf-8"))
    if V3_PATH.exists():
        out["v3"] = json.loads(V3_PATH.read_text(encoding="utf-8"))
    return out
