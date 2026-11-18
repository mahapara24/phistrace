# PhishTrace

Local investigation workbench for the paper *A Rule-Based Agentic Retrieval Framework for Phishing URL Detection and Evidence-Verified Investigation*.

The site reads a URL, scores it with 22 published weighted rules, retrieves local exhibits, verifies each finding against an exhibit, and writes a docket. It does not train a classifier, call a generative model, or open the page.

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

## Data

Raw files go in `data/raw/`, which is not committed. Download:

| File | Source |
|---|---|
| `data/raw/phiusiil.zip` | PhiUSIIL Phishing URL Dataset, UCI 967 (CC BY 4.0): https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset |
| `data/raw/openphish.txt` | OpenPhish community feed: https://openphish.com/feed.txt |
| `data/raw/phishing-links-active.txt` | Phishing.Database: https://github.com/Phishing-Database/Phishing.Database |
| `data/raw/phishing-ips-active.txt` | Phishing.Database (same repository) |
| `data/raw/urlhaus_filter_online.txt` | URLhaus malware URLs via the malware-filter mirror: https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-online.txt |
| `data/raw/tranco_top1m.csv` | Tranco top sites list: https://tranco-list.eu/ (latest list, top 1M) |

Rebuild the Data page summaries:

```bash
python scripts/build_phiusiil_summary.py
python scripts/build_public_summaries.py
```

## Evaluation

```bash
python scripts/evaluate.py
```

Every dataset is split by an MD5 hash of each URL or domain (30% development, 70% held-out test); rules were only inspected on development splits. The script writes `data/eval_results.json` with accuracy, precision, recall, F1, FPR, ROC-AUC, PR-AUC on PhiUSIIL; recall on OpenPhish, Phishing.Database, and URLhaus; false alarms on the Tranco top-100k; a pooled malicious-vs-safe score; and the three-mode comparison (unsupported-claim rate, evidence support, completeness, latency). `data/eval_baseline.json`, `data/eval_v2.json` and `data/eval_v3.json` hold the same numbers for the 17-rule (v1), 20-rule (v2) and 22-rule (v3) sets. The Method page shows all four.

The sensitive variant discussed in the paper (any single rule raises an alert) is written to its own file, so it does not overwrite the main results:

```bash
python scripts/evaluate.py --sensitive --out data/eval_v4_sensitive.json
```

Held-out test results (v4, alert point): PhiUSIIL accuracy 0.813, precision 0.998, recall 0.566, F1 0.722, FPR 0.075%, ROC-AUC 0.954. Pooled OpenPhish + Phishing.Database + URLhaus against Tranco top-100k: accuracy 0.923, precision 0.986, recall 0.802, F1 0.884, false alarms 0.65%. v4 keeps the 22 rules of v3 and widens their lists (hosting platforms, shorteners, brands); see the Method page.

Testing screenshots: [`screenshots/`](screenshots/README.md) holds full PhishTrace reports for 15 real phishing URLs plus the classroom example, 2 malware URLs, 5 safe sites, and one three-mode comparison, with a results table.

Limitation: every legitimate URL in PhiUSIIL and Tranco is a bare homepage, so false alarms on real deep links (sign-in pages, shared documents, software downloads) are not measured.

## Paper

```bash
python3 paper/make_figures.py
python3 paper/build_paper.py path/to/conference-template-a4.docx
```

This writes `paper/Mahapara_PhishTrace_IEEE.docx` in the IEEE A4 conference template, with every number read from the evaluation files.

The PDF and ODT copies in `paper/` are converted from that DOCX with LibreOffice:

```bash
soffice --headless --convert-to pdf --outdir paper paper/Mahapara_PhishTrace_IEEE.docx
soffice --headless --convert-to odt --outdir paper paper/Mahapara_PhishTrace_IEEE.docx
```

| File | Format |
|---|---|
| `paper/Mahapara_PhishTrace_IEEE.docx` | Word |
| `paper/Mahapara_PhishTrace_IEEE.odt` | OpenDocument Text |
| `paper/Mahapara_PhishTrace_IEEE.pdf` | PDF |
