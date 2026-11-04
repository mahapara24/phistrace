"""Checks the investigation chain without starting the server."""

from __future__ import annotations

import json

from app import agents
from app.detector import analyze


def _ids(url: str) -> set[str]:
    return {item["id"] for item in analyze(url)["indicators"]}


def _mode(url: str, mode: str) -> dict:
    return agents.investigate(url, mode)["primary"] if mode != "compare" else agents.investigate(url, mode)


def main() -> None:
    google = analyze("https://www.google.com")
    assert google["score"] == 0, google["score"]
    assert google["verdict"]["code"] == "clean"
    assert google["path"] == "light"
    assert "brand_mismatch" not in _ids("https://www.google.com")

    paypal = analyze("https://www.paypal.com/signin")
    assert paypal["score"] < 21, paypal
    assert paypal["verdict"]["code"] == "clean"
    assert "brand_mismatch" not in _ids("https://www.paypal.com/signin")
    assert paypal["official_brands"], paypal["official_brands"]

    real_cmd = analyze("https://www.paypal.com/cgi-bin/webscr?cmd=_login-run")
    assert real_cmd["verdict"]["code"] == "clean", real_cmd["verdict"]
    assert "quoted_printable" not in _ids("https://www.paypal.com/cgi-bin/webscr?cmd=_login-run")
    assert "quoted_printable" not in _ids("https://www.paypal.com/signin?x=%3Dabc")

    mailed = analyze("https://www.paypal.com/cgi-bin/webscr?cmd=3D_login-run")
    assert mailed["verdict"]["code"] == "phishing", mailed["verdict"]
    assert "quoted_printable" in _ids("https://www.paypal.com/cgi-bin/webscr?cmd=3D_login-run")
    assert mailed["official_brands"]
    assert any("=3D" in line for line in mailed["verdict"]["why"])

    buried_path = analyze("http://shop.example/www.paypal.com/cgi-bin/webscr?cmd=_login-run")
    assert buried_path["verdict"]["code"] == "phishing"
    assert "brand_mismatch" in _ids("http://shop.example/www.paypal.com/cgi-bin/webscr?cmd=_login-run")
    assert buried_path["registrable_domain"] == "shop.example"

    microsoft = analyze("https://login.microsoftonline.com")
    assert microsoft["score"] < 21, microsoft
    assert "brand_mismatch" not in _ids("https://login.microsoftonline.com")
    assert microsoft["official_brands"]

    look = analyze("http://paypa1-secure-login.tk/verify/account")
    assert look["verdict"]["code"] == "phishing"
    assert look["verdict"]["why"]
    look_ids = {item["id"] for item in look["indicators"]}
    assert {"brand_mismatch", "suspicious_tld", "lure_terms", "no_https"} <= look_ids, look_ids
    assert look["score"] >= 50

    buried = analyze("http://linkedin.com.evil.tk/login")
    assert "brand_mismatch" in _ids("http://linkedin.com.evil.tk/login")
    assert buried["registrable_domain"] == "evil.tk"

    trick = analyze("http://paypal.com@evil.example/login")
    trick_ids = _ids("http://paypal.com@evil.example/login")
    assert "userinfo_at" in trick_ids and "brand_mismatch" in trick_ids
    assert trick["host"] == "evil.example"

    ip_url = analyze("http://192.0.2.10/banking/login")
    assert ip_url["features"]["has_ip"] == 1
    assert ip_url["score"] >= 50
    assert ip_url["score"] <= 100

    short = analyze("https://bit.ly/3example")
    assert "shortener" in _ids("https://bit.ly/3example")
    assert short["verdict"]["code"] == "suspicious"
    assert short["path"] == "standard"
    plain = analyze("http://example.com")
    assert plain["verdict"]["code"] == "clean"

    amazon = analyze("https://amaz0n-billing.xyz/secure/update")
    assert "brand_mismatch" in _ids("https://amaz0n-billing.xyz/secure/update")
    assert "suspicious_tld" in _ids("https://amaz0n-billing.xyz/secure/update")

    puny = analyze("http://xn--pypal-4ve.com/update")
    assert "punycode" in _ids("http://xn--pypal-4ve.com/update")
    assert puny["score"] < 50

    for bad in ("", "javascript:alert(1)", "data:text/html,hi", "http://"):
        try:
            analyze(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"should reject {bad!r}")

    packed = "http://paypal.com@192.0.2.10:8080/" + "a" * 180 + "/%25%25%25%25/login/verify/secure/account"
    assert analyze(packed)["score"] <= 100

    compared = agents.investigate("http://paypa1-secure-login.tk/verify/account", "compare")
    modes = compared["modes"]
    assert modes["rules"]["detection"]["score"] == modes["agentic"]["detection"]["score"]
    assert modes["agentic"]["metrics"]["evidence_support"] == 1
    assert modes["agentic"]["metrics"]["unsupported_rate"] == 0
    assert modes["retrieval"]["metrics"]["evidence_support"] == 0.5, json.dumps(
        [
            {
                "text": claim["text"],
                "verdict": claim["verdict"],
                "cites": [cite["id"] for cite in claim["citations"]],
            }
            for claim in modes["retrieval"]["claims"]
        ],
        indent=2,
    )
    assert modes["retrieval"]["metrics"]["unsupported_rate"] == 0.5
    assert modes["rules"]["metrics"]["evidence_support"] == 0
    assert modes["rules"]["metrics"]["unsupported_rate"] == 1
    assert (
        modes["agentic"]["metrics"]["completeness"]
        > modes["retrieval"]["metrics"]["completeness"]
        > modes["rules"]["metrics"]["completeness"]
    )
    assert modes["agentic"]["metrics"]["completeness"] == 1

    calm = agents.investigate("https://www.google.com", "compare")["modes"]
    assert calm["agentic"]["metrics"]["unsupported_rate"] == 0
    assert calm["agentic"]["metrics"]["evidence_support"] == 1
    assert calm["rules"]["metrics"]["unsupported_rate"] == 1
    assert calm["agentic"]["detection"]["score"] == 0

    try:
        agents.investigate("https://www.google.com", "nope")
    except ValueError:
        pass
    else:
        raise AssertionError("bad mode should fail")

    print("selftest ok")
    print(
        "lookalike",
        modes["agentic"]["detection"]["score"],
        modes["rules"]["metrics"]["completeness_label"],
        modes["retrieval"]["metrics"]["completeness_label"],
        modes["agentic"]["metrics"]["completeness_label"],
    )


if __name__ == "__main__":
    main()
