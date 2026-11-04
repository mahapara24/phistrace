# PhishTrace

Local investigation workbench for the proposal *An Agentic Retrieval-Augmented Framework for Proactive Phishing Detection and Investigation*.

The site reads a URL, scores it with published rules, retrieves local exhibits, and writes a docket. It does not train a classifier, call a generative model, or open the page.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:8000

Check the chain without the server:

```bash
python -m app.selftest
```

## Modes

- **Rules only** — signal and class label, no exhibits.
- **Retrieval only** — one search, citations not checked against tags.
- **Agentic chain** — the score chooses registries; each indicator is retrieved by tag; the verifier withholds uncovered sentences.
- **Compare** — all three, on the same signal.

The classroom lookalike `http://paypa1-secure-login.tk/verify/account` is the comparison to open first.

The data page uses the public PhiUSIIL Phishing URL Dataset (UCI 967, CC BY 4.0): phishing and legitimate URLs from Prasad and Chandra. The raw zip stays in `data/raw/` and is not committed. Rebuild the page summary with:

```bash
python scripts/build_phiusiil_summary.py
```
