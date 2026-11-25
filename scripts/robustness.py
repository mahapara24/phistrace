"""Confidence intervals, McNemar tests, rule ablation, and sensitivity analysis.

Every rule version (legacy/v1, v2, v3 and the current app/) scores the same URLs.
The per-URL results are cached in data/raw/pred_*.pkl. Nothing here changes a
rule or a threshold; the test split is only measured.

Usage
  python scripts/robustness.py --score      # about 15 minutes; caches per-URL results
  python scripts/robustness.py              # writes data/eval_robustness.json
Needs numpy and scipy (analysis only; the detector needs neither).
"""

from __future__ import annotations

import argparse
import json
import math
import pickle
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
VERSIONS = {"v1": ROOT / "legacy" / "v1", "v2": ROOT / "legacy" / "v2", "v3": ROOT / "legacy" / "v3", "v4": ROOT}


def score_version(tag: str) -> None:
    """Runs in its own process so that each version imports its own app package."""
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "scripts"))
    import evaluate as ev

    for name in [k for k in sys.modules if k == "app" or k.startswith("app.")]:
        del sys.modules[name]
    sys.path.insert(0, str(VERSIONS[tag]))
    from app import detector

    assert Path(detector.__file__).is_relative_to(VERSIONS[tag])

    def one(url: str):
        try:
            r = detector.analyze(url)
        except ValueError:
            return None
        hits = tuple((str(i["id"]), int(i["weight"])) for i in r["indicators"])
        return hits, r["verdict"]["code"], int(r.get("raw_score", r["score"])), bool(r["official_brands"]), bool(r["brand_mismatches"]), bool(r["features"].get("raw_executable"))

    def pick(items, size=ev.EXTERNAL_SAMPLE):
        return random.Random(ev.SEED).sample(items, size) if len(items) > size else items

    def dev(items):
        return [i for i in items if ev.split_of(i) == "dev"]

    out = {
        "phiusiil": [(u, l, ev.split_of(u), one(u)) for u, l in ev._phiusiil()],
        "openphish": [(u, one(u)) for u in ev._lines(ev.OPENPHISH)],
        "phishdb": [(u, one(u)) for u in pick(ev._test_only(ev._lines(ev.PHISHDB)))],
        "urlhaus": [(u, one(u)) for u in pick(ev._test_only(ev._urlhaus()))],
        "tranco": [(u, one(f"https://{u}/")) for u in ev._test_only(ev._tranco())],
        "phishdb_dev": [(u, one(u)) for u in pick(dev(ev._lines(ev.PHISHDB)), 9000)],
        "urlhaus_dev": [(u, one(u)) for u in pick(dev(ev._urlhaus()), 9000)],
        "tranco_dev": [(u, one(f"https://{u}/")) for u in dev(ev._tranco())],
    }
    if tag == "v4":  # the same feeds cut down to scheme and host, so a path gives nothing away
        from urllib.parse import urlsplit

        def host_only(u: str) -> str:
            full = u if "://" in u else "http://" + u
            netloc = urlsplit(full).netloc
            return f"https://{netloc}/"

        for key in ("openphish", "phishdb", "urlhaus"):
            out[key + "_host"] = [(host_only(u), one(host_only(u))) for u, _ in out[key]]
    with (RAW / f"pred_{tag}.pkl").open("wb") as handle:
        pickle.dump(out, handle, protocol=4)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--score", action="store_true")
    parser.add_argument("--one", choices=list(VERSIONS))
    args = parser.parse_args()
    if args.one:
        score_version(args.one)
        return
    if args.score:
        for tag in VERSIONS:
            subprocess.run([sys.executable, "-B", __file__, "--one", tag], check=True)
            print("scored", tag, flush=True)
    analyse()


def analyse() -> None:
    import numpy as np
    from scipy.stats import chi2, spearmanr

    sys.path.insert(0, str(ROOT))
    from app import detector as D

    preds = {}
    for tag in VERSIONS:
        with (RAW / f"pred_{tag}.pkl").open("rb") as handle:
            preds[tag] = pickle.load(handle)
    cur = preds["v4"]
    rng = np.random.default_rng(967)
    res: dict[str, object] = {}

    def flag(p, codes=("phishing", "suspicious")):
        return bool(p) and p[1] in codes

    test = {t: [r for r in preds[t]["phiusiil"] if r[2] == "test" and r[3]] for t in VERSIONS}
    y = np.array([r[1] == "phishing" for r in test["v4"]])
    assert all([r[0] for r in test[t]] == [r[0] for r in test["v4"]] for t in VERSIONS)

    def counts(p):
        return np.array([(y & p).sum(), (~y & p).sum(), (y & ~p).sum(), (~y & ~p).sum()])

    def measures(c):
        tp, fp, fn, tn = c
        return {
            "accuracy": float((tp + tn) / (tp + fp + fn + tn)), "precision": float(tp / (tp + fp)), "recall": float(tp / (tp + fn)),
            "f1": float(2 * tp / (2 * tp + fp + fn)), "fpr": float(fp / (fp + tn)),
        }

    def interval(c, n=10000):
        """Percentile bootstrap, resampling phishing and legitimate rows separately."""
        tp, fp, fn, tn = (int(v) for v in c)
        a = rng.binomial(tp + fn, tp / (tp + fn), n)
        b = rng.binomial(fp + tn, fp / (fp + tn), n)
        pos, neg = tp + fn, fp + tn
        series = {"accuracy": (a + neg - b) / (pos + neg), "precision": a / (a + b), "recall": a / pos, "f1": 2 * a / (a + b + pos), "fpr": b / neg}
        return {k: [float(x) for x in np.percentile(v, [2.5, 97.5])] for k, v in series.items()}

    def mcnemar(ok_a, ok_b):
        only_a, only_b = int((ok_a & ~ok_b).sum()), int((~ok_a & ok_b).sum())
        stat = (abs(only_a - only_b) - 1) ** 2 / (only_a + only_b) if only_a + only_b else 0.0
        return {"only_first_correct": only_a, "only_second_correct": only_b, "chi2": round(float(stat), 2), "p": float(chi2.sf(stat, 1))}

    # ---------------------------------------------------------------- intervals and McNemar
    alert = {t: np.array([flag(r[3]) for r in test[t]]) for t in VERSIONS}
    strict = {t: np.array([flag(r[3], ("phishing",)) for r in test[t]]) for t in VERSIONS}
    res["phiusiil_ci"] = {
        t: {name: {"point": measures(counts(p[t])), "ci95": interval(counts(p[t]))} for name, p in (("alert", alert), ("strict", strict))}
        for t in VERSIONS
    }
    pairs = [("v1", "v2"), ("v2", "v3"), ("v3", "v4"), ("v2", "v4"), ("v1", "v4")]
    res["mcnemar_phiusiil"] = {
        f"{a}-{b}": {
            "all": mcnemar(alert[a] == y, alert[b] == y),
            "phishing": mcnemar(alert[a][y], alert[b][y]),
            "legitimate": mcnemar(~alert[a][~y], ~alert[b][~y]),
        }
        for a, b in pairs
    }
    feeds = ("openphish", "phishdb", "urlhaus")
    rw_y = np.array([True] * sum(len(cur[k]) for k in feeds) + [False] * len(cur["tranco"]))
    rw = {t: np.array([flag(x[1]) for k in (*feeds, "tranco") for x in preds[t][k]]) for t in VERSIONS}
    res["mcnemar_realworld"] = {
        f"{a}-{b}": {
            "all": mcnemar(rw[a] == rw_y, rw[b] == rw_y),
            "malicious": mcnemar(rw[a][rw_y], rw[b][rw_y]),
            "safe": mcnemar(~rw[a][~rw_y], ~rw[b][~rw_y]),
        }
        for a, b in pairs
    }

    def wilson(k, n, z=1.959964):
        p, d = k / n, 1 + z * z / n
        half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
        centre = (p + z * z / (2 * n)) / d
        return [centre - half, centre + half]

    def rw_counts(p):
        return np.array([(rw_y & p).sum(), (~rw_y & p).sum(), (rw_y & ~p).sum(), (~rw_y & ~p).sum()])

    res["realworld_ci"] = {
        t: {
            **{k: {"rate": sum(flag(x[1]) for x in preds[t][k]) / len(preds[t][k]), "ci95": wilson(sum(flag(x[1]) for x in preds[t][k]), len(preds[t][k]))} for k in (*feeds, "tranco")},
            "pooled": {"point": measures(rw_counts(rw[t])), "ci95": interval(rw_counts(rw[t]))},
        }
        for t in VERSIONS
    }

    # ---------------------------------------------------------------- what is missed
    missed = [r for r in test["v4"] if r[1] == "phishing" and not flag(r[3])]
    none = sum(1 for r in missed if not r[3][0])
    single = sum(1 for r in missed if len({i for i, _ in r[3][0]}) == 1)
    single_http = sum(1 for r in missed if {i for i, _ in r[3][0]} == {"no_https"})
    res["missed"] = {"n": len(missed), "no_rule": none, "one_rule": single, "only_http": single_http, "two_or_more": len(missed) - none - single}

    # ---------------------------------------------------------------- re-deciding without a rule
    def decide(p, drop=frozenset(), weights=None, phishing_at=40, moderate=21):
        hits, _, _, official, mismatch, executable = p
        kept = [(i, w if weights is None else weights[i] * w / BASE_W[i]) for i, w in hits if i not in drop]
        D.PHISHING_AT, D.LEVEL_MODERATE = phishing_at, moderate
        official = official and (not mismatch or "brand_mismatch" in drop)
        return D.decide({
            "indicators": [{"id": i, "text": ""} for i, _ in kept], "official_brands": official, "brand_mismatches": False,
            "features": {"raw_executable": executable and "file_download" not in drop}, "score": min(100, sum(w for _, w in kept)), "notes": [],
        })["code"]

    ids = [str(r["id"]) for r in D.catalog()]
    labels = {str(r["id"]): str(r["label"]) for r in D.catalog()}
    BASE_W = {r["id"]: (D.W_LURE if r["id"] == "lure_terms" else int(str(r["weight"]).split()[0])) for r in D.catalog()}
    rows = [r[3] for r in test["v4"]]
    mal = [x[1] for k in feeds for x in cur[k]]
    safe = [x[1] for x in cur["tranco"]]
    assert all(decide(p) == p[1] for p in rows) and all(decide(p) == p[1] for p in mal + safe if p)

    def auc(pos, neg):
        s = np.concatenate([pos, neg])
        order = np.unique(s, return_inverse=True)
        cnt = np.bincount(order[1])
        rank = (np.cumsum(cnt) - (cnt - 1) / 2)[order[1]]
        return float((rank[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))

    def raw(p, weights=None, drop=frozenset()):
        return sum((w if weights is None else weights[i] * w / BASE_W[i]) for i, w in p[0] if i not in drop) if p else 0.0

    def evaluate(fn):
        c = measures(counts(np.array([fn(p) for p in rows])))
        r = measures(rw_counts(np.array([bool(p) and fn(p) for p in mal + safe])))
        return {"phiusiil": c, "realworld": r}

    full = evaluate(lambda p: p[1] != "clean")
    full_auc = auc(np.array([raw(p) for p, t in zip(rows, y) if t]), np.array([raw(p) for p, t in zip(rows, y) if not t]))
    res["full"] = {**full, "roc_auc": full_auc}
    ablation = []
    for rule in ids:
        drop = frozenset([rule])
        e = evaluate(lambda p: (decide(p, drop) if any(i == rule for i, _ in p[0]) else p[1]) != "clean")
        a = auc(np.array([raw(p, None, drop) for p, t in zip(rows, y) if t]), np.array([raw(p, None, drop) for p, t in zip(rows, y) if not t]))
        ablation.append({
            "id": rule, "label": labels[rule], "weight": BASE_W[rule],
            "d_f1": e["phiusiil"]["f1"] - full["phiusiil"]["f1"], "d_recall": e["phiusiil"]["recall"] - full["phiusiil"]["recall"],
            "d_fpr": e["phiusiil"]["fpr"] - full["phiusiil"]["fpr"], "d_auc": a - full_auc,
            "rw_d_f1": e["realworld"]["f1"] - full["realworld"]["f1"], "rw_d_recall": e["realworld"]["recall"] - full["realworld"]["recall"],
            "rw_d_fpr": e["realworld"]["fpr"] - full["realworld"]["fpr"],
        })
    res["ablation"] = ablation

    # ---------------------------------------------------------------- thresholds
    res["threshold_alert"] = {str(t): evaluate(lambda p: decide(p, moderate=t) != "clean") for t in (8, 12, 16, 18, 21, 24, 28, 32)}
    res["threshold_strict"] = {str(t): evaluate(lambda p: decide(p, phishing_at=t) == "phishing") for t in (30, 35, 40, 45, 50)}
    scores = np.array([min(100, p[2]) for p in rows])
    res["threshold_deep"] = {str(t): {"phishing_deep": float((scores[y] >= t).mean()), "legitimate_deep": float((scores[~y] >= t).mean())} for t in (40, 45, 50, 55, 60)}

    # ---------------------------------------------------------------- weights
    dev_rows = [(r[3], r[1] == "phishing") for r in cur["phiusiil"] if r[2] == "dev" and r[3]]
    dev_rows += [(x[1], True) for k in ("phishdb_dev", "urlhaus_dev") for x in cur[k] if x[1]]
    dev_rows += [(x[1], False) for x in cur["tranco_dev"] if x[1]]
    npos = sum(t for _, t in dev_rows)
    nneg = len(dev_rows) - npos
    llr = {}
    for rule in ids:
        a = sum(1 for p, t in dev_rows if t and any(i == rule for i, _ in p[0]))
        b = sum(1 for p, t in dev_rows if not t and any(i == rule for i, _ in p[0]))
        llr[rule] = math.log(((a + 0.5) / (npos + 1)) / ((b + 0.5) / (nneg + 1)))
    scale = sum(BASE_W.values()) / sum(max(v, 0) for v in llr.values())
    data_w = {k: max(v, 0) * scale for k, v in llr.items()}
    equal_w = {k: sum(BASE_W.values()) / len(BASE_W) for k in BASE_W}
    rho = spearmanr([BASE_W[k] for k in ids], [llr[k] for k in ids])
    res["weights"] = {"hand": BASE_W, "log_ratio": llr, "spearman": float(rho.statistic), "spearman_p": float(rho.pvalue)}

    def weight_row(w):
        a = evaluate(lambda p: decide(p, weights=w) != "clean")
        s = evaluate(lambda p: decide(p, weights=w) == "phishing")
        return {
            "alert_f1": a["phiusiil"]["f1"], "alert_fpr": a["phiusiil"]["fpr"], "rw_alert_f1": a["realworld"]["f1"], "rw_alert_fpr": a["realworld"]["fpr"],
            "strict_f1": s["phiusiil"]["f1"], "rw_strict_f1": s["realworld"]["f1"],
            "roc_auc": auc(np.array([raw(p, w) for p, t in zip(rows, y) if t]), np.array([raw(p, w) for p, t in zip(rows, y) if not t])),
            "rw_roc_auc": auc(np.array([raw(p, w) for p in mal]), np.array([raw(p, w) for p in safe])),
        }

    res["weight_schemes"] = {"hand": weight_row(BASE_W), "equal": weight_row(equal_w), "log_ratio": weight_row(data_w)}
    for span in (0.25, 0.5):
        runs = []
        for seed in range(20):
            g = np.random.default_rng(seed)
            runs.append(weight_row({k: v * g.uniform(1 - span, 1 + span) for k, v in BASE_W.items()}))
        res[f"perturb_{int(span * 100)}"] = {k: [min(r[k] for r in runs), max(r[k] for r in runs)] for k in runs[0]}

    out = ROOT / "data" / "eval_robustness.json"
    out.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
