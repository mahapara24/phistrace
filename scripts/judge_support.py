"""Automatic check of sentence support with a local judge model that wrote none of the sentences.

The judge (phi3) sees one published sentence and its cited evidence and answers yes or no:
does the evidence address the topic of the claim? Control pairs (the same PhishTrace sentence
with a randomly chosen wrong exhibit) show how far the judge can be trusted. A judge forced to
answer as JSON said "not supported" for every pair, so the answer is plain text. The wording was
chosen on 12 control pairs from the first 60 URLs; the results use the next 100 URLs.
  python scripts/judge_support.py          # resumable; writes data/judge_support.jsonl
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from app import agents  # noqa: E402
from app.corpus import DOCS, by_id  # noqa: E402
from baseline_llm_rag import call  # noqa: E402

OUT = ROOT / "data" / "judge_support.jsonl"
FIRST, LAST = 60, 160
MODEL = "phi3:latest"


def prompt(item: dict) -> str:
    return (
        f"Evidence: {item['evidence'] or '(none)'}\n\nClaim: {item['sentence']}\n\n"
        "Does the evidence talk about the topic of the claim? Reply with one word only: yes or no."
    )


def items() -> list[dict]:
    out, rng = [], random.Random(967)
    for line in (ROOT / "data" / "llm_rag_reports.jsonl").read_text(encoding="utf-8").splitlines()[FIRST:LAST]:
        record = json.loads(line)
        modes = agents.investigate(record["url"], "compare")["modes"]
        for name, system in (("agentic", "PhishTrace"), ("retrieval", "Retrieval only")):
            for claim in modes[name]["published"]:
                base = {"url": record["url"], "sentence": claim["text"]}
                out.append({**base, "system": system, "evidence": "\n".join(f"{c['title']}. {c['text']}" for c in claim["citations"])})
                if name == "agentic":
                    wrong = rng.choice([d for d in DOCS if claim["rule_id"] not in d["tags"]])
                    out.append({**base, "system": "Control (wrong exhibit)", "evidence": f"{wrong['title']}. {wrong['text']}"})
        for part in record["report"]:
            docs = [by_id(i) for i in part["exhibits"]]
            out.append({"url": record["url"], "sentence": part["sentence"], "system": "LLM-RAG", "evidence": "\n".join(f"{d['title']}. {d['text']}" for d in docs if d)})
    return out


def main() -> None:
    data = items()
    done = len(OUT.read_text(encoding="utf-8").splitlines()) if OUT.exists() else 0
    with OUT.open("a", encoding="utf-8") as handle:
        for item in data[done:]:
            reply = call("generate", {"model": MODEL, "prompt": prompt(item), "stream": False, "keep_alive": "30m",
                                      "options": {"temperature": 0, "seed": 967, "num_predict": 6, "num_ctx": 2048}})
            word = reply["response"].strip().lower()
            label = "supported" if word.startswith("yes") else "not supported" if word.startswith("no") else "invalid"
            handle.write(json.dumps({"system": item["system"], "url": item["url"], "sentence": item["sentence"], "cited": bool(item["evidence"]), "label": label}, ensure_ascii=False) + "\n")
            handle.flush()


if __name__ == "__main__":
    main()
