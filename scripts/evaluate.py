"""Measure the rule detector and the three investigation modes.

No model is trained. The rules are fixed in app/detector.py; this script only
counts how they behave on public data.

Splits
  PhiUSIIL (UCI 967) is split by an MD5 hash of the URL: hash % 10 < 3 is the
  development split (rules were inspected and tuned on it only), the rest is
  the held-out test split. The split does not depend on row order.
  OpenPhish and Phishing.Database lists hold phishing URLs only, so they give
  recall on phishing that PhiUSIIL never saw.

Usage
  python scripts/evaluate.py                      # writes data/eval_results.json
  python scripts/evaluate.py --out other.json --tag v1
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import statistics
import sys
import time
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import agents  # noqa: E402
from app.detector import analyze, catalog  # noqa: E402

RAW = ROOT / "data" / "raw"
PHIUSIIL = RAW / "phiusiil.zip"
OPENPHISH = RAW / "openphish.txt"
PHISHDB = RAW / "phishing-links-active.txt"
URLHAUS = RAW / "urlhaus_filter_online.txt"
TRANCO = RAW / "tranco_top1m.csv"
TRANCO_TOP = 100000
EXTERNAL_SAMPLE = 20000
DEFAULT_OUT = ROOT / "data" / "eval_results.json"
DEV_BUCKETS = 3
CHAIN_SAMPLE = 1000
SEED = 967


def split_of(url: str) -> str:
    bucket = int(hashlib.md5(url.encode("utf-8")).hexdigest(), 16) % 10
    return "dev" if bucket < DEV_BUCKETS else "test"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--tag", default="current")
    parser.add_argument("--skip-chain", action="store_true")
    parser.add_argument("--sensitive", action="store_true", help="count any single rule as an alert (the v2-style gate)")
    args = parser.parse_args()
    if args.sensitive:
        from app import detector

        detector.MEDIUM_RULES = {rule["id"] for rule in catalog()}

    if not PHIUSIIL.exists():
        raise SystemExit(f"Missing {PHIUSIIL}. Download the UCI PhiUSIIL zip first (see README).")

    rows = {"dev": [], "test": []}
    rule_hits = {"dev": {"phishing": Counter(), "legitimate": Counter()}, "test": {"phishing": Counter(), "legitimate": Counter()}}
    skipped = 0
    started = time.perf_counter()
    for url, label in _phiusiil():
        try:
            detection = analyze(url)
        except ValueError:
            skipped += 1
            continue
        split = split_of(url)
        rows[split].append((label, detection["verdict"]["code"], int(detection["raw_score"]), url))
        for indicator in detection["indicators"]:
            rule_hits[split][label][indicator["id"]] += 1
    detect_seconds = time.perf_counter() - started
    scored = len(rows["dev"]) + len(rows["test"])

    result: dict[str, object] = {
        "tag": args.tag,
        "rules": len(catalog()),
        "phiusiil": {
            "skipped": skipped,
            "ms_per_url": round(detect_seconds / max(1, scored) * 1000, 4),
            "dev": _report(rows["dev"]),
            "test": _report(rows["test"]),
            "rule_rates_test": _rule_rates(rule_hits["test"], rows["test"]),
        },
        "external": {
            "openphish": _recall_only(_lines(OPENPHISH), None),
            "phishing_database": _recall_only(_test_only(_lines(PHISHDB)), EXTERNAL_SAMPLE),
            "urlhaus": _recall_only(_test_only(_urlhaus()), EXTERNAL_SAMPLE),
            "tranco": _safe_only(_test_only(_tranco())),
        },
    }
    result["realworld"] = _realworld(result["external"])
    if not args.skip_chain:
        result["chain"] = _chain(rows["test"])

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    _print(result)
    print(f"wrote {args.out}")


def _phiusiil():
    with zipfile.ZipFile(PHIUSIIL) as archive:
        name = next(item for item in archive.namelist() if item.lower().endswith(".csv"))
        with archive.open(name) as handle:
            reader = csv.DictReader(line.decode("utf-8", errors="replace") for line in handle)
            fields = {key.strip("﻿").lower(): key for key in (reader.fieldnames or [])}
            for row in reader:
                label = str(row[fields["label"]]).strip()
                if label not in {"0", "1"}:
                    continue
                yield (row[fields["url"]] or "").strip(), ("phishing" if label == "0" else "legitimate")


def _lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", errors="replace") as handle:
        return [line.strip() for line in handle if line.strip() and not line.startswith("#")]


def _test_only(items: list[str]) -> list[str]:
    """External lists use the same hash split, so rules can be inspected on their dev part."""
    return [item for item in items if split_of(item) == "test"]


def _urlhaus() -> list[str]:
    """malware-filter's URLhaus list is in adblock syntax: ||host/path^$all, or a bare host or IP."""
    out = []
    for line in _lines(URLHAUS):
        if line.startswith("!"):
            continue
        item = line.removeprefix("||")
        item = item.split("^", 1)[0].split("$", 1)[0].strip()
        if item:
            out.append(item)
    return out


def _tranco() -> list[str]:
    if not TRANCO.exists():
        return []
    with TRANCO.open(encoding="utf-8") as handle:
        domains = [line.strip().split(",")[1] for line in handle if "," in line]
    return domains[:TRANCO_TOP]


def _safe_only(domains: list[str]) -> dict[str, object]:
    """Popular registrable domains (Tranco), read as https homepages. Every flag is a false alarm."""
    if not domains:
        return {"available": False}
    codes = Counter()
    for domain in domains:
        try:
            codes[analyze(f"https://{domain}/")["verdict"]["code"]] += 1
        except ValueError:
            codes["rejected"] += 1
    total = sum(codes.values())
    return {
        "available": True,
        "n": total,
        "verdicts": dict(codes),
        "strict_fpr": round(codes["phishing"] / total, 5),
        "alert_fpr": round((codes["phishing"] + codes["suspicious"]) / total, 5),
    }


def _realworld(ext: dict[str, dict]) -> dict[str, object]:
    """Pool the three malicious feeds against popular safe domains (test splits only)."""
    blocks = [ext[key] for key in ("openphish", "phishing_database", "urlhaus") if ext[key].get("available")]
    safe = ext["tranco"]
    if not blocks or not safe.get("available"):
        return {"available": False}
    out = {"available": True, "malicious_n": sum(b["n"] for b in blocks), "safe_n": safe["n"]}
    for point, codes in (("strict", ("phishing",)), ("alert", ("phishing", "suspicious"))):
        tp = sum(sum(b["verdicts"].get(c, 0) for c in codes) for b in blocks)
        fn = out["malicious_n"] - tp
        fp = sum(safe["verdicts"].get(c, 0) for c in codes)
        tn = safe["n"] - fp
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        out[point] = {
            "tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "accuracy": round((tp + tn) / (tp + tn + fp + fn), 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(2 * precision * recall / (precision + recall) if precision + recall else 0.0, 4),
            "fpr": round(fp / (fp + tn), 5),
        }
    return out


def _report(rows: list[tuple[str, str, int, str]]) -> dict[str, object]:
    positives = sum(1 for label, *_ in rows if label == "phishing")
    return {
        "n": len(rows),
        "phishing_n": positives,
        "legitimate_n": len(rows) - positives,
        "verdicts": {
            f"{label}->{code}": count
            for (label, code), count in sorted(Counter((label, code) for label, code, *_ in rows).items())
        },
        "strict": _binary(rows, {"phishing"}),
        "alert": _binary(rows, {"phishing", "suspicious"}),
        "roc_auc": round(_roc_auc(rows), 4),
        "pr_auc": round(_pr_auc(rows), 4),
    }


def _binary(rows, positive_codes: set[str]) -> dict[str, float]:
    tp = fp = tn = fn = 0
    for label, code, *_ in rows:
        flagged = code in positive_codes
        if label == "phishing":
            tp += flagged
            fn += not flagged
        else:
            fp += flagged
            tn += not flagged
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "accuracy": round((tp + tn) / max(1, tp + tn + fp + fn), 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "fpr": round(fp / (fp + tn) if fp + tn else 0.0, 5),
    }


def _roc_auc(rows) -> float:
    """Mann-Whitney form with average ranks for tied scores."""
    pairs = sorted((score, label == "phishing") for label, _code, score, _url in rows)
    positives = sum(1 for _, is_pos in pairs if is_pos)
    negatives = len(pairs) - positives
    if not positives or not negatives:
        return 0.0
    rank_sum = 0.0
    index = 0
    while index < len(pairs):
        end = index
        while end < len(pairs) and pairs[end][0] == pairs[index][0]:
            end += 1
        average_rank = (index + 1 + end) / 2
        rank_sum += average_rank * sum(1 for k in range(index, end) if pairs[k][1])
        index = end
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def _pr_auc(rows) -> float:
    """Average precision, stepping through distinct score thresholds from high to low."""
    by_score: dict[int, list[int]] = {}
    for label, _code, score, _url in rows:
        bucket = by_score.setdefault(score, [0, 0])
        bucket[0 if label == "phishing" else 1] += 1
    positives = sum(bucket[0] for bucket in by_score.values())
    if not positives:
        return 0.0
    tp = fp = 0
    area = 0.0
    previous_recall = 0.0
    for score in sorted(by_score, reverse=True):
        tp += by_score[score][0]
        fp += by_score[score][1]
        recall = tp / positives
        area += (recall - previous_recall) * (tp / (tp + fp))
        previous_recall = recall
    return area


def _rule_rates(hits, rows) -> list[dict[str, object]]:
    counts = Counter(label for label, *_ in rows)
    out = []
    for rule in catalog():
        phish = hits["phishing"][rule["id"]] / max(1, counts["phishing"]) * 100
        legit = hits["legitimate"][rule["id"]] / max(1, counts["legitimate"]) * 100
        out.append({"id": rule["id"], "label": rule["label"], "phishing_pct": round(phish, 2), "legitimate_pct": round(legit, 2)})
    return sorted(out, key=lambda item: item["phishing_pct"] - item["legitimate_pct"], reverse=True)


def _recall_only(urls: list[str], sample: int | None) -> dict[str, object]:
    if not urls:
        return {"available": False}
    if sample and len(urls) > sample:
        urls = random.Random(SEED).sample(urls, sample)
    codes = Counter()
    for url in urls:
        try:
            codes[analyze(url)["verdict"]["code"]] += 1
        except ValueError:
            codes["rejected"] += 1
    total = sum(codes.values())
    return {
        "available": True,
        "n": total,
        "verdicts": dict(codes),
        "strict_recall": round(codes["phishing"] / total, 4),
        "alert_recall": round((codes["phishing"] + codes["suspicious"]) / total, 4),
    }


def _chain(test_rows) -> dict[str, object]:
    """Run all three modes on a seeded, class-balanced test sample."""
    rng = random.Random(SEED)
    phish = [url for label, _c, _s, url in test_rows if label == "phishing"]
    legit = [url for label, _c, _s, url in test_rows if label == "legitimate"]
    half = CHAIN_SAMPLE // 2
    sample = rng.sample(phish, min(half, len(phish))) + rng.sample(legit, min(half, len(legit)))
    keys = ("unsupported_rate", "evidence_support", "completeness", "retrieval_ms", "agent_ms", "published_claims", "withheld_claims", "exhibit_count")
    store = {mode: {key: [] for key in keys} for mode in ("rules", "retrieval", "agentic")}
    for url in sample:
        modes = agents.investigate(url, "compare")["modes"]
        for mode, report in modes.items():
            for key in keys:
                value = report["metrics"][key]
                if value is not None:
                    store[mode][key].append(float(value))
    summary = {}
    for mode, values in store.items():
        summary[mode] = {
            key: round(statistics.fmean(series), 4) if series else None for key, series in values.items()
        }
        summary[mode]["p95_agent_ms"] = round(sorted(values["agent_ms"])[int(0.95 * (len(values["agent_ms"]) - 1))], 4)
    return {"n": len(sample), "modes": summary}


def _print(result) -> None:
    phi = result["phiusiil"]
    print(f"[{result['tag']}] rules={result['rules']}  {phi['ms_per_url']} ms/url  skipped={phi['skipped']}")
    for split in ("dev", "test"):
        block = phi[split]
        for name in ("strict", "alert"):
            m = block[name]
            print(
                f"  {split:4} {name:6} acc={m['accuracy']:.4f} P={m['precision']:.4f} R={m['recall']:.4f} "
                f"F1={m['f1']:.4f} FPR={m['fpr']:.5f}"
            )
        print(f"  {split:4} ROC-AUC={block['roc_auc']}  PR-AUC={block['pr_auc']}")
    for name, block in result["external"].items():
        if block.get("available") and "strict_recall" in block:
            print(f"  {name}: n={block['n']} strict_recall={block['strict_recall']} alert_recall={block['alert_recall']}")
        elif block.get("available"):
            print(f"  {name}: n={block['n']} strict_fpr={block['strict_fpr']} alert_fpr={block['alert_fpr']}")
    rw = result.get("realworld", {})
    if rw.get("available"):
        for point in ("strict", "alert"):
            m = rw[point]
            print(f"  realworld {point:6} acc={m['accuracy']} P={m['precision']} R={m['recall']} F1={m['f1']} FPR={m['fpr']}")
    if "chain" in result:
        for mode, values in result["chain"]["modes"].items():
            print(
                f"  chain {mode:9} unsupported={values['unsupported_rate']} support={values['evidence_support']} "
                f"complete={values['completeness']} ms={values['agent_ms']}"
            )


if __name__ == "__main__":
    main()
