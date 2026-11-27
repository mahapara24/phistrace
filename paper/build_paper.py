"""Fill the IEEE A4 conference template with the PhishTrace paper.

Usage:  python3 paper/build_paper.py <template.docx> [out.docx]

The template's own styles (paper title, Author, Abstract, Keywords, Heading 1/2,
Body Text, table head/copy, figure caption, references) are reused, so the
section, table, figure, and reference numbers come from the template's
numbering. Citations are written as {key} and numbered in order of first use.
All numbers come from data/eval_results.json (v4), data/eval_v3.json, data/eval_v2.json,
data/eval_v4_sensitive.json, data/eval_baseline.json,
data/eval_robustness.json, data/eval_lightgbm.json, and data/eval_llm_rag.json. List sizes come from app/corpus.py.
"""

from __future__ import annotations

import json
import re
import shutil
import struct
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
CUR = json.loads((DATA / "eval_results.json").read_text())
BASE = json.loads((DATA / "eval_baseline.json").read_text())
sys.path.insert(0, str(HERE.parent))
from app.corpus import BRANDS, FREE_HOSTS, PATH_HOSTS, SHORTENERS, SUSPICIOUS_TLDS  # noqa: E402

N_BRANDS = len(BRANDS)
N_HOSTS = len(FREE_HOSTS | set(PATH_HOSTS))
N_SHORT = len(SHORTENERS)
N_TLDS = len(SUSPICIOUS_TLDS)

# ----------------------------------------------------------------- references
REFS = {
    "apwg": "Anti-Phishing Working Group, “Phishing activity trends report, 4th quarter 2025,” APWG, Feb. 18, 2026. Accessed: Nov. 17, 2026. [Online]. Available: https://docs.apwg.org/reports/apwg_trends_report_q4_2025.pdf",
    "interisle": "Interisle Consulting Group, “Phishing landscape 2024: A study of the scope and distribution of phishing,” Jul. 23, 2024. Accessed: Nov. 17, 2026. [Online]. Available: https://interisle.net/PhishingLandscape2024",
    "prasad": "A. Prasad and S. Chandra, “PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning,” Comput. Secur., vol. 136, Art. no. 103545, Jan. 2024, doi: 10.1016/j.cose.2023.103545.",
    "mohammad12": "R. M. Mohammad, F. Thabtah, and L. McCluskey, “An assessment of features related to phishing websites using an automated technique,” in Proc. 7th Int. Conf. Internet Technol. Secured Trans. (ICITST), London, U.K., Dec. 2012, pp. 492–497.",
    "uci327": "R. M. Mohammad and L. McCluskey, “Phishing Websites,” UCI Machine Learning Repository, Dataset 327, 2012, doi: 10.24432/C51W2X.",
    "sahoo": "D. Sahoo, C. Liu, and S. C. H. Hoi, “Malicious URL detection using machine learning: A survey,” 2017, arXiv:1701.07179.",
    "sahingoz": "O. K. Sahingoz, E. Buber, O. Demir, and B. Diri, “Machine learning based phishing detection from URLs,” Expert Syst. Appl., vol. 117, pp. 345–357, Mar. 2019, doi: 10.1016/j.eswa.2018.09.029.",
    "tang": "L. Tang and Q. H. Mahmoud, “A survey of machine learning-based solutions for phishing website detection,” Mach. Learn. Knowl. Extr., vol. 3, no. 3, pp. 672–694, Aug. 2021, doi: 10.3390/make3030034.",
    "safi": "A. Safi and S. Singh, “A systematic literature review on phishing website detection techniques,” J. King Saud Univ. Comput. Inf. Sci., vol. 35, no. 2, pp. 590–611, Feb. 2023, doi: 10.1016/j.jksuci.2023.01.004.",
    "access25": "Y. A. Kustiawan and K. I. Ghauth, “Feature engineering for phishing website detection using machine learning: A systematic review,” IEEE Access, vol. 13, pp. 192080–192104, 2025, doi: 10.1109/ACCESS.2025.3630334.",
    "garera": "S. Garera, N. Provos, M. Chew, and A. D. Rubin, “A framework for detection and measurement of phishing attacks,” in Proc. ACM Workshop Recurring Malcode (WORM), Nov. 2007, pp. 1–8, doi: 10.1145/1314389.1314391.",
    "cantina": "Y. Zhang, J. I. Hong, and L. F. Cranor, “CANTINA: A content-based approach to detecting phishing web sites,” in Proc. 16th Int. Conf. World Wide Web (WWW), May 2007, pp. 639–648, doi: 10.1145/1242572.1242659.",
    "kintis": "P. Kintis et al., “Hiding in plain sight: A longitudinal study of combosquatting abuse,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur. (CCS), Oct. 2017, pp. 569–586, doi: 10.1145/3133956.3134002.",
    "agten": "P. Agten, W. Joosen, F. Piessens, and N. Nikiforakis, “Seven months’ worth of mistakes: A longitudinal study of typosquatting abuse,” in Proc. Netw. Distrib. Syst. Secur. Symp. (NDSS), 2015, doi: 10.14722/ndss.2015.23058.",
    "lewis": "P. Lewis et al., “Retrieval-augmented generation for knowledge-intensive NLP tasks,” in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 33, 2020, pp. 9459–9474.",
    "yao": "S. Yao et al., “ReAct: Synergizing reasoning and acting in language models,” in Proc. Int. Conf. Learn. Represent. (ICLR), 2023.",
    "nicklas": "F. Nicklas, N. Ventulett, and J. Conrad, “Enhancing phishing email detection with context-augmented open large language models,” in Proc. Upper-Rhine Artif. Intell. Symp. (URAI), Offenburg, Germany, Nov. 2024, pp. 159–166, doi: 10.60643/urai.v2024p159.",
    "li26": "W. Li, S. Manickam, Y.-W. Chong, and S. Karuppayah, “PhishIntentionLLM: Uncovering phishing website intentions through multi-agent retrieval-augmented generation,” in Digital Forensics and Cyber Crime (ICDF2C 2025), Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering. Cham, Switzerland: Springer, 2026, pp. 88–106, doi: 10.1007/978-3-032-22545-0_6.",
    "openphish": "OpenPhish, “OpenPhish community phishing feed,” OpenPhish. Accessed: Nov. 4, 2026. [Online]. Available: https://openphish.com/phishing_feeds.html",
    "urlhaus": "abuse.ch, “URLhaus: Malware URL exchange,” abuse.ch. Accessed: Nov. 8, 2026. [Online]. Available: https://urlhaus.abuse.ch/",
    "urlhausmirror": "malware-filter, “Online malicious URL blocklist (urlhaus-filter),” GitLab repository. Accessed: Nov. 8, 2026. [Online]. Available: https://gitlab.com/malware-filter/urlhaus-filter",
    "tranco": "V. Le Pochat, T. Van Goethem, S. Tajalizadehkhoob, M. Korczyński, and W. Joosen, “Tranco: A research-oriented top sites ranking hardened against manipulation,” in Proc. 26th Annu. Netw. Distrib. Syst. Secur. Symp. (NDSS), Feb. 2019, doi: 10.14722/ndss.2019.23386.",
    "phishdb": "M. Krog, N. Chababy, and Phishing.Database contributors, “Phishing.Database,” GitHub repository, version V.2026-10-02.17. Accessed: Nov. 4, 2026. [Online]. Available: https://github.com/Phishing-Database/Phishing.Database",
}
REFS.update({
    "lightgbm": "G. Ke et al., “LightGBM: A highly efficient gradient boosting decision tree,” in Proc. Adv. Neural Inf. Process. Syst. (NIPS), vol. 30, 2017, pp. 3146–3154.",
    "phi3": "M. Abdin et al., “Phi-3 technical report: A highly capable language model locally on your phone,” 2024, arXiv:2404.14219.",
    "llama": "A. Grattafiori et al., “The Llama 3 herd of models,” 2024, arXiv:2407.21783.",
    "mcnemar": "Q. McNemar, “Note on the sampling error of the difference between correlated proportions or percentages,” Psychometrika, vol. 12, no. 2, pp. 153–157, Jun. 1947, doi: 10.1007/BF02295996.",
    "bm25": "S. Robertson and H. Zaragoza, “The probabilistic relevance framework: BM25 and beyond,” Found. Trends Inf. Retr., vol. 3, no. 4, pp. 333–389, 2009, doi: 10.1561/1500000019.",
})
_order: list[str] = []


def cite(text: str) -> str:
    def repl(match: re.Match) -> str:
        nums = []
        for key in match.group(1).split(","):
            key = key.strip()
            if key not in REFS:
                raise KeyError(key)
            if key not in _order:
                _order.append(key)
            nums.append(_order.index(key) + 1)
        return ", ".join(f"[{n}]" for n in sorted(nums))

    return re.sub(r"\{([a-z0-9,\s]+)\}", repl, text)


# ----------------------------------------------------------------- numbers
ROB = json.loads((DATA / "eval_robustness.json").read_text())
LGB = json.loads((DATA / "eval_lightgbm.json").read_text())
LLM = json.loads((DATA / "eval_llm_rag.json").read_text())
V2 = json.loads((DATA / "eval_v2.json").read_text())
V3 = json.loads((DATA / "eval_v3.json").read_text())
SENS = json.loads((DATA / "eval_v4_sensitive.json").read_text())


def pct(x: float, digits: int = 1) -> str:
    return f"{x * 100:.{digits}f}"


def f3(x: float) -> str:
    return f"{x:.3f}"


t4 = CUR["phiusiil"]["test"]
t3 = V3["phiusiil"]["test"]
t2 = V2["phiusiil"]["test"]
t1 = BASE["phiusiil"]["test"]
d4 = CUR["phiusiil"]["dev"]
ts = SENS["phiusiil"]["test"]
ext4 = CUR["external"]
ext3 = V3["external"]
ext2 = V2["external"]
rw4 = CUR["realworld"]
rw3 = V3["realworld"]
rw2 = V2["realworld"]
rws = SENS["realworld"]
exts = SENS["external"]
ch = CUR["chain"]["modes"]
N_TEST = t4["n"]
N_DEV = d4["n"]
N_ALL = N_TEST + N_DEV
MISSED = t4["alert"]["fn"]
RULES = {r["id"]: r for r in CUR["phiusiil"]["rule_rates_test"]}


def n(x: int) -> str:
    return f"{x:,}"


def ci(pair, digits: int = 3) -> str:
    return f"{pair[0]:.{digits}f}–{pair[1]:.{digits}f}"


def signed(x: float, digits: int = 3) -> str:
    text = f"{x:+.{digits}f}".replace("-", "−")
    return "0" if float(f"{x:.{digits}f}") == 0 else text


def pval(p: float) -> str:
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


PC = ROB["phiusiil_ci"]
RC = ROB["realworld_ci"]
MP = ROB["mcnemar_phiusiil"]
MR = ROB["mcnemar_realworld"]
AB = {a["id"]: a for a in ROB["ablation"]}
WS = ROB["weight_schemes"]
MISS = ROB["missed"]
LM = LGB["models"]
LF, LFR = LM["full|phiusiil"], LM["full|phiusiil+realworld"]
LN, LNR = LM["no_prefix|phiusiil"], LM["no_prefix|phiusiil+realworld"]
LH, LHR = LM["host_only|phiusiil"], LM["host_only|phiusiil+realworld"]
SHORT = LGB["shortcuts"]
LS = LLM["systems"]
SN = LLM["sentences"]
JG = LLM["judge"]
JR = JG["rule"]
def jshare(name, digits=0):
    return pct(JR[name]["supported"] / JR[name]["n"], digits)
HOST = LGB["rules"]["realworld_host_only"]


# ----------------------------------------------------------------- XML helpers
def run(text: str, italic=False, bold=False, sup=False, size=None) -> str:
    props = ""
    if bold:
        props += "<w:b/><w:bCs/>"
    if italic:
        props += "<w:i/><w:iCs/>"
    if size:
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if sup:
        props += '<w:vertAlign w:val="superscript"/>'
    rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def rich(text: str, size=None, bold=False) -> str:
    """*italic* segments; everything else plain."""
    text = cite(text)
    parts = text.split("*")
    return "".join(run(p, italic=(i % 2 == 1), size=size, bold=bold) for i, p in enumerate(parts) if p)


def para(style: str, inner: str, ppr_extra: str = "") -> str:
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/>{ppr_extra}</w:pPr>{inner}</w:p>'


def body(text: str) -> str:
    return para("BodyText", rich(text))


def h1(text: str) -> str:
    return para("Heading1", run(text))


def h2(text: str) -> str:
    return para("Heading2", run(text))


def h5(text: str) -> str:
    return para("Heading5", run(text))


def equation(text: str, number: int) -> str:
    font = '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/></w:rPr>'
    runs = f'<w:r>{font}<w:tab/></w:r><w:r>{font}<w:t xml:space="preserve">{escape(text)}</w:t></w:r><w:r>{font}<w:tab/></w:r><w:r>{font}<w:t>({number})</w:t></w:r>'
    return para("equation", runs)


def table(caption: str, header: list[str], rows: list[list[str]], widths_pt: list[float], note: str = "", left: int = 1,
          size: int = 16, rule_after: tuple[int, ...] = (), groups: tuple[tuple[str, int], ...] = (), left_cols: tuple[int, ...] = ()) -> str:
    """Three horizontal rules and no vertical ones. The first `left` columns are left-aligned, the rest right-aligned."""
    grid = "".join(f'<w:gridCol w:w="{int(w * 20)}"/>' for w in widths_pt)
    thick = 'w:val="single" w:sz="8" w:space="0" w:color="auto"'
    thin = 'w:val="single" w:sz="4" w:space="0" w:color="auto"'
    last = len(rows) - 1

    def cell(text: str, width: float, head: bool, col: int, borders: str) -> str:
        style = "tablecolhead" if head else "tablecopy"
        jc = f'<w:jc w:val="{"start" if col < left or col in left_cols else "end"}"/>'
        edge = f"<w:tcBorders>{borders}</w:tcBorders>" if borders else ""
        keep = "<w:keepNext/>"
        return (
            f'<w:tc><w:tcPr><w:tcW w:w="{width}pt" w:type="dxa"/>{edge}<w:vAlign w:val="center"/></w:tcPr>'
            f'<w:p><w:pPr><w:pStyle w:val="{style}"/>{keep}<w:spacing w:before="1pt" w:after="1pt"/>{jc}</w:pPr>{rich(text, size=size, bold=head)}</w:p></w:tc>'
        )

    def row(cells: list[str], head: bool, index: int = -1) -> str:
        trpr = '<w:trPr><w:cantSplit/><w:tblHeader/><w:jc w:val="center"/></w:trPr>' if head else '<w:trPr><w:cantSplit/><w:jc w:val="center"/></w:trPr>'
        borders = (f"<w:bottom {thin}/>" if groups else f"<w:top {thick}/><w:bottom {thin}/>") if head else ""
        if not head and index == last:
            borders = f"<w:bottom {thick}/>"
        elif not head and index in rule_after:
            borders = f"<w:bottom {thin}/>"
        return "<w:tr>" + trpr + "".join(cell(c, w, head, i, borders) for i, (c, w) in enumerate(zip(cells, widths_pt))) + "</w:tr>"

    def group_row() -> str:
        cells, at = "", 0
        for text, span in groups:
            edge = f"<w:top {thick}/>" + (f"<w:bottom {thin}/>" if text else "")
            cells += (
                f'<w:tc><w:tcPr><w:tcW w:w="{sum(widths_pt[at:at + span])}pt" w:type="dxa"/><w:gridSpan w:val="{span}"/><w:tcBorders>{edge}</w:tcBorders></w:tcPr>'
                f'<w:p><w:pPr><w:pStyle w:val="tablecolhead"/><w:keepNext/><w:spacing w:before="1pt" w:after="1pt"/><w:jc w:val="center"/></w:pPr>{rich(text, size=size, bold=True)}</w:p></w:tc>'
            )
            at += span
        return '<w:tr><w:trPr><w:cantSplit/><w:tblHeader/><w:jc w:val="center"/></w:trPr>' + cells + "</w:tr>"

    tbl = (
        '<w:tbl><w:tblPr><w:tblW w:w="0pt" w:type="dxa"/><w:jc w:val="center"/>'
        '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:start w:w="1.5pt" w:type="dxa"/><w:end w:w="1.5pt" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="1" w:noVBand="1"/></w:tblPr>'
        f"<w:tblGrid>{grid}</w:tblGrid>" + (group_row() if groups else "") + row(header, True) + "".join(row(r, False, i) for i, r in enumerate(rows)) + "</w:tbl>"
    )
    out = para("tablehead", run(caption), "<w:keepNext/>") + tbl  # keep the caption on the table's page
    if note:  # 8-pt note without the template's automatic a, b, c letters
        ppr = ('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr><w:spacing w:before="4pt" w:after="10pt"/>'
               '<w:ind w:start="0pt" w:firstLine="0pt"/><w:jc w:val="both"/>')
        out += para("tablefootnote", rich(note, size=16), ppr)
    else:
        out += '<w:p><w:pPr><w:spacing w:after="6pt"/></w:pPr></w:p>'
    return out


_images: list[tuple[str, Path]] = []


def figure(path: Path, caption: str, width_in: float = 3.3) -> str:
    w, h = struct.unpack(">II", path.read_bytes()[16:24])
    cx = int(width_in * 914400)
    cy = int(cx * h / w)
    rid = f"rIdFig{len(_images) + 1}"
    _images.append((rid, path))
    idx = len(_images)
    a = "http://purl.oclc.org/ooxml/drawingml/main"
    pic = "http://purl.oclc.org/ooxml/drawingml/picture"
    drawing = (
        f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
        f'<wp:docPr id="{100 + idx}" name="Figure {idx}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="{a}" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        f'<a:graphic xmlns:a="{a}"><a:graphicData uri="{pic}"><pic:pic xmlns:pic="{pic}">'
        f'<pic:nvPicPr><pic:cNvPr id="{idx}" name="{path.name}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>"
    )
    holder = f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="6pt" w:after="0pt"/><w:jc w:val="center"/></w:pPr>{drawing}</w:p>'
    return holder + para("figurecaption", rich(caption))


# ----------------------------------------------------------------- content
TITLE = "A Rule-Based Agentic Retrieval Framework for Phishing URL Detection and Evidence-Verified Investigation"
AUTHOR_LINES = [
    ("Mahapara", False),
    ("MS (Data Science), 26I8005_A", True),
    ("Department of Artificial Intelligence & Data Science", True),
    ("FAST NUCES Islamabad Campus", True),
    ("Islamabad, Pakistan", False),
    ("mahapara2424@gmail.com", False),
]
ABSTRACT = (
    "Most phishing and malware URL detectors return a label and stop there, without the evidence behind it. This paper presents "
    "PhishTrace, which detects malicious URLs from the URL text and then investigates each decision without any trained or "
    "generative model. Twenty-two weighted rules produce a score and a verdict, and fixed agents publish only the sentences that "
    "a tagged exhibit covers. "
    f"On {n(N_TEST)} held-out PhiUSIIL URLs, precision is {f3(t4['alert']['precision'])}, recall is {f3(t4['alert']['recall'])} "
    f"(95% CI {ci(PC['v4']['alert']['ci95']['recall'])}), and F1 is {f3(t4['alert']['f1'])}. On phishing and malware feeds pooled "
    f"against popular domains, F1 is {f3(rw4['alert']['f1'])} with {pct(rw4['alert']['fpr'], 2)} percent false alarms. The cost of "
    "this audit-first design is measured on the same splits. A lexical LightGBM classifier reaches an F1 of "
    f"{f3(LF['phiusiil']['f1'])} on PhiUSIIL but {f3(LN['phiusiil']['f1'])} once the scheme and www prefix, a collection artifact, "
    f"are removed, and {f3(LNR['realworld']['f1'])} on the pooled lists when it is trained on both sources. A retrieval-augmented "
    f"pipeline around a 3-billion-parameter open model reaches an F1 of {f3(LS['llm_rag']['f1'])} on {LLM['n']} URLs, against "
    f"{f3(LS['rules']['f1'])} for the rules. Free hosting and file download carry most of the recall, and the alert verdict does not "
    "change when the weights move by 25 percent. Full sentence support holds by construction; a separate judge model finds the "
    f"cited evidence on topic for {jshare('PhishTrace')} percent of PhishTrace's rule sentences, {jshare('Retrieval only')} percent "
    f"with plain retrieval, {jshare('LLM-RAG')} percent for the language model, and {jshare('Control (wrong exhibit)')} percent of wrong-exhibit controls."
)
KEYWORDS = "phishing detection, malicious URL, rule-based detection, retrieval-augmented generation, agents, explainability, verification"

R = RULES
SECTIONS: list[str] = []
S = SECTIONS.append
IND = '<w:ind w:start="10pt" w:firstLine="0pt"/>'

S(h1("Introduction"))
S(body(
    "A fake link is still one of the cheapest ways to steal a login, take a card number, or get someone to run malware. "
    "Industry trackers count these attacks in the millions every year {apwg,interisle}. In the research literature the task is "
    "almost always framed as yes-or-no classification. Features are pulled from the URL, the host, or the page, and a model "
    "learns to split the two classes {sahoo,sahingoz,tang,safi}. The label such a model returns is a reasonable starting point. "
    "It does not, however, tell an analyst what evidence lies behind it, whether anyone checked that evidence, or what to do "
    "about the link."
))
S(body(
    "Two ideas from language-model research point toward something better. Retrieval-augmented generation (RAG) looks up "
    "passages before producing an answer {lewis}. Agent designs let the system pick its next tool based on what it has "
    "seen so far {yao}. Both have started to appear in phishing studies, typically with a large language model doing the "
    "work and, in one study, several cooperating agents {nicklas,li26}. Two gaps are left open. A single look-up followed by "
    "an answer always takes the same route, so it has no way to notice that a piece of evidence is missing. And when a "
    "language model drafts the report, no step makes sure each of its sentences is backed by what was retrieved."
))
S(body(
    "This study keeps the detect, retrieve, verify, and report chain of an agentic RAG system but builds every stage from "
    "transparent, deterministic components. No classifier is trained and no generative model is called. The detector is a "
    "table of weighted rules that an analyst can read. The agents are fixed functions that call tools. The verifier is a "
    "separate function, and it withholds any sentence that no exhibit covers. This design puts auditability ahead of raw "
    "accuracy. The evaluation measures what that choice costs in detection quality against a trained classifier and a "
    "language-model pipeline, on benchmark data and on live feeds."
))
S(body("The contributions of this paper are as follows."))
for item in (
    "*A transparent URL detector for phishing and malware.* Twenty-two weighted rules, including five added in this work "
    "(free hosting {interisle} and dynamic DNS hosts, machine-generated labels, glued www or com labels, program or archive downloads, and "
    "per-victim hex folders), one-edit typosquat matching, and mixed-script homograph checks, produce a score and a three-way verdict.",
    "*A score-driven agentic investigation chain.* The score selects which registries and retrievals run. A separate verifier "
    "keeps only the sentences that an exhibit covers, and the report contains nothing else.",
    "*A reproducible evaluation that prices the design.* The detector is measured on hash-based held-out splits of "
    "PhiUSIIL {prasad}, two phishing feeds {openphish,phishdb}, a malware feed {urlhaus}, and the Tranco top sites {tranco}, "
    "with confidence intervals, McNemar tests, rule ablation, and sensitivity analysis. It is compared with a lexical LightGBM classifier "
    "and an open-weight language-model pipeline, and the chain is compared with rules-only and retrieval-only baselines.",
):
    S(para("BodyText", rich(item), IND))

S(h1("Related Work"))
S(h2("Machine-Learning URL and Website Detection"))
S(body(
    "Learning from hand-built features is the oldest and largest line of work. The website feature set of Mohammad et al. "
    "{mohammad12,uci327} is still reused in many later studies. Several surveys {sahoo,tang,safi,access25} catalogue the "
    "features in use, which come from the URL string, the host, and the page itself, and the models trained on them, from "
    "logistic regression and decision trees to random forests, support vector machines, and boosted ensembles. Sahingoz et al. "
    "{sahingoz} showed that the URL string on its own can already give high accuracy. Prasad and Chandra {prasad} built "
    "PhiUSIIL, a large labeled URL collection that adds similarity-index features. In all of these systems the output ends "
    "at a label; nothing is retrieved, checked, or written up."
))
S(h2("Heuristic and Lexical Detection"))
S(body(
    "Early detectors relied on rules a person could read. Garera et al. {garera} measured how often phishing URLs hide their "
    "target, for instance by placing a brand name in a subdomain or using a bare IP address as the host. CANTINA {cantina} "
    "mixed word-frequency scores from the page with a small set of such rules. Two long-term measurement studies, one on "
    "combosquatting {kintis} and one on typosquatting {agten}, found that attackers either add extra words to a brand name or "
    "alter a single character in it. The brand rules in PhishTrace are built around exactly these two tricks."
))
S(h2("Retrieval and Agents for Phishing Analysis"))
S(body(
    "Nicklas et al. {nicklas} fed retrieved context to open language models to classify phishing emails. Retrieval enriches "
    "the input there, yet the system still answers with a class. Li et al. {li26} went further and used several RAG agents "
    "to explain what a phishing page is trying to achieve. Neither study links a URL detector to retrieved evidence and then "
    "to a checker that limits what the final report is allowed to say. Table I lists the data and the results these studies "
    "report. The tasks and the data sets differ, so the numbers show the range in the literature and are not a ranking; "
    "Section VI-D compares methods on identical splits."
))
S(table(
    "Reported Results of Prior Work",
    ["Study", "Data", "Acc.", "F1", "FPR", "Time", "R / V"],
    [
        [cite("CANTINA {cantina}"), "200 pages", "—", "—", "0.010", "—", "N / N"],
        [cite("Sahingoz {sahingoz}"), "73,575 URLs", "0.980", "—", "—", "—", "N / N"],
        [cite("Prasad {prasad}"), "235,795 URLs", "0.998", "—", "—", "—", "N / N"],
        [cite("Nicklas {nicklas}"), "5,800 emails", "0.962", "0.962", "0.023", "—", "Y / N"],
        [cite("Li {li26}"), "2,063 pages", "0.892", "0.821", "—", "—", "Y / P"],
        ["This work, v4", f"{n(N_TEST)} URLs", f3(t4["alert"]["accuracy"]), f3(t4["alert"]["f1"]), f"{t4['alert']['fpr']:.4f}", f"{CUR['phiusiil']['ms_per_url']:.1f} ms", "Y / Y"],
    ],
    [58, 56, 26, 26, 30, 28, 24],
    "R / V: retrieval / separate verifier (Y yes, N no, P partial). A dash marks a value not given in the sources consulted: the abstract "
    "and data records for Sahingoz and Prasad, the full text for the others. CANTINA reports a true positive rate of 0.89. Prasad reports 0.992 for fully "
    "incremental training. Nicklas is Llama 3.1 70B with retrieval; its FPR is one minus the reported specificity. Li classifies the "
    "intent of known phishing pages (GPT-4o, micro-averaged) and does not detect phishing.",
    left=2, size=15,
))

S(h1("Research Questions"))
S(body("The study follows one chain, detection then retrieval then agents, and asks four questions."))
for label, text in (
    ("RQ1.", "How effectively can a transparent rule-based detector separate phishing and malware URLs from legitimate ones, "
             "so that its score can serve as the initial risk signal?"),
    ("RQ2.", "Does retrieved cybersecurity evidence support and explain that signal better than the rule output alone?"),
    ("RQ3.", "Do agents that choose tools from the score and verify evidence separately from the report reduce unsupported "
             "claims and increase investigation completeness compared with non-agentic retrieval?"),
    ("RQ4.", "What detection quality does the audit-first design give up against a trained lexical classifier and an open-weight "
             "language-model pipeline on the same splits?"),
):
    S(para("BodyText", run(label + " ", bold=True) + rich(text), IND))
S(h1("Methodology"))
S(body(
    "Fig. 1 shows the pipeline. The system reads only the URL string. It never opens the page, follows a redirect, or "
    "contacts the host, so an investigation cannot set off the attack it is studying."
))
S(figure(HERE / "fig1_pipeline.png", "PhishTrace pipeline. The detector score selects the investigation path. The green "
         "stages form the agentic chain; the baselines reuse the same signal."))
S(h2("Input Preparation"))
S(body(
    "A URL of at most 2048 characters is accepted only with the http or https scheme. The parser extracts the host, port, "
    "path, query, and user information, then derives the public suffix and the registrable domain using a table of "
    "multi-label suffixes such as co.uk and com.pk, plus a generic rule for second-level labels such as com or co under a "
    "two-letter country code. A leading www label is not counted as a subdomain. Brand matching folds common digit-for-letter "
    "swaps (0 to o, 1 to l, 3 to e, 4 to a, 5 to s, 7 to t) before comparison."
))
S(h2("Rule-Based Detector"))
S(body("Each rule tests one observable property of the URL and adds a fixed weight when it fires. The score is"))
S(equation("S = min(100, Σ w_r over all fired rules r)", 1))
S(body(
    "Table II lists the strongest rules. A brand mismatch fires when a token in the host or user information names one of "
    f"{N_BRANDS} listed brands, but the registrable domain is not on that brand's list of official and infrastructure domains (for "
    "example githubusercontent.com for GitHub) and is not under a brand-owned top-level domain such as .google. The exact brand "
    "name on a country-code suffix or on .com, .net, or .org (hsbc.fr) is read as the brand's own domain. On a newer generic "
    "suffix (interac.tax) it is not, because anyone can register such a name. A token "
    "matches when it equals the brand, starts with it (a common form of combosquatting {kintis}), or, for names of six or more letters, differs "
    "by one insertion, deletion, substitution, or adjacent swap (typosquatting {agten}). Brands that are also ordinary words, "
    "such as apple and steam, match a longer token only when the extra text is an account word such as id, login, or support, "
    "and short brand names such as DHL or DPD match only a whole token. "
    "A Punycode label fires only when it decodes to Latin letters mixed with letters of another script, which is the homograph "
    "form. A name written wholly in Thai, Cyrillic, or accented Latin does not fire."
))
S(table(
    "Main Detection Rules",
    ["Rule", "Weight", "Fires when"],
    [
        ["Raw IP host", "32", "Host is an IPv4 or IPv6 address"],
        ["Brand mismatch", "28", "Brand token on an unlisted domain"],
        ["Email leftover", "28", "URL contains =3D from email encoding"],
        ["User information", "26", "Text before @ hides the real host"],
        ["Shortener", "26", f"One of {N_SHORT} shorteners, with a short code"],
        ["Free hosting†", "22", f"Page on one of {N_HOSTS} site, storage, IPFS, or dynamic DNS hosts"],
        ["Glued www/com†", "22", "Subdomain label contains www or ends in com"],
        ["Mixed-script IDN", "22", "Punycode label mixes Latin and another script"],
        ["Unusual port", "18", "Port other than 80 or 443"],
        ["Abused suffix", "16", f"Suffix on a {N_TLDS}-entry abuse list {{interisle}}"],
        ["File download†", "16", "Path ends in one of 27 program or archive types"],
        ["Machine label†", "14", "Long label with six consonants in a row or mixed digits"],
        ["Lure words", "6 each", "Account words; parcel-scam words in the host; cap 18"],
    ],
    [72, 36, 132],
    "† Rule added after v1. Nine smaller rules (long URL, very long URL, depth, hyphens, digits, encoding, double slash, explicit HTTP, hex folder†) weigh 8 to 12.",
    left=3,
))
S(h2("Verdict Decision"))
S(body(
    "The verdict is *phishing / malicious* in four cases. The first is a strong rule: brand mismatch, user information, or a "
    "mixed-script label. The second is a host signal backed by a second cue. A free host needs lure words or a machine-generated "
    "label. An abused suffix, raw IP, or shortener needs lure words. A file download needs a raw IP, an unusual port, a free host, "
    "an abused suffix, or a machine-generated label. The third is a program served raw from a user file host such as "
    "raw.githubusercontent.com, and the fourth is a score of 40 or more. The verdict is *suspicious* when a medium rule fires, "
    "when two weak shape cues fire together, or when the score reaches 21. One weak cue on its own, such as an abused suffix, a "
    "long URL, a digit-heavy host, or explicit HTTP, does not raise an alert, because each of these is common on popular "
    "legitimate sites. Every other URL is *not phishing*. Results are given at two operating points. At the *strict* point only "
    "the phishing verdict counts as positive, and at the *alert* point suspicious counts too."
))
S(h2("Knowledge Base and Retrieval"))
S(body(
    "The knowledge base holds 24 exhibits written for this system, each tagged with the rule identifiers it supports, plus "
    "a brand registry and a suffix registry. Every rule is covered by at least one exhibit. Retrieval is either a tag lookup "
    "(agentic mode) or a single term-overlap search over exhibit titles and text, with tag matches weighted eight times "
    "higher (retrieval-only mode). No embedding model is used."
))
S(h2("Agentic Investigation Chain"))
S(body(
    "The chain has five fixed roles. The *detector* records the score and verdict. The *planner* selects a light path for a "
    "score below 21, a standard path from 21 to 49, and a deep path at 50 or above. A brand token or an abused suffix also "
    "opens its registry on a lower path. The *tool* role consults the selected registries and retrieves exhibits by the "
    "tag of each fired rule, plus a low-score exhibit on the light path. The *verifier* is a separate function. It publishes a "
    "candidate sentence only if at least one cited exhibit carries the tag of the rule that produced it. The *reporter* "
    "receives only verified sentences and adds protective recommendations. In short, the detector output decides the next "
    "step, each evidence source is its own tool, and checking is kept apart from writing."
))
S(h2("Baselines"))
S(body(
    "Two baselines share the detector output and isolate the chain. *Rules only* writes one sentence per fired rule, adds the class "
    "label, and stops. *Retrieval only* searches once using the words in the URL, pins the same search results to every sentence, and "
    "publishes the lot unchecked."
))
S(body(
    "Two more baselines replace the detector. The first is a lexical LightGBM classifier {lightgbm} (300 trees, 63 leaves, learning rate "
    "0.08) on 26 URL features such as lengths, character counts, entropy, suffix, and account words, plus three for the scheme and "
    "www. It is trained on the PhiUSIIL development split "
    f"({n(LGB['n']['train_phiusiil'])} URLs), alone or with {n(LGB['n']['train_extra'])} URLs from the real-world development splits, and "
    "cut at a probability of 0.5. Three views are tested: the *full* URL, the URL *without prefix* (scheme and leading www removed), and the "
    "*host only*. The second is a retrieval-augmented pipeline with Llama 3.2 3B {llama}, run locally at temperature 0. The model names the "
    "URL features to check, those words and the words of the URL form a BM25 query {bm25} over the same exhibits, and the model then "
    "returns a label and a report of two or three sentences, each citing exhibits. Nothing checks its citations."
))
S(h2("Evaluation Metrics"))
S(body(
    "Detection quality is reported as accuracy, precision, recall, F1 score, false positive rate (FPR), ROC-AUC, and PR-AUC. "
    "Both area measures rank URLs by the raw score before the cap of 100 is applied. ROC-AUC gives tied scores their average "
    "rank, and PR-AUC is computed as average precision across all score thresholds. "
    "Three measures describe the investigation. The *unsupported-claim rate* is the share of candidate sentences that no cited "
    "exhibit covers. *Evidence support* is the share of published sentences that are covered. *Completeness* is the share of "
    "required checks that actually ran. The checks come from a nine-item list, and which items are required depends on the "
    "score; for example, the brand registry is required whenever a brand token is present. Latency is the wall-clock time "
    "of one investigation."
))
S(body(
    "Intervals are 95 percent. PhiUSIIL and pooled intervals are percentile bootstraps with 10,000 resamples drawn within each class; "
    "single rates use the Wilson interval. Two detectors on the same URLs are compared with McNemar's test {mcnemar} with continuity "
    "correction. The v1 to v3 rule sets were rerun on every test URL and reproduce the counts of the original runs. The ablation removes one rule at a time "
    "from v4 and decides every URL again; the sensitivity analysis moves the thresholds and the weights. Neither was used to change v4."
))

S(h1("Experimental Setup"))
S(h2("Datasets"))
S(body(
    f"PhiUSIIL {{prasad}} provides 235,795 labeled URLs, of which {n(N_ALL)} parse as http or https URLs. Four real-world lists "
    "add data that PhiUSIIL never saw. The first is a snapshot of OpenPhish {openphish}, and the second is the set of active "
    "links in Phishing.Database {phishdb}. The third holds online malware URLs from URLhaus {urlhaus}. They are taken from the "
    "malware-filter project's urlhaus-filter list {urlhausmirror}. That list copies the URLhaus entries that are still online, "
    "refreshes the copy twice a day, and strips the http or https prefix. Working from the copy lets anyone rerun the "
    "evaluation without first getting an abuse.ch Auth-Key, a free key that URLhaus now demands for bulk downloads. The fourth list supplies popular safe sites: the top 100,000 domains of the Tranco "
    "list {tranco} generated on 7 November 2026 (list ID 94P72, https://tranco-list.eu/list/94P72), read as https homepages. "
    "Each URL or domain is placed in a split by its MD5 hash. Three of ten buckets form the development split, and the rest "
    "form the held-out test split. OpenPhish is used only for testing. Table III gives the test sizes. The larger lists are "
    "sampled with a fixed seed."
))
S(table(
    "Evaluation Data (Test Splits)",
    ["Set", "Use", "Malicious", "Safe"],
    [
        ["PhiUSIIL", "Benchmark", n(t4["phishing_n"]), n(t4["legitimate_n"])],
        ["OpenPhish", "Phishing recall", n(ext4["openphish"]["n"]), "0"],
        ["Phishing.Database", "Phishing recall", n(ext4["phishing_database"]["n"]), "0"],
        ["URLhaus", "Malware recall", n(ext4["urlhaus"]["n"]), "0"],
        ["Tranco top-100k", "False alarms", "0", n(ext4["tranco"]["n"])],
    ],
    [76, 68, 50, 46],
    f"PhiUSIIL development split: {n(d4['phishing_n'])} phishing and {n(d4['legitimate_n'])} legitimate URLs.",
    left=2,
))
S(h2("Rule Development Protocol"))
S(body(
    "The first rule set (v1, 17 rules) was written from the literature before any data was inspected. Version 2 (20 rules) was "
    "built by studying misses and false alarms on the PhiUSIIL development split: three new rules, typosquat matching, more "
    "brands, suffixes {interisle}, and lure words, and new decision combinations. Version 3 (22 rules) was built after adding the "
    "real-world development splits. It fixed false alarms on brand infrastructure and on native-script internationalized names. "
    "For example, v2 had flagged every raw.githubusercontent.com link as a GitHub lookalike. Version 3 also added the file-download and "
    "hex-folder rules and dynamic DNS hosts for malware and kit hosting, and it stopped single weak cues from raising an alert. "
    "Version 4 keeps the 22 rules of v3. It came from studying the phishing URLs that v3 missed on the development splits, and "
    "it widens the lists rather than the rules. The hosting list gains cloud storage buckets, IPFS gateways, and shared hosts, "
    "including platforms whose pages sit in the path (sites.google.com, Google Forms, ipfs.io/ipfs/). The shortener list grows, "
    "and a shortener now fires only when a short code follows the host. The brand list adds parcel carriers, banks, "
    "cryptocurrency services, and games. A new brand was kept only if it recovered missed phishing on the development splits "
    "and raised no more than one or two alerts on popular domains. Short or common-word names such as line, att, and meta "
    "failed that test. V4 also closed a gap in which "
    "an exact brand name on a new generic suffix, such as interac.tax, was read as the brand's own domain. "
    "Test splits were used only for the final measurement."
))
S(h2("Implementation"))
S(body(
    "PhishTrace is written in Python 3 with FastAPI for the web interface and only the standard library for detection, "
    "retrieval, and agents. The system itself needs no machine-learning or language-model library; LightGBM, NumPy, SciPy, and the local "
    "model server are used only to run the baselines and the statistics. All timings come from one laptop with a 4-GB GPU, which "
    "only the language model uses."
))

S(h1("Results"))
S(h2("Benchmark Detection (RQ1)"))
S(body(
    f"Table IV reports the four rule sets on the held-out PhiUSIIL test split. At the alert operating point, recall rises from "
    f"{f3(t1['alert']['recall'])} in v1 to {f3(t2['alert']['recall'])} in v2, while the false positive rate falls from "
    f"{pct(t1['alert']['fpr'], 2)} to {pct(t2['alert']['fpr'], 2)} percent. Version 3 gives up some recall "
    f"({f3(t3['alert']['recall'])}) because single weak cues no longer raise an alert, and cuts the false positive rate to "
    f"{pct(t3['alert']['fpr'], 3)} percent. Section VI-B shows why this trade is worth making on real traffic. Version 4 "
    f"recovers most of that recall ({f3(t4['alert']['recall'])}) and raises accuracy from {f3(t3['alert']['accuracy'])} to "
    f"{f3(t4['alert']['accuracy'])} and F1 from {f3(t3['alert']['f1'])} to {f3(t4['alert']['f1'])}, at a false positive rate "
    f"of {pct(t4['alert']['fpr'], 3)} percent and a precision of {f3(t4['alert']['precision'])}. ROC-AUC is "
    f"{f3(t4['roc_auc'])} in v4 against {f3(t1['roc_auc'])} in v1. The development F1 of "
    f"{f3(d4['alert']['f1'])} is close to the test F1 of {f3(t4['alert']['f1'])}, which suggests that the rule changes did "
    "not overfit the development split."
))
S(table(
    "Detection on the PhiUSIIL Test Split (95% Interval for F1)",
    ["Rules", "Point", "Acc.", "Prec.", "Rec.", "F1", "F1 interval", "FPR"],
    [
        [tag, point.capitalize(), f3(t[point]["accuracy"]), f3(t[point]["precision"]), f3(t[point]["recall"]), f3(t[point]["f1"]), ci(PC[tag][point]["ci95"]["f1"]), f"{t[point]['fpr']:.4f}"]
        for tag, t in (("v1", t1), ("v2", t2), ("v3", t3), ("v4", t4))
        for point in ("strict", "alert")
    ],
    [26, 28, 28, 28, 28, 28, 50, 30],
    f"ROC-AUC / PR-AUC: v1 {f3(t1['roc_auc'])} / {f3(t1['pr_auc'])}; v2 {f3(t2['roc_auc'])} / {f3(t2['pr_auc'])}; v3 {f3(t3['roc_auc'])} / {f3(t3['pr_auc'])}; v4 {f3(t4['roc_auc'])} / {f3(t4['pr_auc'])}. v4 alert intervals: accuracy {ci(PC['v4']['alert']['ci95']['accuracy'])}, precision {ci(PC['v4']['alert']['ci95']['precision'])}, recall {ci(PC['v4']['alert']['ci95']['recall'])}, FPR {ci(PC['v4']['alert']['ci95']['fpr'], 4)}. n = {n(N_TEST)}.",
    left=2, rule_after=(1, 3, 5),
))
S(body(
    "Table V tests these changes on the same URLs. Every step changes the result significantly, and the direction depends on the class: v3 loses "
    f"{n(MP['v2-v3']['phishing']['only_first_correct'])} phishing URLs that v2 caught and clears "
    f"{n(MP['v2-v3']['legitimate']['only_second_correct'])} of its false alarms, and v4 regains {n(MP['v3-v4']['phishing']['only_second_correct'])} "
    "phishing URLs without losing any. Against v2, however, v4 is not more accurate on PhiUSIIL "
    f"(p = {MP['v2-v4']['all']['p']:.2f}, with overlapping F1 intervals). It misses slightly more phishing and raises far fewer false alarms. On the "
    "pooled real-world lists, v4 is better than every earlier version."
))
S(table(
    "McNemar Tests Between Rule Sets (Alert Point)",
    ["Pair", "First", "Second", "χ²", "p", "First", "Second", "χ²", "p"],
    [
        [pair.replace("-", "–"), n(MP[pair]["all"]["only_first_correct"]), n(MP[pair]["all"]["only_second_correct"]), f"{MP[pair]['all']['chi2']:,.0f}" if MP[pair]["all"]["chi2"] > 10 else f"{MP[pair]['all']['chi2']:.1f}", pval(MP[pair]["all"]["p"]).replace("< ", "<"),
         n(MR[pair]["all"]["only_first_correct"]), n(MR[pair]["all"]["only_second_correct"]), f"{MR[pair]['all']['chi2']:,.0f}", pval(MR[pair]["all"]["p"]).replace("< ", "<")]
        for pair in ("v1-v2", "v2-v3", "v3-v4", "v2-v4", "v1-v4")
    ],
    [32, 25, 31, 29, 28, 25, 27, 26, 28],
    f"n = {n(N_TEST)} for PhiUSIIL and {n(LGB['n']['realworld'])} for the pooled lists. First / second: URLs that only the first or only the second rule set of the pair decides correctly. Five pairs are tested; a Bonferroni limit of 0.01 leads to the same conclusions.",
    size=15, groups=(("", 1), ("PhiUSIIL", 4), ("Real-world lists", 4)),
))
S(h2("Real-World Phishing, Malware, and Popular Sites (RQ1)"))
S(body(
    "Table VI and Fig. 2 report the real-world lists at the alert point. On the Tranco top 100,000 domains, v2 raises an alert "
    f"on {pct(ext2['tranco']['alert_fpr'])} percent of popular sites, mostly because of a single abused suffix, a digit-heavy name, "
    f"or a brand token on brand infrastructure. Version 3 brings this down to {pct(ext3['tranco']['alert_fpr'])} percent, a "
    f"{ext2['tranco']['alert_fpr'] / ext3['tranco']['alert_fpr']:.1f}-fold reduction. URLhaus recall is "
    f"{f3(ext3['urlhaus']['alert_recall'])} in v3. The v2 figure of {f3(ext2['urlhaus']['alert_recall'])} looks similar but was "
    "inflated by the raw.githubusercontent.com false match: its strict recall falls from "
    f"{f3(ext2['urlhaus']['strict_recall'])} to {f3(ext3['urlhaus']['strict_recall'])} once that match is fixed, and the new "
    "file-download rule now carries the malware signal. Phishing recall falls on OpenPhish and Phishing.Database, where many "
    "lures show only an abused suffix or a long path. Pooling the three malicious lists against Tranco, v3 raises precision from "
    f"{f3(rw2['alert']['precision'])} to {f3(rw3['alert']['precision'])} and F1 from {f3(rw2['alert']['f1'])} to "
    f"{f3(rw3['alert']['f1'])}. Version 4 wins back part of the lost phishing recall: OpenPhish recall rises from "
    f"{f3(ext3['openphish']['alert_recall'])} to {f3(ext4['openphish']['alert_recall'])} and Phishing.Database recall from "
    f"{f3(ext3['phishing_database']['alert_recall'])} to {f3(ext4['phishing_database']['alert_recall'])}, while false alarms on "
    f"Tranco move from {pct(ext3['tranco']['alert_fpr'], 2)} to {pct(ext4['tranco']['alert_fpr'], 2)} percent. Pooled accuracy "
    f"rises from {f3(rw3['alert']['accuracy'])} to {f3(rw4['alert']['accuracy'])} and pooled F1 from {f3(rw3['alert']['f1'])} to "
    f"{f3(rw4['alert']['f1'])}."
))
S(table(
    "Real-World Lists at the Alert Point",
    ["Measure", "v2", "v3", "v4", "v4 interval"],
    [
        [label, fmt(a), fmt(b), fmt(c), iv]
        for label, fmt, (a, b, c), iv in [
            ("OpenPhish recall", f3, [e["openphish"]["alert_recall"] for e in (ext2, ext3, ext4)], ci(RC["v4"]["openphish"]["ci95"])),
            ("Phishing.Database recall", f3, [e["phishing_database"]["alert_recall"] for e in (ext2, ext3, ext4)], ci(RC["v4"]["phishdb"]["ci95"])),
            ("URLhaus recall", f3, [e["urlhaus"]["alert_recall"] for e in (ext2, ext3, ext4)], ci(RC["v4"]["urlhaus"]["ci95"])),
            ("URLhaus strict recall", f3, [e["urlhaus"]["strict_recall"] for e in (ext2, ext3, ext4)], "—"),
            ("Tranco false alarms (%)", lambda x: pct(x, 2), [e["tranco"]["alert_fpr"] for e in (ext2, ext3, ext4)], ci([100 * v for v in RC["v4"]["tranco"]["ci95"]], 2)),
            ("Pooled accuracy", f3, [r["alert"]["accuracy"] for r in (rw2, rw3, rw4)], ci(RC["v4"]["pooled"]["ci95"]["accuracy"])),
            ("Pooled precision", f3, [r["alert"]["precision"] for r in (rw2, rw3, rw4)], ci(RC["v4"]["pooled"]["ci95"]["precision"])),
            ("Pooled recall", f3, [r["alert"]["recall"] for r in (rw2, rw3, rw4)], ci(RC["v4"]["pooled"]["ci95"]["recall"])),
            ("Pooled F1", f3, [r["alert"]["f1"] for r in (rw2, rw3, rw4)], ci(RC["v4"]["pooled"]["ci95"]["f1"])),
        ]
    ],
    [96, 32, 32, 32, 52],
    f"Pooled: {n(rw4['malicious_n'])} malicious URLs (OpenPhish, Phishing.Database, URLhaus) against {n(rw4['safe_n'])} Tranco domains.",
))
S(figure(HERE / "fig3_realworld.png", "Alert-point recall on the three malicious lists and false alarms on the Tranco top 100,000 domains (shaded) for v2, v3, and v4."))
S(h2("Rule Ablation and Sensitivity"))
S(body(
    "Table VII removes one rule at a time. Two rules carry most of the recall, one per source: without free hosting, PhiUSIIL F1 falls by "
    f"{abs(AB['free_hosting']['d_f1']):.3f}, and without file download, pooled F1 falls by {abs(AB['file_download']['rw_d_f1']):.3f}. Explicit HTTP is the "
    f"second most important rule on PhiUSIIL, and removing it lowers the ROC-AUC from {ROB['full']['roc_auc']:.3f} to "
    f"{ROB['full']['roc_auc'] + AB['no_https']['d_auc']:.3f}, which Section VII-C traces to the data set. "
    f"{sum(1 for a in ROB['ablation'] if abs(a['d_f1']) < 0.001 and abs(a['rw_d_f1']) < 0.001)} of the 22 rules change neither F1 by "
    "0.001 or more. They describe rare tricks and stay for coverage, not for measured gain. The false alarms on popular sites come "
    "mainly from brand mismatch, the digit-heavy host, the abused suffix, and the machine label."
))
TA, TS = ROB["threshold_alert"], ROB["threshold_strict"]
S(body(
    "Table VIII moves the thresholds and the weights. The alert verdict is unchanged for any suspicious threshold from 21 to 32. Below 21, a single weak cue can "
    f"raise an alert again: at 16, the Tranco false alarm rate is {pct(TA['16']['realworld']['fpr'], 2)} percent. At 18 the F1 is slightly higher at the "
    "same false alarm rate; this was seen only on the test split, so the threshold was left at 21. The phishing threshold of 40 trades strict recall "
    f"against little precision. The deep-path threshold of 50 sends {pct(ROB['threshold_deep']['50']['phishing_deep'])} percent of phishing URLs and no "
    "legitimate URL to the deep path."
))
S(body(
    f"Twenty random draws that change every weight by up to 25 percent leave the alert F1 and FPR unchanged, and equal weights give "
    f"an ROC-AUC of {WS['equal']['roc_auc']:.3f} against {WS['hand']['roc_auc']:.3f} for the hand-set weights. The decision logic of Section IV-C, that is, which rules fire together, "
    "therefore decides the alert, and the exact weights matter mainly for the strict verdict and the path. The hand-set weights also do not follow the data: "
    f"their rank correlation with the development-split log-likelihood ratio of each rule is {signed(ROB['weights']['spearman'], 2)} (p = {ROB['weights']['spearman_p']:.2f}). "
    f"Weights proportional to that ratio raise the pooled strict F1 from {WS['hand']['rw_strict_f1']:.3f} to {WS['log_ratio']['rw_strict_f1']:.3f} "
    f"and the alert F1 from {WS['hand']['rw_alert_f1']:.3f} to {WS['log_ratio']['rw_alert_f1']:.3f}, which makes them the first candidate for a next version."
))
_ab = sorted(ROB["ablation"], key=lambda a: min(a["d_f1"], a["rw_d_f1"]))
S(table(
    "Leave-One-Rule-Out Ablation of v4 (Alert Point)",
    ["Rule removed", "Weight", "Fires", "ΔF1", "ΔAUC", "ΔF1", "ΔFPR"],
    [
        [a["label"].replace("Program or archive download", "File download").replace("Free hosting platform", "Free hosting").replace("Machine-generated label", "Machine label").replace("Email encoding leftover", "Email leftover"),
         "6–18" if a["id"] == "lure_terms" else str(a["weight"]), f"{R[a['id']]['phishing_pct']:.1f}", signed(a["d_f1"]), signed(a["d_auc"]), signed(a["rw_d_f1"]), signed(100 * a["rw_d_fpr"], 2)]
        for a in _ab
    ],
    [80, 30, 24, 30, 30, 30, 28],
    f"Fires: percent of PhiUSIIL test phishing URLs. Full set on PhiUSIIL: F1 {ROB['full']['phiusiil']['f1']:.3f}, ROC-AUC {ROB['full']['roc_auc']:.3f}. Full set on the pooled lists: F1 {ROB['full']['realworld']['f1']:.3f}, FPR {pct(ROB['full']['realworld']['fpr'], 2)} percent. ΔFPR is in percentage points. A zero means a change below the last digit shown.",
    size=15, groups=(("", 2), ("PhiUSIIL", 3), ("Real-world lists", 2)),
))
S(table(
    "Sensitivity of v4 to Thresholds and Weights",
    ["Setting", "F1", "FPR (%)", "F1", "FPR (%)"],
    [[f"Suspicious at {t}" + (" (used)" if t == "21" else ""), f3(TA[t]["phiusiil"]["f1"]), pct(TA[t]["phiusiil"]["fpr"], 2), f3(TA[t]["realworld"]["f1"]), pct(TA[t]["realworld"]["fpr"], 2)] for t in ("12", "16", "18", "21", "32")]
    + [[f"Strict, phishing at {t}" + (" (used)" if t == "40" else ""), f3(TS[t]["phiusiil"]["f1"]), pct(TS[t]["phiusiil"]["fpr"], 2), f3(TS[t]["realworld"]["f1"]), pct(TS[t]["realworld"]["fpr"], 2)] for t in ("30", "40", "50")]
    + [
        ["Equal weights", f3(WS["equal"]["alert_f1"]), pct(WS["equal"]["alert_fpr"], 2), f3(WS["equal"]["rw_alert_f1"]), pct(WS["equal"]["rw_alert_fpr"], 2)],
        ["Log-ratio weights", f3(WS["log_ratio"]["alert_f1"]), pct(WS["log_ratio"]["alert_fpr"], 2), f3(WS["log_ratio"]["rw_alert_f1"]), pct(WS["log_ratio"]["rw_alert_fpr"], 2)],
        ["Random ±25%, 20 draws", f3(ROB["perturb_25"]["alert_f1"][0]), pct(ROB["perturb_25"]["alert_fpr"][0], 2), f3(ROB["perturb_25"]["rw_alert_f1"][0]), pct(ROB["perturb_25"]["rw_alert_fpr"][0], 2)],
        ["Random ±50%, 20 draws", ci(ROB["perturb_50"]["alert_f1"], 2), ci([100 * v for v in ROB["perturb_50"]["alert_fpr"]], 2), ci(ROB["perturb_50"]["rw_alert_f1"], 2), ci([100 * v for v in ROB["perturb_50"]["rw_alert_fpr"]], 2)],
    ],
    [96, 38, 38, 38, 38],
    "Strict rows count only the phishing verdict; all other rows are at the alert point. Ranges give the smallest and largest value of the draws.",
    size=15, rule_after=(4, 7), groups=(("", 1), ("PhiUSIIL", 2), ("Real-world lists", 2)),
))
S(h2("Trained and Language-Model Baselines (RQ4)"))
S(body(
    f"Table IX compares the rules with LightGBM. On the full URL, the classifier reaches an F1 of {f3(LF['phiusiil']['f1'])} on PhiUSIIL. That figure is mostly a "
    "collection artifact: every legitimate test URL is an https://www homepage without a path, and only "
    f"{pct(LGB['phiusiil_https_www_homepage']['phishing'])} percent of the phishing URLs have this form, so a one-line rule that flags everything else "
    f"already reaches {f3(SHORT['phiusiil_not_https_www_homepage']['f1'])}. The same model flags every Tranco domain. Without the prefix, its PhiUSIIL F1 is "
    f"{f3(LN['phiusiil']['f1'])} at an FPR of {pct(LN['phiusiil']['fpr'], 2)} percent, and its recall at the FPR of the rules is "
    f"{f3(LN['phiusiil']['recall_at_rules_fpr'])} against {f3(t4['alert']['recall'])}. Trained on both sources, it reaches a pooled F1 of "
    f"{f3(LNR['realworld']['f1'])} against {f3(LGB['rules']['realworld']['f1'])} for the rules. McNemar's test gives p < 0.001 for all of these comparisons except "
    f"the model without prefix trained on PhiUSIIL alone on the pooled lists, where p = {LN['mcnemar_realworld']['p']:.3f}."
))
S(body(
    "The pooled lists have an artifact of their own: no Tranco entry has a path, but "
    f"{pct(LGB['path_share']['openphish'], 0)} to {pct(LGB['path_share']['urlhaus'], 0)} percent of the malicious entries do, so flagging any URL with a path "
    f"reaches an F1 of {f3(SHORT['realworld_has_path']['f1'])}. When every URL is cut to its host, the rules fall to a recall of {f3(HOST['recall'])} and "
    f"the classifier trained on both sources to an F1 of {f3(LHR['realworld']['f1'])} at {pct(LHR['realworld']['fpr'], 2)} percent false alarms. The conclusion for RQ4 is that a "
    "trained lexical model detects clearly more wherever it is trained on similar data, that its benchmark scores overstate this lead, and that PhishTrace "
    "gives up recall in exchange for few false alarms on unseen popular sites and a reason for each decision."
))
def _lg(name, m):
    return [name, f3(m["phiusiil"]["f1"]), pct(m["phiusiil"]["fpr"], 2), f3(m["realworld"]["f1"]), pct(m["realworld"]["fpr"], 2)]


S(table(
    "Rules, Shortcuts, and LightGBM on the Same Test Splits",
    ["Detector (training data)", "F1", "FPR (%)", "F1", "FPR (%)"],
    [
        ["PhishTrace v4 (none)", f3(t4["alert"]["f1"]), pct(LGB["rules"]["phiusiil"]["fpr"], 2), f3(LGB["rules"]["realworld"]["f1"]), pct(LGB["rules"]["realworld"]["fpr"], 2)],
        ["PhishTrace v4, host only", "—", "—", f3(HOST["f1"]), pct(HOST["fpr"], 2)],
        ["One-line shortcut", f3(SHORT["phiusiil_not_https_www_homepage"]["f1"]), "0.00", f3(SHORT["realworld_has_path"]["f1"]), "0.00"],
        _lg("LightGBM, full URL (P)", LF), _lg("LightGBM, full URL (P + R)", LFR),
        _lg("LightGBM, no prefix (P)", LN), _lg("LightGBM, no prefix (P + R)", LNR),
        _lg("LightGBM, host only (P)", LH), _lg("LightGBM, host only (P + R)", LHR),
    ],
    [110, 30, 36, 30, 38],
    "P: PhiUSIIL development split. R: real-world development splits. Shortcut: not an https://www homepage (PhiUSIIL), has a path (real-world).",
    size=15, rule_after=(2,), groups=(("", 1), ("PhiUSIIL", 2), ("Real-world lists", 2)),
))
S(body(
    f"Table X adds the language-model pipeline on {LLM['n']} test URLs ({LLM['phishing']} phishing), drawn from the 1,000-URL sample of Section VI-E; one answer takes "
    f"{LLM['seconds']['median']:.1f} s (median) on the laptop, which set this size. It labels most phishing URLs legitimate (recall {f3(LS['llm_rag']['recall'])}). Its retrieval step finds an exhibit of a fired rule for "
    f"{pct(LLM['retrieval_hit']['hit'] / LLM['retrieval_hit']['urls_with_rule'], 0)} percent of the URLs on which any rule fires, so the errors are not only missing evidence. The rules decide "
    f"{LLM['mcnemar_rules_llm']['rules_only_correct']} URLs correctly that the pipeline gets wrong, and the pipeline {LLM['mcnemar_rules_llm']['model_only_correct']} that the rules get wrong "
    f"(McNemar p {pval(LLM['mcnemar_rules_llm']['p'])}). This is one small open model with one prompt; larger models may do better."
))
S(table(
    f"Detection on {LLM['n']} Shared PhiUSIIL Test URLs",
    ["System", "Acc.", "Prec.", "Rec.", "F1", "FPR", "Time"],
    [
        [label, f3(m["accuracy"]), f3(m["precision"]), f3(m["recall"]), f3(m["f1"]), f3(m["fpr"]), time]
        for label, m, time in (
            ("PhishTrace v4", LS["rules"], f"{CUR['phiusiil']['ms_per_url']:.1f} ms"),
            ("LightGBM, full URL", LS["lightgbm full|phiusiil"], f"{LF['ms_per_url']:.1f} ms"),
            ("LightGBM, no prefix", LS["lightgbm no_prefix|phiusiil"], f"{LN['ms_per_url']:.1f} ms"),
            ("Llama 3.2 3B + RAG", LS["llm_rag"], f"{LLM['seconds']['median']:.1f} s"),
        )
    ],
    [78, 27, 27, 27, 27, 27, 31],
    f"LightGBM is trained on the PhiUSIIL development split. F1 intervals: rules {ci(LLM['f1_ci95']['rules'])}, language model {ci(LLM['f1_ci95']['llm_rag'])}. Time is per URL and one at a time; it excludes loading the model.",
    size=15,
))
S(h2("Evidence and Investigation (RQ2 and RQ3)"))
S(body(
    f"All three modes were run on a seeded, class-balanced sample of {CUR['chain']['n']} PhiUSIIL test URLs (Table XI). Rules only "
    "publishes every sentence without an exhibit, so its unsupported-claim rate is 100 percent and it completes "
    f"{pct(ch['rules']['completeness'])} percent of the required checks. A single retrieval pass attaches exhibits, but "
    f"only {pct(ch['retrieval']['evidence_support'])} percent of its published sentences are covered by a matching exhibit "
    f"and it completes {pct(ch['retrieval']['completeness'])} percent of the checks, because it never opens the registries "
    "or runs the verifier. The agentic chain publishes no unsupported sentence and completes every required check, using "
    f"on average {ch['agentic']['exhibit_count']:.2f} exhibits per report. The zero holds by construction, because the verifier matches tags "
    "and every rule has a tagged exhibit. The informative results are the share of sentences that the baselines publish without covering "
    "evidence and the checks they skip (RQ2 and RQ3)."
))
S(table(
    "Investigation Modes on 1,000 Test URLs",
    ["Mode", "Unsupp.", "Support", "Compl.", "Time (ms)"],
    [
        [label, pct(ch[mode]["unsupported_rate"]), pct(ch[mode]["evidence_support"] or 0), pct(ch[mode]["completeness"]), f"{ch[mode]['agent_ms']:.3f}"]
        for mode, label in (("rules", "Rules only"), ("retrieval", "Retrieval only"), ("agentic", "Agentic chain"))
    ],
    [72, 42, 42, 42, 44],
    "Unsupp. = unsupported-claim rate, Support = evidence support, Compl. = completeness, all in percent. Time is the mean chain time after detection.",
))
S(h2("Sentence Support Outside the Verifier"))
S(body(
    "Because the verifier checks its own tags, support was also tested by means that share nothing with it. Two facts need no judge. "
    f"Over {LLM['n']} reports ({n(SN['total'])} sentences), the language model cites no exhibit in {SN['no_citation']} sentences and cites an identifier that does not exist in "
    f"{SN['unknown_exhibit']}. For {LLM['false_https']['urls']} of the {LLM['false_https']['http_urls']} URLs that start with http://, its report states that the URL uses HTTPS. "
    "PhishTrace cannot make these errors, since its sentences are templates filled from the parsed URL."
))
S(body(
    "A judge model (Phi-3 3.8B {phi3}), which wrote none of the sentences, then read each sentence with its cited evidence for "
    f"{JG['urls']} URLs and answered whether the evidence "
    "addresses the topic of the claim. The same PhishTrace sentences with a randomly chosen wrong exhibit are controls. On rule "
    f"sentences (Table XII), the judge accepts {jshare('PhishTrace', 1)} percent of the correct pairs and {jshare('Control (wrong exhibit)', 1)} percent of the controls, so it tells them apart but is not exact. Retrieval-only "
    f"pairs the same sentences with evidence that is on topic for {jshare('Retrieval only', 1)} percent, and the language model reaches {jshare('LLM-RAG', 1)} percent. On the two fixed low-signal sentences, it accepts "
    f"{JG['low_signal']['Control (wrong exhibit)']['supported']} of {JG['low_signal']['Control (wrong exhibit)']['n']} wrong exhibits, so nothing is concluded from them. The wording was chosen on 12 control pairs from other URLs, after a first version "
    "that answered in JSON rejected every pair. The test covers topic, not truth."
))
S(table(
    "Automatic Support Check on Rule Sentences",
    ["System", "Sentences", "On topic", "95% CI"],
    [
        [label, n(JR[k]["n"]), f"{pct(JR[k]['supported'] / JR[k]['n'])}", f"{pct(JR[k]['ci95'][0])}–{pct(JR[k]['ci95'][1])}"]
        for label, k in (("PhishTrace", "PhishTrace"), ("Control (wrong exhibit)", "Control (wrong exhibit)"), ("Retrieval only", "Retrieval only"), ("Llama 3.2 3B + RAG", "LLM-RAG"))
    ],
    [96, 48, 46, 54],
    f"On topic = share of sentences whose cited evidence the judge accepts, in percent, on {JG['urls']} URLs. Intervals are Wilson. The language model's sentences differ from the rule sentences of the others.",
))
S(h2("Efficiency"))
S(body(
    f"Parsing and scoring take {CUR['phiusiil']['ms_per_url']:.2f} ms per URL on average, so all {n(N_ALL)} PhiUSIIL URLs "
    f"are scored in under three minutes on one core. The agentic chain adds {ch['agentic']['agent_ms']:.3f} ms on average "
    f"({ch['agentic']['p95_agent_ms']:.3f} ms at the 95th percentile). It is faster than the retrieval-only baseline "
    f"({ch['retrieval']['agent_ms']:.3f} ms) because a tag lookup touches fewer exhibits than a full search. No GPU, "
    "network call, or model loading is needed."
))

S(h1("Discussion"))
S(h2("Precision Against Recall"))
S(body(
    "The v3 gate, which ignores single weak cues, trades some recall for fewer false alarms. A sensitive variant of v4 that "
    "keeps every v4 rule but lets any single cue raise an alert, as v2 did, reaches a PhiUSIIL F1 of "
    f"{f3(ts['alert']['f1'])} and a pooled real-world recall of {f3(rws['alert']['recall'])}, "
    f"but it raises an alert on {pct(exts['tranco']['alert_fpr'])} percent of popular sites, against "
    f"{pct(ext4['tranco']['alert_fpr'], 2)} percent for v4. The stricter gate was kept because "
    "a tool that flags several of every hundred popular sites soon teaches its users to ignore it. Both variants come from the same "
    "evaluation script."
))
S(h2("What Limits Recall"))
S(body(
    f"The v4 detector labels {n(MISSED)} PhiUSIIL test phishing URLs ({pct(MISSED / t4['phishing_n'])} percent) as not phishing. "
    f"{pct(MISS['only_http'] / MISS['n'], 0)} percent of them fire explicit HTTP and nothing else, {pct(MISS['no_rule'] / MISS['n'], 0)} percent fire no rule at all, "
    f"and the rest fire another weak cue such as a long URL or an abused suffix. Many are bare registered "
    "domains such as http://www.example-shop.com, with no brand token, lure word, or unusual structure. Broader matching was "
    "tested on the development splits and rejected: one-edit typos of brand infrastructure names and alerts on an abused suffix alone recovered "
    "thousands of misses but multiplied false alarms on popular sites. Alerting on HTTP alone would recover most misses on PhiUSIIL, but only because of "
    "how its legitimate URLs were collected. LightGBM without the prefix recovers part of the gap, which shows that some "
    "signal remains in the URL text that the rules do not read; at the FPR of the rules, its recall is "
    f"{f3(LN['phiusiil']['recall_at_rules_fpr'])}. The remaining URLs need page content, domain age, or reputation data."
))
S(h2("Dataset Artifacts"))
S(body(
    "Every legitimate PhiUSIIL test URL is an https://www homepage, so the scheme and the prefix alone almost separate the classes. The rules treat HTTP "
    f"as a weak cue, but the score still leans on it: without that rule the ROC-AUC is {ROB['full']['roc_auc'] + AB['no_https']['d_auc']:.3f}, not {ROB['full']['roc_auc']:.3f}. The "
    "pooled lists have the path artifact of Section VI-D, so a simple shortcut scores a higher F1 than the rules on both sources, and the results without "
    "the artifacts are the more informative ones. The Tranco sites are homepages, so rules that read the path, such as file download, "
    "hex folder, long URL, lure words in the path, and the path-based hosting platforms added in v4, are not tested for false "
    "alarms on real deep links such as sign-in pages, shared documents, or software downloads. A file download alone is only "
    "suspicious, but it fires on legitimate installers as well, and the high URLhaus recall comes mostly from that rule. "
    "Reported precision should be read as optimistic for path-based rules."
))
S(h2("What the Verifier Guarantees"))
S(body(
    "The verifier guarantees that a gap in the knowledge base appears as a withheld sentence and not as an unsupported claim. Because the knowledge base covers all "
    "twenty-two rules, no sentence had to be withheld in the experiment. Tag coverage is not semantic entailment, and the exhibits are written for this "
    "system rather than drawn from a live threat feed. The guarantee is therefore about traceability: each sentence can be followed to a rule, a weight, and an exhibit."
))
S(h2("Limitations and Threats to Validity"))
S(body(
    "The rules, weights, thresholds, and lists were set by hand on development splits that share their sources with the test "
    f"splits. The brand list has {N_BRANDS} entries and the brand infrastructure lists are incomplete, so other brands rely on structural "
    "rules and some official domains may still be flagged. On the test split, v4 flags "
    f"{n(t4['alert']['fp'])} legitimate PhiUSIIL URLs against {n(t3['alert']['fp'])} for v3. Most of the new alerts are one-edit "
    "matches of the added brands on unrelated names. They appeared only on the test split, so they were left unfixed to keep "
    "the test numbers unbiased. Feeds and popularity lists change daily, and the lists will need upkeep. Phishing.Database "
    "marks a link active when it is still reachable, not when it has been re-confirmed as phishing, so some of its labels may "
    "be stale. The LightGBM features and settings were not tuned, and the language-model baseline covers one 3-billion-parameter model, one prompt, "
    f"and {LLM['n']} URLs. No human raters checked the report sentences, so the support results rest on tags, on two mechanical checks, and on a "
    "small judge model with measurable error."
))

S(h1("Conclusion"))
S(body(
    "PhishTrace shows that a detect, retrieve, verify, and report chain can work without any trained or generative model. On held-out PhiUSIIL "
    f"data, twenty-two readable rules reach a precision of {f3(t4['alert']['precision'])}, a recall of {f3(t4['alert']['recall'])}, and an F1 of "
    f"{f3(t4['alert']['f1'])}. On live feeds the pooled F1 is {f3(rw4['alert']['f1'])} with an alert on {pct(ext4['tranco']['alert_fpr'], 2)} percent of popular sites. A trained lexical "
    "classifier detects more on the same splits, and the comparison puts a number on the price of readable decisions: without the collection artifacts, "
    f"an F1 of {f3(t4['alert']['f1'])} against {f3(LN['phiusiil']['f1'])} on PhiUSIIL and {f3(LGB['rules']['realworld']['f1'])} against {f3(LNR['realworld']['f1'])} on the pooled lists. The rules "
    f"do better than a retrieval-augmented 3-billion-parameter model, at roughly {round(LLM['seconds']['median'] * 1000 / CUR['phiusiil']['ms_per_url'], -3):,.0f} times the speed. Most recall rests on two rules, and the exact "
    "weights matter little at the alert point. Next steps are weights taken from the development data, page-content and domain-age evidence through the same tool interface, "
    "a benchmark with legitimate deep links, and a human check of report sentences."
))

S(h5("Code Availability"))
S(body(
    "The implementation, evaluation script, and figure scripts are available at https://github.com/mahapara24/phistrace. "
    "Running python scripts/evaluate.py reproduces the detection and chain results from the public data files listed in the "
    "README. The scripts robustness.py, baseline_lightgbm.py, baseline_llm_rag.py, summarize_llm.py, and judge_support.py in the same folder reproduce the "
    "intervals, tests, ablation, baselines, and support check; the rule sets v1 to v3 are in the folder legacy. Running python scripts/evaluate.py --sensitive --out data/eval_v4_sensitive.json reproduces the sensitive "
    "variant. The results of the earlier rule sets are kept in "
    "data/eval_baseline.json, data/eval_v2.json, and data/eval_v3.json."
))
S(h5("References"))


def references_xml() -> str:
    return "".join(
        para("references", run(REFS[key]), '<w:ind w:start="17.70pt" w:hanging="17.70pt"/><w:jc w:val="left"/>') for key in _order
    )


# ----------------------------------------------------------------- assemble
def build(template: Path, out: Path) -> None:
    work = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(template) as archive:
        archive.extractall(work)
    for link in work.rglob("*"):
        if link.is_symlink():
            link.unlink()
    doc_path = work / "word" / "document.xml"
    xml = doc_path.read_text(encoding="utf-8")

    head = xml[: xml.index("<w:body>") + len("<w:body>")]
    if 'xmlns:r="' not in head:
        raise SystemExit("template lacks the r namespace")
    sect_paras = re.findall(r"<w:p [^>]*>(?:(?!</w:p>).)*?<w:sectPr.*?</w:sectPr></w:pPr>(?:(?!</w:p>).)*?</w:p>", xml, re.S)
    final_sect = re.search(r"<w:sectPr(?:(?!<w:sectPr).)*?</w:sectPr></w:body>", xml, re.S).group(0)[: -len("</w:body>")]
    title_sect = sect_paras[0]  # single column, first-page footer
    two_col = [p for p in sect_paras if 'w:num="2"' in p][0]
    two_col_sect = re.search(r"<w:sectPr.*?</w:sectPr>", two_col, re.S).group(0)
    author_sect = re.search(r"<w:sectPr.*?</w:sectPr>", sect_paras[1], re.S).group(0).replace('<w:cols w:num="3" w:space="36pt"/>', '<w:cols w:space="36pt"/>')

    title = para("papertitle", f'<w:r><w:rPr><w:kern w:val="48"/></w:rPr><w:t>{escape(TITLE)}</w:t></w:r>',
                 '<w:spacing w:before="5pt" w:beforeAutospacing="1" w:after="5pt" w:afterAutospacing="1"/>')
    author_runs = []
    for i, (line, italic) in enumerate(AUTHOR_LINES):
        if i:
            author_runs.append('<w:r><w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr><w:br/></w:r>')
        author_runs.append(run(line, italic=italic, size=18 if i else 22))
    author = para("Author", "".join(author_runs), '<w:spacing w:before="5pt" w:beforeAutospacing="1"/>')
    author_end = f'<w:p><w:pPr>{author_sect}</w:pPr></w:p>'

    abstract = para("Abstract", run("Abstract", italic=True) + run("—" + ABSTRACT))
    keywords = para("Keywords", run("Keywords—" + KEYWORDS))
    body_xml = "".join(SECTIONS) + references_xml()
    close_two_col = f'<w:p><w:pPr><w:pStyle w:val="references"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>{two_col_sect}</w:pPr></w:p>'

    new = head + title + title_sect + author + author_end + abstract + keywords + body_xml + two_col_sect + "</w:body></w:document>"  # last section is the two-column body; no empty trailing section
    doc_path.write_text(new, encoding="utf-8")

    # images
    rels_path = work / "word" / "_rels" / "document.xml.rels"
    rels = rels_path.read_text(encoding="utf-8")
    rels = re.sub(r'<Relationship Id="rId(9|10)"[^>]*/>', "", rels)
    media = work / "word" / "media"
    media.mkdir(exist_ok=True)
    for rid, path in _images:
        shutil.copy(path, media / path.name)
        rels = rels.replace(
            "</Relationships>",
            f'<Relationship Id="{rid}" Type="http://purl.oclc.org/ooxml/officeDocument/relationships/image" Target="media/{path.name}"/></Relationships>',
        )
    rels_path.write_text(rels, encoding="utf-8")
    ct_path = work / "[Content_Types].xml"
    ct = ct_path.read_text(encoding="utf-8")
    if 'Extension="png"' not in ct:
        ct = ct.replace("<Default Extension=\"xml\"", '<Default Extension="png" ContentType="image/png"/><Default Extension="xml"')
    ct_path.write_text(ct, encoding="utf-8")

    # footer placeholder (IEEE copyright line) is removed for a course submission
    footer = work / "word" / "footer1.xml"
    footer.write_text(re.sub(r"<w:t([^>]*)>[^<]*</w:t>", r"<w:t\1></w:t>", footer.read_text(encoding="utf-8")), encoding="utf-8")

    core = work / "docProps" / "core.xml"
    if core.exists():
        text = core.read_text(encoding="utf-8")
        text = re.sub(r"<dc:title>.*?</dc:title>|<dc:title/>", f"<dc:title>{escape(TITLE)}</dc:title>", text)
        text = re.sub(r"<dc:creator>.*?</dc:creator>|<dc:creator/>", "<dc:creator>Mahapara</dc:creator>", text)
        core.write_text(text, encoding="utf-8")

    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        ct_first = work / "[Content_Types].xml"
        archive.write(ct_first, "[Content_Types].xml")
        for file in sorted(work.rglob("*")):
            if file.is_file() and file != ct_first:
                archive.write(file, file.relative_to(work).as_posix())
    shutil.rmtree(work)
    print(f"wrote {out}  ({len(_order)} references, {len(_images)} figures)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    template = Path(sys.argv[1])
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "Mahapara_PhishTrace_IEEE.docx"
    build(template, target)
