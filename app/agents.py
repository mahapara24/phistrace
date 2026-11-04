"""Three investigation modes over one rule signal.

rules      — publish the signal and a class label, with no exhibits
retrieval  — one search, citations not checked against indicator tags
agentic    — score chooses tools; the verifier drops sentences tags do not cover

No generative model is called. Roles are fixed functions.
"""

from __future__ import annotations

import time

from app import detector, retrieval
from app.corpus import by_id

MODES = ("rules", "retrieval", "agentic", "compare")

_MODE_NOTES = {
    "rules": "This mode publishes the rule signal and a class label. It does not retrieve exhibits, and it does not run the verifier.",
    "retrieval": "This mode runs one search over the URL's words and attaches those exhibits to every finding. It does not check that an exhibit tag covers the finding.",
    "agentic": "This mode chooses tools from the score, retrieves each indicator by its tag, and publishes a sentence only when the verifier finds a covering exhibit.",
}


def investigate(url: str, mode: str) -> dict[str, object]:
    if mode not in MODES:
        raise ValueError("Choose rules, retrieval, agentic, or compare.")
    detection = detector.analyze(url)
    if mode == "compare":
        modes = {name: run_mode(detection, name) for name in ("rules", "retrieval", "agentic")}
        return {
            "kind": "compare",
            "url": detection["url"],
            "input": detection["input"],
            "kb_version": retrieval.VERSION,
            "modes": modes,
            "primary": modes["agentic"],
            "comparison_rows": _comparison_rows(modes),
        }
    report = run_mode(detection, mode)
    return {
        "kind": "single",
        "url": detection["url"],
        "input": detection["input"],
        "kb_version": retrieval.VERSION,
        "modes": None,
        "primary": report,
        "comparison_rows": None,
    }


def run_mode(detection: dict[str, object], mode: str) -> dict[str, object]:
    started = time.perf_counter()
    needed = _needed(detection)
    ran = {key: False for key in needed}
    ran["signal"] = True
    ran["recommendation"] = True
    steps: list[dict[str, object]] = []
    claims: list[dict[str, object]] = []
    exhibits: list[dict[str, object]] = []

    detect_started = time.perf_counter()
    steps.append(
        _step(
            "Detect",
            f"{detection['verdict']['label']}. Rule signal {detection['score']} / 100.",
            _ms(detect_started),
            "done",
        )
    )
    steps.append(_step("Choose path", str(detection["path_reason"]), 0.0, "done"))

    brand_exhibit = None
    tld_exhibit = None
    generic: list[dict[str, object]] = []
    retrieve_ms = 0.0

    if mode == "agentic":
        brand_exhibit, tld_exhibit, steps, ran = _run_registries(detection, needed, steps, ran, True)
        retrieve_started = time.perf_counter()
        tagged: list[dict[str, object]] = []
        for indicator in detection["indicators"]:
            tagged.extend(retrieval.by_tag(str(indicator["id"])))
            ran["per_indicator"] = True
        if needed["legitimacy"]:
            tagged.extend(retrieval.by_tag("legitimacy"))
            ran["legitimacy"] = True
        if tagged or detection["indicators"] or needed["legitimacy"]:
            ran["kb"] = True
        retrieve_ms = _ms(retrieve_started)
        policy = by_id("ex-path")
        steps.append(_step("Retrieve", _retrieve_detail(detection, tagged), retrieve_ms, "done"))
        claims = _indicator_claims(detection["indicators"], tagged, brand_exhibit, tld_exhibit)
        if needed["legitimacy"]:
            claims.append(_legitimacy_claim(detection, tagged))
        _verify_agentic(claims)
        ran["verify"] = True
        ran["supported_only"] = True
        steps.append(_step("Verify", "Each sentence keeps only exhibits whose tags cover that indicator.", _ms(time.perf_counter()), "done"))
        if brand_exhibit:
            exhibits.append(brand_exhibit)
        if tld_exhibit:
            exhibits.append(tld_exhibit)
        exhibits.extend(tagged)
        if policy:
            exhibits.append(
                {
                    "id": policy["id"],
                    "title": policy["title"],
                    "text": policy["text"],
                    "tags": list(policy["tags"]),
                    "source": policy["source"],
                    "kind": "policy",
                    "score": 0,
                }
            )
    elif mode == "retrieval":
        steps.extend(_skipped_registries(needed))
        retrieve_started = time.perf_counter()
        generic = retrieval.search(_query_terms(detection), limit=3)
        retrieve_ms = _ms(retrieve_started)
        ran["kb"] = True
        steps.append(
            _step(
                "Retrieve",
                f"One search returned {len(generic)} exhibit(s). The same set is attached to every finding.",
                retrieve_ms,
                "done",
            )
        )
        claims = _indicator_claims(detection["indicators"], generic, None, None, force_all=True)
        if not detection["indicators"]:
            claims.append(
                {
                    "rule_id": "legitimacy",
                    "text": "No weighted indicator fired.",
                    "weight": 0,
                    "citations": [_cite(doc, "legitimacy") for doc in generic],
                }
            )
        _verify_open(claims)
        steps.append(_step("Verify", "The verifier does not run in this mode.", 0.0, "gap" if needed["verify"] else "skip"))
        exhibits.extend(generic)
    else:
        steps.extend(_skipped_registries(needed))
        steps.append(_step("Retrieve", "No exhibit is retrieved in this mode.", 0.0, "gap"))
        claims = _indicator_claims(detection["indicators"], [], None, None)
        if not claims:
            claims.append(
                {
                    "rule_id": "legitimacy",
                    "text": "No weighted indicator fired.",
                    "weight": 0,
                    "citations": [],
                }
            )
        label = "phishing" if int(detection["score"]) >= 50 else "legitimate"
        claims.append(
            {
                "rule_id": "class_label",
                "text": f"Class label: {label}. This sentence repeats the score band and has no exhibit.",
                "weight": 0,
                "citations": [],
            }
        )
        _verify_open(claims)
        steps.append(_step("Verify", "The verifier does not run in this mode.", 0.0, "gap"))

    published = [claim for claim in claims if claim["published"]]
    withheld = [claim for claim in claims if not claim["published"]]
    steps.append(
        _step(
            "Report",
            f"{len(published)} sentence(s) published, {len(withheld)} withheld.",
            0.0,
            "done",
        )
    )
    checklist = _checklist(needed, ran)
    required = [item for item in checklist if item["required"]]
    done_count = sum(1 for item in required if item["done"])
    completeness = done_count / len(required) if required else 1.0
    unsupported = [claim for claim in claims if claim["verdict"] != "supported"]
    unsupported_rate = len(unsupported) / len(claims) if claims else 0.0
    if published:
        support = sum(1 for claim in published if claim["verdict"] == "supported") / len(published)
    else:
        support = None

    _assign_letters(exhibits)
    letter_of = {item["id"]: item["letter"] for item in exhibits}
    for claim in claims:
        for citation in claim["citations"]:
            citation["letter"] = letter_of.get(citation["id"], "")

    total_ms = _ms(started)
    metrics = {
        "completeness": completeness,
        "completeness_label": _pct(completeness),
        "unsupported_rate": unsupported_rate,
        "unsupported_label": _pct(unsupported_rate),
        "evidence_support": support,
        "support_label": _pct(support),
        "retrieval_ms": retrieve_ms,
        "retrieval_label": _fmt_ms(retrieve_ms),
        "agent_ms": total_ms,
        "agent_label": _fmt_ms(total_ms),
        "candidate_claims": len(claims),
        "published_claims": len(published),
        "withheld_claims": len(withheld),
        "exhibit_count": len(exhibits),
        "checks_done": done_count,
        "checks_required": len(required),
    }
    return {
        "mode": mode,
        "mode_label": {"rules": "Rules only", "retrieval": "Retrieval only", "agentic": "Agentic chain"}[mode],
        "mode_note": _MODE_NOTES[mode],
        "detection": detection,
        "steps": steps,
        "checklist": checklist,
        "claims": claims,
        "published": published,
        "withheld": withheld,
        "exhibits": exhibits,
        "anatomy": _anatomy(detection),
        "pills": _pills(detection),
        "metrics": metrics,
        "summary": _summary(detection, published, withheld, mode),
        "recommendations": _recommendations(str(detection["verdict"]["code"])),
        "policy": by_id("ex-path")["text"] if mode == "agentic" else "",
    }


def _run_registries(detection, needed, steps, ran, execute: bool):
    brand_exhibit = None
    tld_exhibit = None
    if needed["brand"]:
        if execute:
            started = time.perf_counter()
            brand_exhibit = detector.brand_lookup(detection)
            ran["brand"] = True
            steps.append(_step("Brand registry", str(brand_exhibit["text"]), _ms(started), "done"))
        else:
            steps.append(_step("Brand registry", "Required for this score, and not run in this mode.", 0.0, "gap"))
    else:
        steps.append(_step("Brand registry", "The score does not call for the brand registry.", 0.0, "skip"))
    if needed["tld"]:
        if execute:
            started = time.perf_counter()
            tld_exhibit = detector.tld_lookup(detection)
            ran["tld"] = True
            steps.append(_step("Suffix registry", str(tld_exhibit["text"]), _ms(started), "done"))
        else:
            steps.append(_step("Suffix registry", "Required for this score, and not run in this mode.", 0.0, "gap"))
    else:
        steps.append(_step("Suffix registry", "The score does not call for the suffix registry.", 0.0, "skip"))
    return brand_exhibit, tld_exhibit, steps, ran


def _skipped_registries(needed) -> list[dict[str, object]]:
    rows = []
    if needed["brand"]:
        rows.append(_step("Brand registry", "Required for this score, and not run in this mode.", 0.0, "gap"))
    else:
        rows.append(_step("Brand registry", "The score does not call for the brand registry.", 0.0, "skip"))
    if needed["tld"]:
        rows.append(_step("Suffix registry", "Required for this score, and not run in this mode.", 0.0, "gap"))
    else:
        rows.append(_step("Suffix registry", "The score does not call for the suffix registry.", 0.0, "skip"))
    return rows


def _needed(detection: dict[str, object]) -> dict[str, bool]:
    score = int(detection["score"])
    return {
        "signal": True,
        "kb": True,
        "per_indicator": bool(detection["indicators"]),
        "legitimacy": score < 21,
        "brand": detection["path"] == "deep" or bool(detection["brand_tokens"]),
        "tld": detection["path"] == "deep" or bool(detection["suspicious_tld"]),
        "verify": True,
        "supported_only": True,
        "recommendation": True,
    }


def _indicator_claims(indicators, docs, brand, tld, force_all: bool = False) -> list[dict[str, object]]:
    claims = []
    for indicator in indicators:
        citations = []
        pool = list(docs)
        if brand:
            pool.append(brand)
        if tld:
            pool.append(tld)
        seen = set()
        for doc in pool:
            if doc["id"] in seen:
                continue
            if force_all or indicator["id"] in doc["tags"]:
                seen.add(doc["id"])
                citations.append(_cite(doc, str(indicator["id"])))
        claims.append(
            {
                "rule_id": indicator["id"],
                "text": indicator["text"],
                "weight": indicator["weight"],
                "label": indicator["label"],
                "citations": citations,
            }
        )
    return claims


def _legitimacy_claim(detection, docs) -> dict[str, object]:
    if detection["indicators"]:
        text = (
            "The score stays in the low band after the weights above. "
            "A low signal does not show that the page is safe to trust with a password."
        )
    else:
        text = (
            "No weighted indicator fired. "
            "A low signal does not show that the page is safe to trust with a password."
        )
    return {
        "rule_id": "legitimacy",
        "text": text,
        "weight": 0,
        "label": "Low score",
        "citations": [_cite(doc, "legitimacy") for doc in docs if "legitimacy" in doc["tags"]],
    }


def _verify_agentic(claims: list[dict[str, object]]) -> None:
    for claim in claims:
        matched = [citation for citation in claim["citations"] if citation["matched"]]
        if matched:
            claim["citations"] = matched
            claim["verdict"] = "supported"
            claim["published"] = True
            claim["badge"] = "Exhibit matches"
        else:
            claim["verdict"] = "unsupported"
            claim["published"] = False
            claim["badge"] = "Withheld"


def _verify_open(claims: list[dict[str, object]]) -> None:
    for claim in claims:
        matched = any(citation["matched"] for citation in claim["citations"])
        claim["verdict"] = "supported" if matched else "unsupported"
        claim["published"] = True
        claim["badge"] = "Exhibit matches" if matched else "No matching exhibit"


def _cite(doc: dict[str, object], rule_id: str) -> dict[str, object]:
    tags = list(doc["tags"])
    return {
        "id": doc["id"],
        "title": doc["title"],
        "text": doc["text"],
        "source": doc["source"],
        "tags": tags,
        "matched": rule_id in tags,
        "letter": "",
    }


def _checklist(needed: dict[str, bool], ran: dict[str, bool]) -> list[dict[str, object]]:
    labels = [
        ("signal", "Rule signal recorded"),
        ("kb", "Knowledge base searched"),
        ("per_indicator", "Each fired indicator retrieved by its own tag"),
        ("legitimacy", "Low-score exhibit retrieved"),
        ("brand", "Brand registry consulted"),
        ("tld", "Suffix registry consulted"),
        ("verify", "Verifier ran separately from the report"),
        ("supported_only", "Report writer published verifier output only"),
        ("recommendation", "Protective recommendation included"),
    ]
    rows = []
    for key, label in labels:
        required = needed[key]
        done = ran.get(key, False) and required
        if not required:
            state, state_label = "skip", "Not required"
            done = False
        elif ran.get(key, False):
            state, state_label = "done", "Done"
            done = True
        else:
            state, state_label = "gap", "Not run"
            done = False
        rows.append(
            {"key": key, "label": label, "required": required, "done": done, "state": state, "state_label": state_label}
        )
    return rows


def _query_terms(detection: dict[str, object]) -> set[str]:
    blob = " ".join(
        [
            str(detection["host"]),
            str(detection["path"]),
            str(detection["query"]),
        ]
    )
    return retrieval.tokenize(blob)


def _retrieve_detail(detection, docs) -> str:
    ids = ", ".join(str(indicator["id"]) for indicator in detection["indicators"]) or "none"
    return f"Tag retrieval for indicators: {ids}. Exhibits gathered: {len(docs)}."


def _summary(detection, published, withheld, mode: str) -> str:
    headline = str(detection["verdict"]["headline"])
    if mode == "agentic":
        return (
            f"{headline} {len(published)} reasons are published with a covering exhibit. "
            f"{len(withheld)} candidate sentences were withheld."
        )
    if mode == "retrieval":
        return f"{headline} The reasons below come from one retrieval pass, and some may lack a covering exhibit."
    return f"{headline} The reasons below are the URL cues, without exhibits."


def _recommendations(code: str) -> list[str]:
    if code == "phishing":
        return [
            "Do not enter a password, a one-time code, or payment details on this URL.",
            "Do not download files from this URL.",
            "Close the page.",
            "If credentials were already submitted, change them from a bookmark or a typed official address on a device you trust.",
            "Give this docket to your organization's security contact.",
        ]
    if code == "suspicious":
        return [
            "Do not type a password or a one-time code until you recognize the registrable domain.",
            "Open the service from a bookmark if the page is asking for secrets.",
            "Share this docket with a security contact if the link arrived in an unexpected message.",
        ]
    return [
        "If this page asks for a password, use a bookmark or type the official address.",
        "Read the published exhibits before treating the low score as a reason to trust the page.",
    ]


def _anatomy(detection: dict[str, object]) -> list[list[str]]:
    rows: list[list[str]] = []
    if detection["input"] != detection["url"]:
        rows.append(["Submitted", str(detection["input"])])
    rows.append(["Read as", str(detection["url"])])
    scheme = str(detection["scheme"])
    if detection["scheme_assumed"]:
        scheme += " (scheme was missing)"
    rows.append(["Scheme", scheme])
    rows.append(["Host", str(detection["host"])])
    if detection["host_display"] != detection["host"]:
        rows.append(["Decoded host", str(detection["host_display"])])
    rows.append(["Registrable domain", str(detection["registrable_domain"])])
    rows.append(["Public suffix", f".{detection['tld']}" if detection["tld"] else "None"])
    if detection["port"]:
        rows.append(["Port", str(detection["port"])])
    rows.append(["Path", str(detection["path"] or "/")])
    if detection["query"]:
        rows.append(["Query", str(detection["query"])])
    return rows


def _pills(detection: dict[str, object]) -> list[str]:
    features = detection["features"]
    pills = [
        f"{features['url_length']} characters",
        f"{features['num_dots']} dots",
        f"{features['num_hyphens']} hyphens",
        f"{features['num_subdomains']} extra labels",
        f"{features['lure_count']} lure words",
    ]
    if features["has_ip"]:
        pills.append("IP host")
    if features["has_at"]:
        pills.append("userinfo")
    if features["has_https"]:
        pills.append("https")
    if features["suspicious_tld"]:
        pills.append("listed suffix")
    if features["brand_mismatch"]:
        pills.append("brand mismatch")
    if features["quoted_printable"]:
        pills.append("email encoding")
    if features["punycode"]:
        pills.append("punycode")
    if features["shortener"]:
        pills.append("shortener")
    if features["num_encodings"]:
        pills.append(f"{features['num_encodings']} encodings")
    return pills


def _assign_letters(exhibits: list[dict[str, object]]) -> None:
    seen = set()
    letter_index = 0
    unique = []
    for exhibit in exhibits:
        if exhibit["id"] in seen:
            continue
        seen.add(exhibit["id"])
        exhibit["letter"] = chr(ord("A") + letter_index) if letter_index < 26 else str(letter_index + 1)
        letter_index += 1
        unique.append(exhibit)
    exhibits[:] = unique


def _comparison_rows(modes: dict[str, dict[str, object]]) -> list[dict[str, str]]:
    def grab(label: str, picker) -> dict[str, str]:
        return {
            "label": label,
            "rules": picker(modes["rules"]),
            "retrieval": picker(modes["retrieval"]),
            "agentic": picker(modes["agentic"]),
        }

    return [
        grab("Risk score", lambda report: str(report["detection"]["score"])),
        grab("Path", lambda report: str(report["detection"]["path_label"])),
        grab("Unsupported-claim rate", lambda report: report["metrics"]["unsupported_label"]),
        grab("Support in published findings", lambda report: report["metrics"]["support_label"]),
        grab("Investigation completeness", lambda report: report["metrics"]["completeness_label"]),
        grab("Published sentences", lambda report: str(report["metrics"]["published_claims"])),
        grab("Withheld sentences", lambda report: str(report["metrics"]["withheld_claims"])),
        grab("Exhibits", lambda report: str(report["metrics"]["exhibit_count"])),
        grab("Retrieval time", lambda report: report["metrics"]["retrieval_label"]),
        grab("Chain time", lambda report: report["metrics"]["agent_label"]),
    ]


def _step(name: str, detail: str, elapsed: float, state: str) -> dict[str, object]:
    labels = {"done": "Done", "gap": "Not run", "skip": "Not required"}
    return {
        "name": name,
        "detail": detail,
        "ms": elapsed,
        "ms_label": _fmt_ms(elapsed) if state == "done" else "—",
        "state": state,
        "state_label": labels[state],
    }


def _ms(started: float) -> float:
    return (time.perf_counter() - started) * 1000


def _pct(value: float | None) -> str:
    if value is None:
        return "—"
    percent = value * 100
    if abs(percent - round(percent)) < 0.05:
        return f"{percent:.0f}%"
    return f"{percent:.1f}%"


def _fmt_ms(value: float) -> str:
    if value < 0.01:
        return "<0.01 ms"
    return f"{value:.2f} ms"
