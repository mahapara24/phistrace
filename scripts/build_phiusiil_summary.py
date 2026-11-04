"""Score every PhiUSIIL URL with the existing rules and write the data-page summary.

The raw file is the public UCI copy (CC BY 4.0). This script does not train a model.
"""

from __future__ import annotations

import csv
import json
import random
import sys
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.detector import analyze, catalog  # noqa: E402

ZIP_PATH = ROOT / "data" / "raw" / "phiusiil.zip"
OUT_PATH = ROOT / "data" / "phiusiil_summary.json"
SAMPLE_PER_CLASS = 8
SEED = 967

NUMERIC = [
    ("url_length", "URL length"),
    ("num_dots", "Dots in the host"),
    ("num_hyphens", "Hyphens in the host"),
    ("num_digits", "Digits in the host"),
    ("num_subdomains", "Subdomain labels"),
    ("lure_count", "Lure words"),
]
BINARY = [
    ("has_https", "HTTPS"),
    ("has_ip", "Raw IP host"),
    ("has_at", "@ in the authority"),
    ("suspicious_tld", "Higher-abuse suffix"),
    ("brand_mismatch", "Brand mismatch"),
    ("punycode", "Punycode"),
    ("shortener", "Shortener"),
]
GLOSSARY = [
    {"term": "URL length", "meaning": "Characters in the URL string from PhiUSIIL."},
    {"term": "Dots", "meaning": "Dot characters in the host."},
    {"term": "Hyphens", "meaning": "Hyphen characters in the host."},
    {"term": "Digits", "meaning": "Digit characters in the host."},
    {"term": "Subdomains", "meaning": "Labels to the left of the registrable domain."},
    {"term": "HTTPS", "meaning": "The URL uses the https scheme."},
    {"term": "Raw IP", "meaning": "The host is an IP address."},
    {"term": "@ sign", "meaning": "User information is present before @."},
    {"term": "Listed suffix", "meaning": "The public suffix is on this workbench's higher-abuse list."},
    {"term": "Lure words", "meaning": "Credential and account words in the host, path, or query."},
    {"term": "Brand mismatch", "meaning": "A brand-like token sits on a domain that is not in the local brand list."},
    {"term": "Punycode", "meaning": "A host label uses xn--."},
    {"term": "Shortener", "meaning": "The host is a shortening service in the local list."},
    {"term": "High signal", "meaning": "Rule score of 50 or more. This is the workbench threshold for the deep path."},
]


def main() -> None:
    if not ZIP_PATH.exists():
        raise SystemExit(f"Missing {ZIP_PATH}. Download the UCI PhiUSIIL zip first.")
    rules = [row["id"] for row in catalog()]
    labels = {row["id"]: row["label"] for row in catalog()}
    stats = {
        "phishing": _blank(rules),
        "legitimate": _blank(rules),
    }
    samples: dict[str, list[dict[str, object]]] = {"phishing": [], "legitimate": []}
    seen = {"phishing": 0, "legitimate": 0}
    skipped = 0
    rng = random.Random(SEED)

    with zipfile.ZipFile(ZIP_PATH) as archive:
        name = next(item for item in archive.namelist() if item.lower().endswith(".csv"))
        with archive.open(name) as handle:
            text = (line.decode("utf-8", errors="replace") for line in handle)
            reader = csv.DictReader(text)
            fields = {key.lower(): key for key in (reader.fieldnames or [])}
            url_key = fields.get("url")
            label_key = fields.get("label")
            if not url_key or not label_key:
                raise SystemExit(f"Unexpected columns: {reader.fieldnames}")
            for index, row in enumerate(reader, start=1):
                label = _class_name(row[label_key])
                if label is None:
                    skipped += 1
                    continue
                url = (row[url_key] or "").strip()
                try:
                    detection = analyze(url)
                except ValueError:
                    skipped += 1
                    continue
                _add(stats[label], detection, rules)
                seen[label] += 1
                _maybe_sample(samples[label], detection, label, seen[label], rng)
                if index % 25000 == 0:
                    print(f"read {index}", flush=True)

    summary = _finish(stats, samples, skipped)
    OUT_PATH.write_text(json.dumps(summary), encoding="utf-8")
    print(
        f"wrote {OUT_PATH} phishing={summary['phishing_n']} legitimate={summary['legitimate_n']} skipped={skipped}"
    )
    print(
        "high-signal phishing",
        summary["signal"]["phishing_high"],
        "legitimate",
        summary["signal"]["legitimate_high"],
    )


def _blank(rules: list[str]) -> dict[str, object]:
    return {
        "n": 0,
        "score_sum": 0,
        "high": 0,
        "moderate_plus": 0,
        "bands": Counter(),
        "indicators": Counter({rule: 0 for rule in rules}),
        "numeric": Counter({key: 0.0 for key, _label in NUMERIC}),
        "binary": Counter({key: 0 for key, _label in BINARY}),
    }


def _class_name(value: str) -> str | None:
    text = str(value).strip().lower()
    if text in {"0", "phishing"}:
        return "phishing"
    if text in {"1", "legitimate"}:
        return "legitimate"
    return None


def _add(bucket: dict[str, object], detection: dict[str, object], rules: list[str]) -> None:
    bucket["n"] = int(bucket["n"]) + 1
    score = int(detection["score"])
    bucket["score_sum"] = int(bucket["score_sum"]) + score
    if score >= 50:
        bucket["high"] = int(bucket["high"]) + 1
    if score >= 21:
        bucket["moderate_plus"] = int(bucket["moderate_plus"]) + 1
    bucket["bands"][detection["level"]] += 1
    fired = {item["id"] for item in detection["indicators"]}
    for rule in rules:
        if rule in fired:
            bucket["indicators"][rule] += 1
    features = detection["features"]
    for key, _label in NUMERIC:
        bucket["numeric"][key] += float(features[key])
    for key, _label in BINARY:
        bucket["binary"][key] += int(features[key])


def _maybe_sample(pool: list[dict[str, object]], detection: dict[str, object], label: str, seen: int, rng: random.Random) -> None:
    url = str(detection["url"])
    if len(url) > 2048:
        return
    item = {
        "label": label,
        "url": url,
        "score": int(detection["score"]),
        "level": str(detection["level_label"]),
        "reasons": ", ".join(str(indicator["label"]) for indicator in detection["indicators"]) or "No weighted indicator",
    }
    if len(pool) < SAMPLE_PER_CLASS:
        pool.append(item)
        return
    slot = rng.randrange(seen)
    if slot < SAMPLE_PER_CLASS:
        pool[slot] = item


def _finish(stats, samples, skipped: int) -> dict[str, object]:
    phishing = stats["phishing"]
    legitimate = stats["legitimate"]
    numeric = []
    for key, label in NUMERIC:
        phish = _safe_mean(phishing["numeric"][key], phishing["n"])
        legit = _safe_mean(legitimate["numeric"][key], legitimate["n"])
        scale = max(phish, legit, 0.1)
        numeric.append(
            {
                "label": label,
                "phish": round(phish, 1),
                "legit": round(legit, 1),
                "phish_width": round(phish / scale * 100, 1),
                "legit_width": round(legit / scale * 100, 1),
            }
        )
    binary = []
    for key, label in BINARY:
        phish = round(_safe_mean(phishing["binary"][key], phishing["n"]) * 100)
        legit = round(_safe_mean(legitimate["binary"][key], legitimate["n"]) * 100)
        binary.append({"label": label, "phish": phish, "legit": legit, "gap": abs(phish - legit)})
    indicators = []
    labels = {row["id"]: row["label"] for row in catalog()}
    for rule, label in labels.items():
        phish = round(_safe_mean(phishing["indicators"][rule], phishing["n"]) * 100)
        legit = round(_safe_mean(legitimate["indicators"][rule], legitimate["n"]) * 100)
        indicators.append({"label": label, "phish": phish, "legit": legit, "gap": abs(phish - legit)})
    length = next(item for item in numeric if item["label"] == "URL length")
    phish_n = int(phishing["n"])
    legit_n = int(legitimate["n"])
    return {
        "source_name": "PhiUSIIL Phishing URL Dataset",
        "source_url": "https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset",
        "citation": "Prasad, A. and Chandra, S. PhiUSIIL Phishing URL Dataset. UCI Machine Learning Repository, 2024. https://doi.org/10.1016/j.cose.2023.103545",
        "license": "CC BY 4.0",
        "note": "Label 0 is phishing and label 1 is legitimate in the source file. Counts below are rows this workbench could read as an http or https URL.",
        "n": phish_n + legit_n,
        "phishing_n": phish_n,
        "legitimate_n": legit_n,
        "skipped": skipped,
        "signal": {
            "phishing_high": _pct(phishing["high"], phish_n),
            "legitimate_high": _pct(legitimate["high"], legit_n),
            "phishing_moderate": _pct(phishing["moderate_plus"], phish_n),
            "legitimate_moderate": _pct(legitimate["moderate_plus"], legit_n),
            "phishing_mean": round(_safe_mean(phishing["score_sum"], phish_n), 1),
            "legitimate_mean": round(_safe_mean(legitimate["score_sum"], legit_n), 1),
        },
        "bands": {
            "phishing": {name: int(phishing["bands"][name]) for name in ("low", "moderate", "high", "critical")},
            "legitimate": {name: int(legitimate["bands"][name]) for name in ("low", "moderate", "high", "critical")},
        },
        "numeric": numeric,
        "binary": binary,
        "indicators": sorted(indicators, key=lambda item: item["gap"], reverse=True),
        "gaps": sorted(binary, key=lambda item: item["gap"], reverse=True)[:4],
        "samples": samples["phishing"] + samples["legitimate"],
        "glossary": GLOSSARY,
        "length_sentence": (
            f"Mean URL length is {length['phish']} characters on the phishing URLs "
            f"and {length['legit']} characters on the legitimate URLs."
        ),
    }


def _safe_mean(total: float, count: int) -> float:
    if not count:
        return 0.0
    return float(total) / count


def _pct(count: int, total: int) -> float:
    if not total:
        return 0.0
    return round(100 * count / total, 1)


if __name__ == "__main__":
    main()
