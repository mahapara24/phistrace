"""Lexical LightGBM baseline on the same splits as the rule detector.

The model is a comparison only; PhishTrace does not use it. It is trained on
development splits and measured on the held-out test splits. Three feature views
show how much of its score comes from how the data sets were collected:
  full       scheme, www, host, path, and query
  no_prefix  scheme and a leading www are removed
  host_only  only the host is left, so the path gives nothing away

Usage (after python scripts/robustness.py --score)
  python scripts/baseline_lightgbm.py     # needs lightgbm, scikit-learn, numpy, scipy
"""

from __future__ import annotations

import json
import math
import pickle
import re
import sys
import time
import zlib
from collections import Counter
from pathlib import Path

import lightgbm as lgb
import numpy as np
from scipy.stats import chi2
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
SEED = 967
WORDS = re.compile("login|signin|secure|verify|account|update|bank|confirm|support|wallet")
CONSONANTS = re.compile("[bcdfghjklmnpqrstvwxz]+")
TLD = 24  # column holding the hashed suffix


def entropy(text: str) -> float:
    total = len(text) or 1
    return -sum(v / total * math.log2(v / total) for v in Counter(text).values())


def features(url: str, view: str) -> list[float]:
    match = re.match(r"(?i)(https?)://", url)
    scheme = match.group(1).lower() if match else ""
    rest = url[match.end():] if match else url
    if view != "full":
        rest = re.sub(r"(?i)^www\.", "", rest).rstrip("/")
    cut = min([rest.find(c) for c in "/?#" if c in rest] or [len(rest)])
    host, path = rest[:cut].lower(), rest[cut:]
    if view == "host_only":
        rest, path = host, ""
    parts = host.split(".")
    tld, longest = parts[-1], max(parts, key=len)
    row = [
        len(rest), len(host), len(path), host.count("."), host.count("-"), sum(c.isdigit() for c in host), sum(c.isdigit() for c in path),
        path.count("/"), path.count("?"), path.count("="), path.count("&"), rest.count("%"), rest.count("@"), rest.count("_"), path.count("."),
        entropy(host), entropy(path), len(longest), max([len(x) for x in CONSONANTS.findall(host)] or [0]),
        sum(c in "aeiou" for c in host) / (len(host) or 1), int(bool(re.fullmatch(r"[\d.]+(:\d+)?", host))), host.count(":"),
        int(host.startswith("xn--") or ".xn--" in host), len(tld), zlib.crc32(tld.encode()) % 512, len(WORDS.findall(rest.lower())),
    ]
    if view == "full":
        row += [int(scheme == "http"), int(scheme == "https"), int(host.startswith("www."))]
    return row


def matrix(urls: list[str], view: str) -> np.ndarray:
    return np.array([features(u, view) for u in urls], dtype=np.float32)


def scores(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    tp, fp, fn, tn = int((y & p).sum()), int((~y & p).sum()), int((y & ~p).sum()), int((~y & ~p).sum())
    return {
        "accuracy": (tp + tn) / len(y), "precision": tp / max(1, tp + fp), "recall": tp / (tp + fn),
        "f1": 2 * tp / (2 * tp + fp + fn), "fpr": fp / (fp + tn),
    }


def mcnemar(a: np.ndarray, b: np.ndarray) -> dict[str, float]:
    x, z = int((a & ~b).sum()), int((~a & b).sum())
    stat = (abs(x - z) - 1) ** 2 / (x + z) if x + z else 0.0
    return {"rules_only_correct": x, "model_only_correct": z, "chi2": round(stat, 1), "p": float(chi2.sf(stat, 1))}


def main() -> None:
    with (ROOT / "data" / "raw" / "pred_v4.pkl").open("rb") as handle:
        data = pickle.load(handle)
    feeds = ("openphish", "phishdb", "urlhaus")
    dev = [(r[0], r[1] == "phishing") for r in data["phiusiil"] if r[2] == "dev" and r[3]]
    extra = [(x[0], True) for k in ("phishdb_dev", "urlhaus_dev") for x in data[k]] + [(f"https://{x[0]}/", False) for x in data["tranco_dev"]]
    test = [r for r in data["phiusiil"] if r[2] == "test" and r[3]]
    y = np.array([r[1] == "phishing" for r in test])
    mal = [x[0] for k in feeds for x in data[k]]
    safe = [f"https://{x[0]}/" for x in data["tranco"]]
    rw_y = np.array([True] * len(mal) + [False] * len(safe))
    rules = np.array([r[3][1] != "clean" for r in test])
    rw_rules = np.array([bool(x[1]) and x[1][1] != "clean" for k in (*feeds, "tranco") for x in data[k]])
    rw_rules_host = np.array([bool(x[1]) and x[1][1] != "clean" for k in (*(f + "_host" for f in feeds), "tranco") for x in data[k]])

    def has_path(u: str) -> bool:
        return "/" in re.sub(r"(?i)^https?://", "", u).rstrip("/")

    out: dict[str, object] = {
        "n": {"train_phiusiil": len(dev), "train_extra": len(extra), "test": len(test), "realworld": len(rw_y)},
        "rules": {"phiusiil": scores(y, rules), "realworld": scores(rw_y, rw_rules), "realworld_host_only": scores(rw_y, rw_rules_host)},
        "shortcuts": {
            "phiusiil_not_https_www_homepage": scores(y, np.array([not (r[0].lower().startswith("https://www.") and not has_path(r[0])) for r in test])),
            "realworld_has_path": scores(rw_y, np.array([has_path(u) for u in mal + safe])),
        },
        "path_share": {k: float(np.mean([has_path(x[0]) for x in data[k]])) for k in (*feeds, "tranco")},
        "phiusiil_https_www_homepage": {
            name: float(np.mean([r[0].lower().startswith("https://www.") and not has_path(r[0]) for r in test if (r[1] == "phishing") == flag]))
            for name, flag in (("phishing", True), ("legitimate", False))
        },
        "models": {},
    }
    saved: dict[str, object] = {"urls": [r[0] for r in test]}
    for view in ("full", "no_prefix", "host_only"):
        xt, xr = matrix([r[0] for r in test], view), matrix(mal + safe, view)
        for name, train in (("phiusiil", dev), ("phiusiil+realworld", dev + extra)):
            order = np.random.default_rng(SEED).permutation(len(train))
            x = matrix([train[i][0] for i in order], view)
            t = np.array([train[i][1] for i in order])
            model = lgb.LGBMClassifier(n_estimators=300, num_leaves=63, learning_rate=0.08, random_state=SEED, n_jobs=4, verbose=-1, deterministic=True, force_row_wise=True)
            model.fit(x, t, categorical_feature=[TLD])
            pt, pr = model.predict_proba(xt)[:, 1], model.predict_proba(xr)[:, 1]

            saved[f"{view}|{name}"] = pt.astype(np.float32)

            def recall_at(truth, prob, fpr):
                cut = np.quantile(prob[~truth], 1 - fpr)
                return float((prob[truth] > cut).mean())

            entry = {
                "phiusiil": {**scores(y, pt > 0.5), "auc": float(roc_auc_score(y, pt)), "recall_at_rules_fpr": recall_at(y, pt, out["rules"]["phiusiil"]["fpr"])},
                "realworld": {**scores(rw_y, pr > 0.5), "auc": float(roc_auc_score(rw_y, pr)), "recall_at_rules_fpr": recall_at(rw_y, pr, out["rules"]["realworld"]["fpr"])},
                "mcnemar_phiusiil": mcnemar(rules == y, (pt > 0.5) == y),
                "mcnemar_realworld": mcnemar(rw_rules == rw_y, (pr > 0.5) == rw_y),
            }
            one = [r[0] for r in test[:300]]
            started = time.perf_counter()
            for u in one:
                model.predict_proba(matrix([u], view))
            entry["ms_per_url"] = (time.perf_counter() - started) / len(one) * 1000
            out["models"][f"{view}|{name}"] = entry
            print(view, name, json.dumps({k: entry[k] for k in ("phiusiil", "realworld")}, default=float))
    with (ROOT / "data" / "raw" / "lightgbm_test.pkl").open("wb") as handle:
        pickle.dump(saved, handle)  # used by summarize_llm.py
    (ROOT / "data" / "eval_lightgbm.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
