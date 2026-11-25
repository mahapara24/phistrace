"""Build the blinded sentence audit: 40 URLs, PhishTrace and LLM-RAG sentences mixed.

Two raters fill in one workbook each without seeing the other or the key.
  python scripts/make_audit.py             # writes audit/rater_A.xlsx, rater_B.xlsx, key.json
  python scripts/make_audit.py --score     # after both raters finish
Needs openpyxl (analysis only).
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from openpyxl import Workbook, load_workbook  # noqa: E402
from openpyxl.styles import Alignment, Font  # noqa: E402
from openpyxl.worksheet.datavalidation import DataValidation  # noqa: E402

from app import agents  # noqa: E402
from app.corpus import by_id  # noqa: E402

AUDIT = ROOT / "audit"
URLS = 40
LABELS = ("supported", "partly", "not supported")
GUIDE = [
    "You see a URL, one sentence from a report about it, and the evidence cited for that sentence.",
    "Choose one label per row, using ONLY the URL text and the evidence shown. Do not open the URL.",
    "supported: the URL and the evidence together show that the whole sentence is true.",
    "partly: some of the sentence is shown, but another part is not.",
    "not supported: the sentence is wrong, or the evidence is about something else, or no evidence is given.",
    "Links are written as hxxp:// or hxxps:// so that nobody opens them by accident. Read them as http:// and https://.",
    "Work alone. Do not talk about the rows with the other rater until both are finished.",
]


def items() -> list[dict]:
    out = []
    lines = (ROOT / "data" / "llm_rag_reports.jsonl").read_text(encoding="utf-8").splitlines()[:URLS]
    for line in lines:
        record = json.loads(line)
        report = agents.investigate(record["url"], "agentic")["primary"]
        for claim in report["published"]:
            out.append({"system": "PhishTrace", "url": record["url"], "sentence": claim["text"], "evidence": "\n".join(f"{c['title']}. {c['text']}" for c in claim["citations"])})
        for part in record["report"]:
            docs = [by_id(i) for i in part["exhibits"]]
            out.append({"system": "LLM-RAG", "url": record["url"], "sentence": part["sentence"], "evidence": "\n".join(f"{d['title']}. {d['text']}" for d in docs if d)})
    random.Random(967).shuffle(out)
    return out


def write(rows: list[dict], name: str) -> None:
    book = Workbook()
    guide = book.active
    guide.title = "Instructions"
    for i, text in enumerate(GUIDE, 1):
        guide.cell(i, 1, text).alignment = Alignment(wrap_text=True)
    guide.column_dimensions["A"].width = 110
    sheet = book.create_sheet("Ratings")
    for col, (head, width) in enumerate((("No.", 6), ("URL", 45), ("Sentence", 60), ("Evidence", 80), ("Label", 16), ("Comment", 30)), 1):
        sheet.cell(1, col, head).font = Font(bold=True)
        sheet.column_dimensions["ABCDEF"[col - 1]].width = width
    for i, row in enumerate(rows, 1):
        values = (i, row["url"].replace("http", "hxxp", 1), row["sentence"], row["evidence"] or "(no evidence cited)")
        for col, value in enumerate(values, 1):
            cell = sheet.cell(i + 1, col)
            cell.value = value
            if col > 1:
                cell.data_type = "s"  # never read as a formula
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    choice = DataValidation(type="list", formula1='"' + ",".join(LABELS) + '"', allow_blank=True)
    sheet.add_data_validation(choice)
    choice.add(f"E2:E{len(rows) + 1}")
    sheet.freeze_panes = "A2"
    book.save(AUDIT / name)


def score() -> None:
    key = json.loads((AUDIT / "key.json").read_text())
    raters = []
    for name in ("rater_A.xlsx", "rater_B.xlsx"):
        sheet = load_workbook(AUDIT / name)["Ratings"]
        raters.append([sheet.cell(i + 2, 5).value for i in range(len(key))])
    if any(v not in LABELS for r in raters for v in r):
        raise SystemExit("Some rows are not rated yet.")
    a, b = raters
    agree = sum(x == y for x, y in zip(a, b)) / len(a)
    chance = sum((a.count(l) / len(a)) * (b.count(l) / len(b)) for l in LABELS)
    print(f"agreement {agree:.3f}, Cohen's kappa {(agree - chance) / (1 - chance):.3f}")
    for system in ("PhishTrace", "LLM-RAG"):
        rows = [i for i, k in enumerate(key) if k["system"] == system]
        print(system, len(rows), {l: round(sum((a[i] == l) + (b[i] == l) for i in rows) / (2 * len(rows)), 3) for l in LABELS})


if __name__ == "__main__":
    if "--score" in sys.argv:
        score()
    else:
        data = items()
        (AUDIT / "key.json").write_text(json.dumps([{"no": i + 1, "system": d["system"]} for i, d in enumerate(data)]))
        for file in ("rater_A.xlsx", "rater_B.xlsx"):
            if (AUDIT / file).exists():
                raise SystemExit(f"{file} exists; move it first so that ratings are not lost.")
            write(data, file)
        print(len(data), {s: sum(d["system"] == s for d in data) for s in ("PhishTrace", "LLM-RAG")})
