"""Summarise the language-model baseline on the URLs it has answered, next to the rules and LightGBM.

  python scripts/summarize_llm.py          # writes data/eval_llm_rag.json
"""

from __future__ import annotations

import json
import pickle
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np  # noqa: E402
from baseline_lightgbm import mcnemar, scores  # noqa: E402

from app.corpus import DOCS  # noqa: E402
from app.detector import analyze  # noqa: E402


def wilson(k: int, total: int, z: float = 1.96) -> list[float]:
    share, w = k / total, z * z / total
    half = z * (share * (1 - share) / total + w / (4 * total)) ** 0.5
    return [(share + w / 2 - half) / (1 + w), (share + w / 2 + half) / (1 + w)]


def main() -> None:
    rows = [json.loads(line) for line in (ROOT / "data" / "llm_rag_reports.jsonl").read_text(encoding="utf-8").splitlines()]
    with (ROOT / "data" / "raw" / "lightgbm_test.pkl").open("rb") as handle:
        saved = pickle.load(handle)
    index = {u: i for i, u in enumerate(saved["urls"])}
    y = np.array([r["label"] == "phishing" for r in rows])
    found = [analyze(r["url"]) for r in rows]
    llm = np.array([r["verdict"] == "phishing" for r in rows])
    rules = np.array([d["verdict"]["code"] != "clean" for d in found])
    out = {"n": len(rows), "phishing": int(y.sum()), "invalid": sum(r["verdict"] == "invalid" for r in rows)}
    out["systems"] = {"rules": scores(y, rules), "llm_rag": scores(y, llm)}
    for name in ("full|phiusiil", "no_prefix|phiusiil", "no_prefix|phiusiil+realworld"):
        prob = np.array([saved[name][index[r["url"]]] for r in rows])
        out["systems"][f"lightgbm {name}"] = scores(y, prob > 0.5)
    rng = np.random.default_rng(967)
    out["f1_ci95"] = {}
    for name, p in (("rules", rules), ("llm_rag", llm)):
        pos, neg = int(y.sum()), int((~y).sum())
        a, b = rng.binomial(pos, (p & y).sum() / pos, 10000), rng.binomial(neg, (p & ~y).sum() / neg, 10000)
        out["f1_ci95"][name] = [float(x) for x in np.percentile(2 * a / (a + b + pos), [2.5, 97.5])]
    out["mcnemar_rules_llm"] = mcnemar(rules == y, llm == y)
    seconds = [r["seconds"] - r["load_s"] for r in rows]
    out["seconds"] = {"mean": statistics.fmean(seconds), "median": statistics.median(seconds)}
    # the sentences the model wrote, and what it cited
    ids = {d["id"]: set(d["tags"]) for d in DOCS}
    total = none = unknown = outside = fired = 0
    for r, d in zip(rows, found):
        hits = {str(i["id"]) for i in d["indicators"]}
        for part in r["report"]:
            total += 1
            cited = set(part["exhibits"])
            if not cited:
                none += 1
            elif not cited & set(ids):
                unknown += 1
            elif not cited & set(r["retrieved"]):
                outside += 1
            fired += any(ids.get(c, set()) & hits for c in cited)
    out["sentences"] = {"total": total, "per_report": total / len(rows), "no_citation": none, "unknown_exhibit": unknown, "not_retrieved": outside, "cites_fired_rule": fired}
    # a claim that needs no judge: "uses HTTPS" about a URL that starts with http://
    https = re.compile(r"\buses\s+(?:the\s+)?https\b", re.I)
    plain = [r for r in rows if r["url"].lower().startswith("http:")]
    wrong = [sum(bool(https.search(p["sentence"])) for p in r["report"]) for r in plain]
    out["false_https"] = {"http_urls": len(plain), "urls": sum(w > 0 for w in wrong), "sentences": sum(wrong)}
    # did retrieval bring back an exhibit of any rule that the detector fired?
    with_rule = [(r, {str(i["id"]) for i in d["indicators"]}) for r, d in zip(rows, found) if d["indicators"]]
    out["retrieval_hit"] = {"urls_with_rule": len(with_rule), "hit": sum(any(ids[c] & h for c in r["retrieved"]) for r, h in with_rule)}
    judge = ROOT / "data" / "judge_support.jsonl"
    if judge.exists():
        # sentences about a fired rule are kept apart from the two fixed low-signal sentences
        table: dict[str, dict[str, dict]] = {"rule": {}, "low_signal": {}}
        lines = [json.loads(line) for line in judge.read_text(encoding="utf-8").splitlines()]
        for j in lines:
            kind = "low_signal" if j["sentence"].startswith(("No weighted indicator", "The score stays")) else "rule"
            cell = table[kind].setdefault(j["system"], {"n": 0, "supported": 0})
            cell["n"] += 1
            cell["supported"] += j["label"] == "supported"
        for cells in table.values():
            for cell in cells.values():
                cell["ci95"] = wilson(cell["supported"], cell["n"])
        out["judge"] = {"urls": len({j["url"] for j in lines}), "invalid": sum(j["label"] == "invalid" for j in lines), **table}
    (ROOT / "data" / "eval_llm_rag.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
