"""Score public URL lists with the existing rules and write a short summary.

Raw files stay in data/raw/, which is gitignored. This script does not train a
model and does not open any URL.
"""

from __future__ import annotations

import json
import random
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.detector import analyze  # noqa: E402

RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "public_sets.json"
SAMPLE_N = 6
SEED = 2026


def main() -> None:
    sets = [
        _score_lines(
            _lines(RAW / "openphish.txt"),
            meta={
                "id": "openphish",
                "name": "OpenPhish community feed",
                "source_url": "https://openphish.com/",
                "mirror_url": "https://github.com/openphish/public_feed",
                "citation": "OpenPhish community phishing feed. Non-commercial use. https://openphish.com/terms.html",
                "note": "Every row is a phishing URL. This is a snapshot saved with the summary, not a live request during a check.",
                "host_only": False,
            },
        ),
        _score_lines(
            _lines(RAW / "phishing-links-active.txt"),
            meta={
                "id": "phishing-links",
                "name": "Phishing Database, active links",
                "source_url": "https://github.com/mitchellkrogza/Phishing.Database",
                "mirror_url": "https://github.com/mitchellkrogza/Phishing.Database",
                "citation": "Mitchell Krog. Phishing Database, active phishing links. https://github.com/mitchellkrogza/Phishing.Database",
                "note": "Every row is an active phishing link. Addresses that are not http or https, including ftp, are skipped.",
                "host_only": False,
            },
        ),
        _score_lines(
            (f"http://{host}/" for host in _lines(RAW / "phishing-ips-active.txt")),
            meta={
                "id": "phishing-ips",
                "name": "Phishing Database, active IP hosts",
                "source_url": "https://github.com/mitchellkrogza/Phishing.Database",
                "mirror_url": "https://github.com/mitchellkrogza/Phishing.Database",
                "citation": "Mitchell Krog. Phishing Database, active phishing IP addresses. https://github.com/mitchellkrogza/Phishing.Database",
                "note": "The file lists hosts. Each host is read here as an http URL so the same rules can score it. The page is not opened.",
                "host_only": True,
            },
        ),
    ]
    payload = {"built": date.today().isoformat(), "sets": sets}
    OUT.write_text(json.dumps(payload), encoding="utf-8")
    for item in sets:
        print(
            f"{item['id']}: scored {item['n']} skipped {item['skipped']} "
            f"mean {item['signal']['mean']} high {item['signal']['high']}%"
        )


def _lines(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            text = line.strip()
            if text and not text.startswith("#"):
                yield text


def _score_lines(urls, meta: dict[str, object]) -> dict[str, object]:
    rng = random.Random(SEED)
    n = 0
    skipped = 0
    score_sum = 0
    high = 0
    moderate = 0
    verdicts: Counter[str] = Counter()
    pool: list[dict[str, object]] = []
    seen_readable = 0
    for index, url in enumerate(urls, start=1):
        try:
            detection = analyze(url)
        except ValueError:
            skipped += 1
            continue
        n += 1
        score = int(detection["score"])
        score_sum += score
        if score >= 50:
            high += 1
        if score >= 21:
            moderate += 1
        verdicts[str(detection["verdict"]["code"])] += 1
        shown = str(detection["url"])
        if len(shown) <= 160:
            seen_readable += 1
            item = {
                "label": "phishing",
                "url": shown,
                "score": score,
                "level": str(detection["level_label"]),
                "verdict": str(detection["verdict"]["label"]),
                "reasons": ", ".join(str(indicator["label"]) for indicator in detection["indicators"]) or "No weighted indicator",
            }
            if len(pool) < SAMPLE_N:
                pool.append(item)
            else:
                slot = rng.randrange(seen_readable)
                if slot < SAMPLE_N:
                    pool[slot] = item
        if index % 100000 == 0:
            print(f"{meta['id']} read {index}", flush=True)
    return {
        **meta,
        "n": n,
        "skipped": skipped,
        "phishing_n": n,
        "legitimate_n": 0,
        "signal": {
            "mean": round(score_sum / n, 1) if n else 0,
            "high": _pct(high, n),
            "moderate": _pct(moderate, n),
            "phishing_verdict": _pct(verdicts["phishing"], n),
            "suspicious_verdict": _pct(verdicts["suspicious"], n),
            "clean_verdict": _pct(verdicts["clean"], n),
        },
        "samples": pool,
    }


def _pct(count: int, total: int) -> float:
    if not total:
        return 0
    return round(100 * count / total, 1)


if __name__ == "__main__":
    main()
