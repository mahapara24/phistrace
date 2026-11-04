"""Term-overlap retrieval over the local exhibit file. No embeddings."""

from __future__ import annotations

import re

from app.corpus import DOCS, VERSION

_TOKEN = re.compile(r"[a-z0-9]{2,}")
_STOP = {"www", "com", "htm", "html", "php", "asp", "index", "http", "https"}


def tokenize(value: str) -> set[str]:
    return {token for token in _TOKEN.findall(value.lower()) if token not in _STOP}


def search(query_terms: set[str], limit: int = 3) -> list[dict[str, object]]:
    scored: list[tuple[int, dict[str, object]]] = []
    for doc in DOCS:
        # Policy exhibits are fetched by tag so process language does not crowd the open search.
        if "path_policy" in doc["tags"] or "legitimacy" in doc["tags"]:
            continue
        body = tokenize(f"{doc['title']} {doc['text']}")
        tags = set(doc["tags"])
        score = len(query_terms & tags) * 8 + len(query_terms & body)
        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda item: (-item[0], str(item[1]["id"])))
    return [_view(doc, score) for score, doc in scored[:limit]]


def by_tag(tag: str) -> list[dict[str, object]]:
    return [_view(doc, 10) for doc in DOCS if tag in doc["tags"]]


def _view(doc: dict[str, object], score: int) -> dict[str, object]:
    return {
        "id": doc["id"],
        "title": doc["title"],
        "text": doc["text"],
        "tags": list(doc["tags"]),
        "source": doc["source"],
        "kind": "exhibit",
        "score": score,
    }
