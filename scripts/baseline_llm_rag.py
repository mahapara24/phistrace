"""One-pass RAG baseline with a local open-weight language model (Ollama).

It runs on the same seeded, class-balanced sample of 1,000 PhiUSIIL test URLs as
the three PhishTrace modes. Step 1: the model names the URL features it finds worth
checking. Step 2: those words and the URL's own words are the query of a BM25
search over the exhibits (top 3). Step 3: the model returns a label and a
short report in which every sentence names the exhibits it relies on. Nothing
checks those citations: this is the baseline, not part of PhishTrace.

Usage
  ollama serve            # with llama3.2 pulled
  python scripts/baseline_llm_rag.py            # resumable; appends to the JSONL file
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import evaluate as ev  # noqa: E402
from app import retrieval  # noqa: E402
from app.corpus import DOCS  # noqa: E402

API = "http://localhost:11434/api/"
OUT = ROOT / "data" / "llm_rag_reports.jsonl"
SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["phishing", "legitimate"]},
        "report": {
            "type": "array",
            "minItems": 1,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {"sentence": {"type": "string"}, "exhibits": {"type": "array", "items": {"type": "string"}}},
                "required": ["sentence", "exhibits"],
            },
        },
    },
    "required": ["verdict", "report"],
}


def call(name: str, payload: dict) -> dict:
    request = urllib.request.Request(API + name, json.dumps(payload).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=300) as response:
        return json.load(response)


def sample() -> list[tuple[str, str]]:
    """Exactly the sample drawn by evaluate._chain."""
    rows = []
    for url, label in ev._phiusiil():
        if ev.split_of(url) != "test":
            continue
        try:
            ev.analyze(url)
        except ValueError:
            continue
        rows.append((label, url))
    rng = random.Random(ev.SEED)
    half = ev.CHAIN_SAMPLE // 2
    phish = [u for label, u in rows if label == "phishing"]
    legit = [u for label, u in rows if label == "legitimate"]
    return [(u, "phishing") for u in rng.sample(phish, half)] + [(u, "legitimate") for u in rng.sample(legit, half)]


# Same pool as retrieval.search: policy exhibits about the workbench itself are left out.
POOL = [d for d in DOCS if not {"path_policy", "legitimacy"} & set(d["tags"])]
_BODY = [retrieval._TOKEN.findall(f"{d['title']} {d['text']}".lower()) for d in POOL]
_MEAN = sum(map(len, _BODY)) / len(_BODY)
_DF = {w: sum(w in set(body) for body in _BODY) for body in _BODY for w in body}


def bm25(query: set[str], k1: float = 1.5, b: float = 0.75) -> list[dict]:
    scored = []
    for index, body in enumerate(_BODY):
        total = 0.0
        for word in query:
            tf = body.count(word)
            if tf:
                idf = math.log(1 + (len(POOL) - _DF[word] + 0.5) / (_DF[word] + 0.5))
                total += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(body) / _MEAN))
        scored.append((-total, index))
    return [POOL[index] for _, index in sorted(scored)[:3]]


def cue_prompt(url: str) -> str:
    return (
        "You see only the text of a URL. In at most 12 words, name the features of the URL text an analyst should check "
        "for phishing (for example the host type, suffix, scheme, brand name, words, length). Give only the words.\n\n"
        f"URL: {url}\n\nFeatures:"
    )


def prompt(url: str, docs: list[dict]) -> str:
    passages = "\n".join(f"[{d['id']}] {d['title']}. {d['text']}" for d in docs)
    return (
        "You are a security analyst. You see only the text of a URL; you cannot open the page. "
        "Decide whether the URL is phishing or legitimate and write a short report of 2 or 3 sentences. "
        "Base the report on the exhibits below, and list for each sentence the ids of the exhibits that support it.\n\n"
        f"Exhibits:\n{passages}\n\nURL: {url}\n\nAnswer as JSON."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="llama3.2:latest")
    parser.add_argument("--out", default=str(OUT))
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    rows = sample()
    done = set()
    out = Path(args.out)
    if out.exists():
        done = {json.loads(line)["url"] for line in out.read_text(encoding="utf-8").splitlines()}
    # alternate the classes so a partial file stays balanced
    order = [i for pair in zip(range(0, 500), range(500, 1000)) for i in pair]
    if args.limit:
        order = order[: args.limit]
    with out.open("a", encoding="utf-8") as handle:
        for i in order:
            url, label = rows[i]
            if url in done:
                continue
            started = time.perf_counter()
            options = {"temperature": 0, "seed": ev.SEED, "num_ctx": 2048}
            first = call("generate", {"model": args.model, "prompt": cue_prompt(url), "stream": False, "keep_alive": "30m",
                                      "options": {**options, "num_predict": 30}})
            docs = bm25(retrieval.tokenize(f"{url} {first['response']}"))
            try:
                reply = call("generate", {
                    "model": args.model, "prompt": prompt(url, docs), "stream": False, "format": SCHEMA,
                    "keep_alive": "30m", "options": {**options, "num_predict": 260},
                })
                parsed = json.loads(reply["response"])
                record = {"verdict": parsed["verdict"], "report": parsed["report"], "load_s": round((first.get("load_duration", 0) + reply.get("load_duration", 0)) / 1e9, 3)}
            except (ValueError, KeyError) as error:
                record = {"verdict": "invalid", "report": [], "error": str(error)[:80], "load_s": 0}
            record.update(cues=first["response"], url=url, label=label, retrieved=[d["id"] for d in docs], seconds=round(time.perf_counter() - started, 3))
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            handle.flush()


if __name__ == "__main__":
    main()
