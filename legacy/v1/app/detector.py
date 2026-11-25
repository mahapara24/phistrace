"""Transparent URL rules. This module does not train or load a model."""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import unquote, urlparse

from app.corpus import (
    BRANDS,
    LURE_WORDS,
    MULTI_SUFFIXES,
    SHORTENERS,
    SUSPICIOUS_TLDS,
    brand_name,
)

W_RAW_IP = 32
W_USERINFO = 26
W_BRAND = 28
W_TLD = 16
W_PUNY = 22
W_SHORT = 26
W_HTTP = 8
W_LONG = 10
W_VERY_LONG = 8
W_SUB = 12
W_HYPHEN = 8
W_PORT = 18
W_ENCODE = 8
W_DIGIT = 8
W_SLASH = 10
W_LURE = 6
W_QP = 28
LURE_CAP = 18
LURE_CAP_OFFICIAL = 6

LONG_AT = 90
VERY_LONG_AT = 140
SUB_AT = 3
HYPHEN_AT = 3
ENCODE_AT = 4
DIGIT_RATIO = 0.30
DIGIT_MIN = 8
PREFIX_EXTRA = 12
SUFFIX_EXTRA = 2

LEVEL_MODERATE = 21
PATH_DEEP = 50
LEVEL_CRITICAL = 75
SCORE_CAP = 100

_LEET = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t"})
_HEX = re.compile(r"%[0-9a-fA-F]{2}")
_SPLIT = re.compile(r"[^a-z0-9]+")
_QUOTED_PRINTABLE = re.compile(r"=3[Dd]")


def catalog() -> list[dict[str, str]]:
    return [
        {"id": "raw_ip", "label": "Raw IP host", "weight": str(W_RAW_IP), "detail": "The host is an IPv4 or IPv6 address."},
        {"id": "userinfo_at", "label": "User information", "weight": str(W_USERINFO), "detail": "Text before @ is not the host. The connection target is the host after @."},
        {"id": "brand_mismatch", "label": "Brand mismatch", "weight": str(W_BRAND), "detail": "A brand-like token is present, and the registrable domain is not on that brand's list."},
        {"id": "suspicious_tld", "label": "Higher-abuse suffix", "weight": str(W_TLD), "detail": "The public suffix is on this workbench's higher-abuse list."},
        {"id": "punycode", "label": "Punycode label", "weight": str(W_PUNY), "detail": "A host label begins with xn--."},
        {"id": "shortener", "label": "Shortener", "weight": str(W_SHORT), "detail": "The registrable host is a known shortening service. Redirects are not followed."},
        {"id": "no_https", "label": "Explicit HTTP", "weight": str(W_HTTP), "detail": "The typed URL uses http. A missing scheme does not add this weight."},
        {"id": "long_url", "label": "Long URL", "weight": str(W_LONG), "detail": f"The URL is at least {LONG_AT} characters."},
        {"id": "very_long_url", "label": "Very long URL", "weight": str(W_VERY_LONG), "detail": f"The URL is at least {VERY_LONG_AT} characters. This adds to the long-URL weight."},
        {"id": "deep_subdomains", "label": "Deep subdomains", "weight": str(W_SUB), "detail": f"At least {SUB_AT} labels sit left of the registrable domain."},
        {"id": "many_hyphens", "label": "Many hyphens", "weight": str(W_HYPHEN), "detail": f"The host contains at least {HYPHEN_AT} hyphens."},
        {"id": "unusual_port", "label": "Unusual port", "weight": str(W_PORT), "detail": "The port is present and is not 80 or 443."},
        {"id": "heavy_encoding", "label": "Heavy encoding", "weight": str(W_ENCODE), "detail": f"The URL contains at least {ENCODE_AT} percent-encodings."},
        {"id": "digit_heavy_host", "label": "Digit-heavy host", "weight": str(W_DIGIT), "detail": "Digits are at least 30 percent of the host's letters and digits, and the host is not an IP."},
        {"id": "double_slash_path", "label": "Double slash in the path", "weight": str(W_SLASH), "detail": "The path contains //."},
        {
            "id": "lure_terms",
            "label": "Lure words",
            "weight": f"{W_LURE} each, cap {LURE_CAP}",
            "detail": f"Credential and account words in the host, path, or query. Cap {LURE_CAP_OFFICIAL} when the registrable domain is a listed brand domain.",
        },
        {
            "id": "quoted_printable",
            "label": "Email encoding leftover",
            "weight": str(W_QP),
            "detail": "The URL still contains =3D, the way email encodes an equals sign. cmd=3D_login-run is the raw form of cmd=_login-run. Percent-encoding (%3D) does not count.",
        },
    ]


def analyze(raw: str) -> dict[str, object]:
    original, normalized, parts, assumed = _prepare(raw)
    host = parts.hostname or ""
    if host.endswith("."):
        host = host[:-1]
    try:
        port = parts.port
    except ValueError as exc:
        raise ValueError("The port is not valid.") from exc

    decoded_path = unquote(parts.path or "")
    decoded_query = unquote(parts.query or "")
    registrable = registrable_domain(host)
    tld = public_suffix(host)
    ip_host = is_ip(host)
    display = display_host(host)

    host_brands = _matched_brands(host)
    user_brands = _matched_brands(parts.username or "")
    brand_tokens = [{**item, "where": "host"} for item in host_brands] + [
        {**item, "where": "userinfo"} for item in user_brands
    ]

    mismatches = []
    officials = []
    seen_mismatch = set()
    seen_official = set()
    for token in brand_tokens:
        key = token["brand"]
        listed = registrable in BRANDS[key]
        record = {
            "brand": key,
            "name": brand_name(key),
            "piece": token["piece"],
            "where": token["where"],
            "domain": registrable,
        }
        if listed and token["where"] == "host":
            if key not in seen_official:
                officials.append(record)
                seen_official.add(key)
        elif not listed and key not in seen_mismatch:
            mismatches.append(record)
            seen_mismatch.add(key)

    for item in _brand_domains_in_path(decoded_path, registrable):
        brand_tokens.append({"brand": item["brand"], "piece": item["piece"], "where": "path"})
        if item["brand"] not in seen_mismatch and item["brand"] not in seen_official:
            mismatches.append(item)
            seen_mismatch.add(item["brand"])

    lure_hits = _lure_hits(host, decoded_path, decoded_query)
    official_host = bool(officials) and not mismatches
    indicators: list[dict[str, object]] = []

    def add(rule_id: str, weight: int, text: str) -> None:
        label = next(row["label"] for row in catalog() if row["id"] == rule_id)
        indicators.append({"id": rule_id, "label": label, "weight": weight, "text": text})

    if ip_host:
        add("raw_ip", W_RAW_IP, f"The host {host} is an IP address, so there is no domain name to compare.")
    if parts.username or parts.password is not None:
        shown = parts.username or "(empty)"
        add("userinfo_at", W_USERINFO, f"User information “{shown}” sits before @. The host that follows @ is {host}.")
    if mismatches:
        bits = [
            f"{item['name']}-like “{item['piece']}” in the {item['where']}"
            for item in mismatches
        ]
        add(
            "brand_mismatch",
            W_BRAND,
            f"{'; '.join(bits)}. The registrable domain {registrable} is not on the matching brand list.",
        )
    if tld in SUSPICIOUS_TLDS:
        add("suspicious_tld", W_TLD, f"The public suffix .{tld} is on this workbench's higher-abuse list.")
    if any(label.startswith("xn--") for label in host.split(".")):
        add("punycode", W_PUNY, f"The host {host} contains a Punycode label (xn--).")
    if (not ip_host) and (registrable in SHORTENERS or host in SHORTENERS):
        add("shortener", W_SHORT, f"{registrable} is a shortening host. The destination is not in the URL, and this workbench does not follow it.")
    if parts.scheme == "http" and not assumed:
        add("no_https", W_HTTP, "The URL explicitly uses http.")
    length = len(normalized)
    if length >= LONG_AT:
        add("long_url", W_LONG, f"The URL is {length} characters, which is at least {LONG_AT}.")
    if length >= VERY_LONG_AT:
        add("very_long_url", W_VERY_LONG, f"The URL is {length} characters, which is at least {VERY_LONG_AT}.")
    sub_count = subdomain_count(host)
    if sub_count >= SUB_AT:
        add("deep_subdomains", W_SUB, f"The host has {sub_count} labels to the left of {registrable}.")
    hyphens = host.count("-")
    if hyphens >= HYPHEN_AT:
        add("many_hyphens", W_HYPHEN, f"The host contains {hyphens} hyphens.")
    if port not in (None, 80, 443):
        add("unusual_port", W_PORT, f"The URL names port {port}, which is not 80 or 443.")
    encodings = len(_HEX.findall(original if not assumed else normalized))
    if encodings >= ENCODE_AT:
        add("heavy_encoding", W_ENCODE, f"The URL contains {encodings} percent-encodings.")
    digit_ratio = _digit_ratio(host)
    if (not ip_host) and digit_ratio is not None and digit_ratio >= DIGIT_RATIO:
        add("digit_heavy_host", W_DIGIT, f"Digits are {digit_ratio:.0%} of the letters and digits in the host.")
    if "//" in (parts.path or ""):
        add("double_slash_path", W_SLASH, "The path contains a double slash.")
    if lure_hits:
        cap = LURE_CAP_OFFICIAL if official_host else LURE_CAP
        weight = min(cap, W_LURE * len(lure_hits))
        words = ", ".join(lure_hits)
        extra = " The domain is on a brand list, so this weight is capped." if official_host else ""
        add("lure_terms", weight, f"The URL contains the lure words {words}.{extra}")
    if _QUOTED_PRINTABLE.search(f"{original}\n{decoded_path}\n{decoded_query}"):
        listed = ""
        if official_host:
            names = ", ".join(str(item["name"]) for item in officials)
            listed = f" The host is on the local list for {names}, so this is not a lookalike domain."
        add(
            "quoted_printable",
            W_QP,
            "The URL contains =3D. Email encodes an equals sign as =3D, so cmd=3D_login-run is the raw form of cmd=_login-run. Phishing messages copy that login command."
            + listed,
        )

    raw_score = sum(int(item["weight"]) for item in indicators)
    score = min(SCORE_CAP, raw_score)
    level = _level(score)
    path = _path(score)

    notes: list[str] = []
    if assumed:
        notes.append("No scheme was typed. It was not counted as HTTP. Include https:// or http:// when you know the scheme.")
    for item in officials:
        notes.append(f"{item['domain']} is on the local list for {item['name']}.")
    if display != host:
        notes.append(f"The Punycode host decodes for display as {display}.")

    features = {
        "url_length": length,
        "num_dots": host.count("."),
        "num_hyphens": hyphens,
        "num_digits": sum(character.isdigit() for character in host),
        "num_subdomains": sub_count,
        "num_params": len(parts.query.split("&")) if parts.query else 0,
        "num_encodings": encodings,
        "has_ip": int(ip_host),
        "has_at": int(bool(parts.username) or parts.password is not None),
        "has_https": int(parts.scheme == "https"),
        "scheme_assumed": int(assumed),
        "suspicious_tld": int(tld in SUSPICIOUS_TLDS),
        "lure_count": len(lure_hits),
        "quoted_printable": int(bool(_QUOTED_PRINTABLE.search(f"{original}\n{decoded_path}\n{decoded_query}"))),
        "brand_mismatch": int(bool(mismatches)),
        "punycode": int(any(label.startswith("xn--") for label in host.split("."))),
        "shortener": int((not ip_host) and (registrable in SHORTENERS or host in SHORTENERS)),
        "unusual_port": int(port not in (None, 80, 443)),
    }

    result = {
        "input": original,
        "url": normalized,
        "scheme": parts.scheme,
        "scheme_assumed": assumed,
        "host": host,
        "host_display": display,
        "registrable_domain": registrable,
        "tld": tld,
        "path": parts.path or "/",
        "query": parts.query,
        "port": port,
        "is_ip": ip_host,
        "brand_tokens": [
            {"brand": token["brand"], "name": brand_name(token["brand"]), "piece": token["piece"], "where": token["where"]}
            for token in brand_tokens
        ],
        "brand_mismatches": mismatches,
        "official_brands": officials,
        "suspicious_tld": tld in SUSPICIOUS_TLDS,
        "score": score,
        "raw_score": raw_score,
        "level": level,
        "level_label": level.capitalize() if level != "critical" else "Critical",
        "path": path,
        "path_label": {"light": "Light", "standard": "Standard", "deep": "Deep"}[path],
        "path_reason": _path_reason(score, path, bool(brand_tokens), tld in SUSPICIOUS_TLDS),
        "indicators": indicators,
        "notes": notes,
        "features": features,
        "lure_hits": lure_hits,
    }
    result["verdict"] = decide(result)
    return result


def decide(detection: dict[str, object]) -> dict[str, object]:
    """Turn fired indicators into a phishing / suspicious / not-phishing call."""
    ids = {str(item["id"]) for item in detection["indicators"]}
    official = bool(detection["official_brands"]) and not detection["brand_mismatches"]
    reasons = [str(item["text"]) for item in detection["indicators"]]
    phishing = (
        "brand_mismatch" in ids
        or "userinfo_at" in ids
        or "punycode" in ids
        or ("raw_ip" in ids and "lure_terms" in ids)
        or ("suspicious_tld" in ids and "lure_terms" in ids)
        or ("shortener" in ids and "lure_terms" in ids)
        or ("quoted_printable" in ids and "lure_terms" in ids)
        or int(detection["score"]) >= 50
    )
    weak_only = ids <= {"no_https"} or (official and ids <= {"lure_terms", "no_https"})
    suspicious = (not phishing) and bool(ids) and not weak_only
    if phishing:
        code, label = "phishing", "Phishing / scam"
        headline = "This URL is identified as phishing or a scam from the address itself."
        why = reasons or ["The combined rule score is 50 or higher."]
    elif suspicious:
        code, label = "suspicious", "Suspicious"
        headline = "This URL has phishing cues. They are not strong enough, on their own, to call it phishing."
        why = reasons
    else:
        code, label = "clean", "Not phishing"
        headline = "This URL is not identified as phishing. The page itself was not opened."
        why = []
        if official:
            why.extend(str(note) for note in detection["notes"] if "local list" in str(note))
            if "lure_terms" in ids:
                why.append("Account words appear in the URL, and on a listed domain those words are expected.")
        if "no_https" in ids:
            why.append("The URL uses plain HTTP. That cue alone is not treated as phishing.")
        if not why:
            why.append("No lookalike brand, risky suffix, address trick, or credential lure fired.")
    return {"code": code, "label": label, "headline": headline, "why": why}


def brand_lookup(detection: dict[str, object]) -> dict[str, object]:
    mismatches = detection["brand_mismatches"]
    officials = detection["official_brands"]
    if mismatches:
        lines = [
            f"{item['name']}-like token “{item['piece']}” ({item['where']}) is not paired with a listed {item['name']} domain. Registrable domain: {item['domain']}."
            for item in mismatches
        ]
        return _tool(
            "tool-brand",
            "Brand registry",
            " ".join(lines),
            ["brand_mismatch", "brand_registry"],
            "Local brand registry",
        )
    if officials:
        lines = [f"{item['domain']} is listed for {item['name']}." for item in officials]
        return _tool(
            "tool-brand",
            "Brand registry",
            " ".join(lines),
            ["official_brand", "brand_registry"],
            "Local brand registry",
        )
    return _tool(
        "tool-brand",
        "Brand registry",
        "No listed brand token appears in the host or the user information.",
        ["brand_registry"],
        "Local brand registry",
    )


def tld_lookup(detection: dict[str, object]) -> dict[str, object]:
    if detection["is_ip"]:
        return _tool(
            "tool-tld",
            "Suffix registry",
            f"The host {detection['host']} is an IP address, so it has no public suffix.",
            ["raw_ip", "tld_registry"],
            "Local suffix registry",
        )
    tld = str(detection["tld"] or "")
    if tld in SUSPICIOUS_TLDS:
        return _tool(
            "tool-tld",
            "Suffix registry",
            f".{tld} is on the higher-abuse list. A suffix alone is one exhibit, not a finished finding.",
            ["suspicious_tld", "tld_registry"],
            "Local suffix registry",
        )
    shown = f".{tld}" if tld else "the suffix"
    return _tool(
        "tool-tld",
        "Suffix registry",
        f"{shown} is not on the higher-abuse list in this workbench.",
        ["tld_registry"],
        "Local suffix registry",
    )


def is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return False
    return True


def registrable_domain(host: str) -> str:
    if is_ip(host):
        return host
    labels = [label for label in host.split(".") if label]
    if len(labels) <= 2:
        return ".".join(labels)
    last_two = ".".join(labels[-2:])
    if last_two in MULTI_SUFFIXES and len(labels) >= 3:
        return ".".join(labels[-3:])
    return last_two


def public_suffix(host: str) -> str:
    if is_ip(host):
        return ""
    labels = [label for label in host.split(".") if label]
    if len(labels) >= 2 and ".".join(labels[-2:]) in MULTI_SUFFIXES:
        return ".".join(labels[-2:])
    return labels[-1] if labels else ""


def subdomain_count(host: str) -> int:
    if is_ip(host):
        return 0
    labels = [label for label in host.split(".") if label]
    reg_labels = [label for label in registrable_domain(host).split(".") if label]
    return max(0, len(labels) - len(reg_labels))


def display_host(host: str) -> str:
    try:
        return host.encode("ascii").decode("idna")
    except (UnicodeError, UnicodeDecodeError):
        return host


def _prepare(raw: str) -> tuple[str, str, object, bool]:
    original = (raw or "").strip()
    if not original:
        raise ValueError("Enter a URL.")
    if len(original) > 2048:
        raise ValueError("The URL is longer than 2048 characters.")
    if any(character.isspace() for character in original):
        raise ValueError("Remove spaces from the URL.")
    lowered = original.lower()
    if lowered.startswith(("javascript:", "data:", "file:", "vbscript:", "about:")):
        raise ValueError("Only http and https URLs can be investigated.")
    assumed = "://" not in original
    normalized = f"http://{original}" if assumed else original
    parts = urlparse(normalized)
    if parts.scheme not in {"http", "https"}:
        raise ValueError("Only http and https URLs can be investigated.")
    if not parts.hostname:
        raise ValueError("That URL does not have a host.")
    return original, normalized, parts, assumed


def _matched_brands(value: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for piece in _SPLIT.split(value.lower()):
        if not piece:
            continue
        for brand in BRANDS:
            if mention(piece, brand):
                key = (brand, piece)
                if key in seen:
                    continue
                seen.add(key)
                found.append({"brand": brand, "piece": piece})
                break
    return found


def _brand_domains_in_path(path: str, registrable: str) -> list[dict[str, str]]:
    """A brand's own domain written in the path, while the host is a different registrable domain."""
    lowered = path.lower()
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    for brand, domains in BRANDS.items():
        if registrable in domains or brand in seen:
            continue
        for domain in domains:
            pattern = rf"(?<![a-z0-9]){re.escape(domain)}(?![a-z0-9])"
            if re.search(pattern, lowered):
                seen.add(brand)
                found.append(
                    {
                        "brand": brand,
                        "name": brand_name(brand),
                        "piece": domain,
                        "where": "path",
                        "domain": registrable,
                    }
                )
                break
    return found


def mention(piece: str, brand: str) -> bool:
    normalized = piece.lower().translate(_LEET)
    target = brand.lower().translate(_LEET)
    if len(target) < 3 or len(normalized) < 3:
        return False
    if normalized == target:
        return True
    extra = len(normalized) - len(target)
    if normalized.startswith(target) and 0 < extra <= PREFIX_EXTRA:
        return True
    if normalized.endswith(target) and 0 < extra <= SUFFIX_EXTRA:
        return True
    return False


def _lure_hits(host: str, path: str, query: str) -> list[str]:
    blob = f"{host} {path} {query}".lower()
    tokens = set(_SPLIT.split(blob))
    hits = [word for word in LURE_WORDS if word in tokens or ("-" in word and word in blob)]
    return hits


def _digit_ratio(host: str) -> float | None:
    digits = sum(character.isdigit() for character in host)
    letters = sum(character.isalpha() for character in host)
    total = digits + letters
    if total < DIGIT_MIN:
        return None
    return digits / total


def _level(score: int) -> str:
    if score >= LEVEL_CRITICAL:
        return "critical"
    if score >= PATH_DEEP:
        return "high"
    if score >= LEVEL_MODERATE:
        return "moderate"
    return "low"


def _path(score: int) -> str:
    if score >= PATH_DEEP:
        return "deep"
    if score >= LEVEL_MODERATE:
        return "standard"
    return "light"


def _path_reason(score: int, path: str, brand_token: bool, suspicious: bool) -> str:
    if path == "deep":
        base = f"The score is {score}, at least {PATH_DEEP}. The deep path opens the brand registry, the suffix registry, and one retrieval per fired indicator."
    elif path == "standard":
        base = f"The score is {score}, from {LEVEL_MODERATE} through {PATH_DEEP - 1}. The standard path retrieves one exhibit per fired indicator."
    else:
        base = f"The score is {score}, below {LEVEL_MODERATE}. The light path reads the low-score exhibit and retrieves any indicator that still fired."
    extras = []
    if brand_token and path != "deep":
        extras.append("A brand token is present, so the brand registry opens as well.")
    if suspicious and path != "deep":
        extras.append("The suffix is on the higher-abuse list, so the suffix registry opens as well.")
    return " ".join([base, *extras])


def _tool(tool_id: str, title: str, text: str, tags: list[str], source: str) -> dict[str, object]:
    return {"id": tool_id, "title": title, "text": text, "tags": tags, "source": source, "kind": "tool"}
