"""Fill the IEEE A4 conference template with the PhishTrace paper.

Usage:  python3 paper/build_paper.py <template.docx> [out.docx]

The template's own styles (paper title, Author, Abstract, Keywords, Heading 1/2,
Body Text, table head/copy, figure caption, references) are reused, so the
section, table, figure, and reference numbers come from the template's
numbering. Citations are written as {key} and numbered in order of first use.
All numbers come from data/eval_results.json (v4), data/eval_v3.json, data/eval_v2.json,
data/eval_v4_sensitive.json, and data/eval_baseline.json. List sizes come from app/corpus.py.
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


def table(caption: str, header: list[str], rows: list[list[str]], widths_pt: list[float], note: str = "") -> str:
    grid = "".join(f'<w:gridCol w:w="{int(w * 20)}"/>' for w in widths_pt)
    borders = "".join(
        f'<w:{side} w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
        for side in ("top", "start", "bottom", "end", "insideH", "insideV")
    )

    def cell(text: str, width: float, head: bool) -> str:
        style = "tablecolhead" if head else "tablecopy"
        jc = '<w:jc w:val="center"/>' if head else ""
        return (
            f'<w:tc><w:tcPr><w:tcW w:w="{width}pt" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
            f'<w:p><w:pPr><w:pStyle w:val="{style}"/><w:keepNext/>{jc}</w:pPr>{rich(text)}</w:p></w:tc>'
        )

    def row(cells: list[str], head: bool) -> str:
        trpr = '<w:trPr><w:cantSplit/><w:tblHeader/><w:jc w:val="center"/></w:trPr>' if head else '<w:trPr><w:cantSplit/><w:jc w:val="center"/></w:trPr>'
        return "<w:tr>" + trpr + "".join(cell(c, w, head) for c, w in zip(cells, widths_pt)) + "</w:tr>"

    tbl = (
        f'<w:tbl><w:tblPr><w:tblW w:w="0pt" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:start w:w="2.5pt" w:type="dxa"/><w:end w:w="2.5pt" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
        f"<w:tblGrid>{grid}</w:tblGrid>" + row(header, True) + "".join(row(r, False) for r in rows) + "</w:tbl>"
    )
    out = para("tablehead", run(caption), "<w:keepNext/>") + tbl  # keep the caption on the table's page
    if note:
        out += para("tablefootnote", rich(note))
    else:
        out += '<w:p><w:pPr><w:spacing w:after="4pt"/></w:pPr></w:p>'
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
    "Phishing and malware URL detection is usually treated as binary classification, and the resulting label neither collects "
    "supporting evidence nor records an investigation. This paper presents PhishTrace, a framework that detects malicious URLs "
    "from the URL text and then investigates the decision without any trained or generative model. A transparent detector of "
    "twenty-two weighted rules produces a risk score and a verdict. The score then selects an investigation path for a chain of "
    "fixed agents that consult brand and suffix registries, retrieve exhibits from a local cybersecurity knowledge base by "
    "indicator tag, verify that each candidate sentence is covered by an exhibit, and publish only verified sentences in a report. "
    "Pooling phishing and malware feeds against the hundred thousand most popular domains, the final rule set reaches an accuracy "
    f"of {f3(rw4['alert']['accuracy'])}, a precision of {f3(rw4['alert']['precision'])}, a recall of {f3(rw4['alert']['recall'])}, "
    f"and a false alarm rate of {pct(rw4['alert']['fpr'], 2)} percent, {rw2['alert']['fpr'] / rw4['alert']['fpr']:.1f} times "
    f"lower than the first data-tuned rule set. On a held-out split of the PhiUSIIL dataset it reaches an accuracy of "
    f"{f3(t4['alert']['accuracy'])}, a precision of {f3(t4['alert']['precision'])}, and a ROC-AUC of {f3(t4['roc_auc'])}; "
    f"its recall of {f3(t4['alert']['recall'])} shows that many phishing URLs carry no warning sign in the URL text. In the "
    "investigation stage the agentic chain publishes no unsupported sentence and completes every required check, while a "
    f"single-retrieval baseline leaves {pct(ch['retrieval']['unsupported_rate'], 0)} percent of its sentences unsupported. A full "
    "investigation takes well under one millisecond per URL."
)
KEYWORDS = "phishing detection, malicious URL, rule-based detection, retrieval-augmented generation, agents, explainability, verification"

R = RULES
SECTIONS: list[str] = []
S = SECTIONS.append
IND = '<w:ind w:start="10pt" w:firstLine="0pt"/>'

S(h1("Introduction"))
S(body(
    "Phishing and malware delivery use deceptive URLs to obtain passwords and payment details or to install malicious programs, "
    "and they remain among the most common forms of online fraud, with millions of attacks observed each year {apwg,interisle}. Most published detectors treat the problem "
    "as binary classification: lexical, host, or page features are extracted and a classifier separates malicious from legitimate "
    "pages {sahoo,sahingoz,tang,safi}. A class label is a useful first signal, but it does not say which evidence supports the "
    "decision, whether that evidence was checked, or what an analyst should do next."
))
S(body(
    "Retrieval-augmented generation (RAG) attaches retrieved context to an answer {lewis}, and agent frameworks let a system "
    "choose tools step by step {yao}. Recent phishing work uses retrieval and, in one case, multiple agents, usually with a large language model in the loop "
    "{nicklas,li26}. Two problems remain. First, one retrieve-and-answer step follows a fixed path and cannot decide which "
    "evidence is still missing. Second, when a generative model writes the report, nothing guarantees that each sentence "
    "is supported by the retrieved text."
))
S(body(
    "This study keeps the detect, retrieve, verify, and report chain of an agentic RAG system but builds every stage from "
    "transparent, deterministic components. No classifier is trained and no generative model is called. The detector is a "
    "table of weighted rules that an analyst can read; the agents are fixed functions with tools; and the verifier is a "
    "separate function that withholds any sentence no exhibit covers. The design favors auditability over raw accuracy, and "
    "the evaluation measures how much detection quality that choice costs on both benchmark and real-world data."
))
S(body("The contributions of this paper are as follows."))
for item in (
    "*A transparent URL detector for phishing and malware.* Twenty-two weighted rules, including five added in this work "
    "(free hosting {interisle} and dynamic DNS hosts, machine-generated labels, glued www or com labels, program or archive downloads, and "
    "per-victim hex folders), one-edit typosquat matching, and mixed-script homograph checks, produce a score and a three-way verdict.",
    "*A score-driven agentic investigation chain.* The score selects which registries and retrievals run; a separate verifier "
    "keeps only sentences that an exhibit covers; and the report publishes only verifier output.",
    "*A reproducible evaluation on benchmark and real-world data.* The detector is measured on hash-based held-out splits of "
    "PhiUSIIL {prasad}, two phishing feeds {openphish,phishdb}, a malware feed {urlhaus}, and the Tranco top sites {tranco}, and the "
    "chain is compared with rules-only and retrieval-only baselines on unsupported-claim rate, evidence support, completeness, and latency.",
):
    S(para("BodyText", rich(item), IND))

S(h1("Related Work"))
S(h2("Machine-Learning URL and Website Detection"))
S(body(
    "Feature-based detection has a long history. Mohammad et al. {mohammad12,uci327} defined widely used website features, "
    "and surveys {sahoo,tang,safi,access25} describe lexical, host-based, and content features combined with classifiers "
    "such as logistic regression, decision trees, random forests, support vector machines, and gradient boosting. Sahingoz "
    "et al. {sahingoz} reported strong results from URL text alone. Prasad and Chandra {prasad} released PhiUSIIL, a large "
    "URL dataset with similarity-index features. These systems output a label but do not retrieve, verify, or report evidence."
))
S(h2("Heuristic and Lexical Detection"))
S(body(
    "Before trained models dominated, phishing was detected with interpretable heuristics. Garera et al. {garera} measured "
    "URL obfuscation patterns such as brand names in subdomains and IP hosts, and CANTINA {cantina} combined term "
    "statistics with heuristics. Studies of combosquatting {kintis} and typosquatting {agten} show that attackers attach "
    "words to a brand name or change one character of it. These findings motivate the brand rules used here."
))
S(h2("Retrieval and Agents for Phishing Analysis"))
S(body(
    "Nicklas et al. {nicklas} added retrieved context to open language models for phishing email detection, but the output "
    "is still a class label. Li et al. {li26} used multi-agent RAG to explain phishing intention. Neither work joins a URL "
    "detector, retrieved evidence, and a verifier that controls what the report may claim. Table I summarizes the gap that "
    "this paper addresses."
))
S(table(
    "Comparison with Prior Work",
    ["Study", "Detector", "Retrieval", "Verifier", "Report"],
    [
        [cite("Prasad {prasad}"), "ML", "No", "No", "No"],
        [cite("Sahingoz {sahingoz}"), "ML", "No", "No", "No"],
        [cite("Nicklas {nicklas}"), "LLM", "Yes", "No", "Label"],
        [cite("Li {li26}"), "LLM (intent)", "Yes", "Partial‡", "Text"],
        ["This work", "Rules", "Yes", "Yes", "Verified"],
    ],
    [62, 44, 44, 44, 46],
    "‡Aggregates agent outputs but does not check each report sentence against retrieved evidence. Li et al. classify the intent of known phishing pages rather than detect phishing.",
))

S(h1("Research Questions and Objectives"))
S(body(
    "The study follows one chain, detection then retrieval then agents, and asks one question at each link. The questions "
    "and objectives of the proposal were revised so that detection uses transparent rules instead of trained classifiers."
))
for label, text in (
    ("RQ1.", "How effectively can a transparent rule-based detector separate phishing and malware URLs from legitimate ones, "
             "so that its score can serve as the initial risk signal?"),
    ("RQ2.", "Does retrieved cybersecurity evidence support and explain that signal better than the rule output alone?"),
    ("RQ3.", "Do agents that choose tools from the score and verify evidence separately from the report reduce unsupported "
             "claims and increase investigation completeness compared with non-agentic retrieval?"),
):
    S(para("BodyText", run(label + " ", bold=True) + rich(text), IND))
S(body(
    "*RO1* builds and tunes the rule detector on development splits and measures it on held-out benchmark and real-world data. "
    "*RO2* builds a tagged knowledge base and measures whether retrieved exhibits cover each finding. *RO3* implements the detect, "
    "plan, tool, verify, and report agents and compares three modes on the metrics in Section IV-G."
))

S(h1("Methodology"))
S(body(
    "Fig. 1 shows the pipeline. The system reads only the URL string; it never opens the page, follows a redirect, or "
    "contacts the host, so an investigation cannot trigger the attack it studies."
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
    "name on a country-code suffix or on .com, .net, or .org (hsbc.fr) is read as the brand's own domain; on a newer generic "
    "suffix (interac.tax) it is not, because anyone can register it. A token "
    "matches when it equals the brand, starts with it (a common form of combosquatting {kintis}), or, for names of six or more letters, differs "
    "by one insertion, deletion, substitution, or adjacent swap (typosquatting {agten}). Brands that are also ordinary words, "
    "such as apple and steam, match a longer token only when the extra text is an account word such as id, login, or support, "
    "and short brand names such as DHL or DPD match only a whole token. "
    "A Punycode label fires only when it decodes to Latin letters mixed with letters of another script, the homograph form; a "
    "name written wholly in Thai, Cyrillic, or accented Latin does not fire."
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
    [66, 34, 140],
    "†Rules added after v1. Nine smaller rules (long URL, very long URL, depth, hyphens, digits, encoding, double slash, explicit HTTP, hex folder†) weigh 8 to 12.",
))
S(h2("Verdict Decision"))
S(body(
    "The verdict is *phishing / malicious* when a strong rule fires (brand mismatch, user information, or a mixed-script label), "
    "when a host signal fires together with a corroborating one (a free host with lure words or a machine-generated label; an "
    "abused suffix, raw IP, or shortener with lure words; a file download with a raw IP, unusual port, free host, abused suffix, "
    "or machine-generated label), when a program is served raw from a user file host such as raw.githubusercontent.com, or when "
    "the score reaches 40. The verdict is *suspicious* when a medium rule fires, when two weak shape cues fire together, or when "
    "the score reaches 21. One weak cue alone, such as an abused suffix, a long URL, a digit-heavy host, or explicit HTTP, is not "
    "an alert, because each is common on popular legitimate sites. Otherwise the verdict is *not phishing*. Two operating points "
    "are reported: *strict*, where only the phishing verdict counts as positive, and *alert*, where suspicious also counts."
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
    "score below 21, a standard path from 21 to 49, and a deep path at 50 or above; a brand token or an abused suffix also "
    "opens its registry on a lower path. The *tool* role consults the selected registries and retrieves exhibits by the "
    "tag of each fired rule, plus a low-score exhibit on the light path. The *verifier* is a separate function: a candidate "
    "sentence is published only if at least one cited exhibit carries the tag of the rule that produced it. The *reporter* "
    "receives only verified sentences and adds protective recommendations. The next step therefore depends on the detector "
    "output, each evidence source is a separate tool, and verification is kept apart from report writing."
))
S(h2("Baselines"))
S(body(
    "Two baselines use the same detection signal. *Rules only* publishes the fired-rule sentences and a class label with no "
    "retrieval or verification. *Retrieval only* runs one search over the URL words, attaches the same results to every "
    "sentence, and publishes them without verification. This mirrors a single-step RAG pipeline."
))
S(h2("Evaluation Metrics"))
S(body(
    "Detection is measured with accuracy, precision, recall, F1 score, false positive rate (FPR), ROC-AUC, and PR-AUC. "
    "ROC-AUC uses the uncapped score with average ranks for ties, and PR-AUC is average precision over score thresholds. "
    "For investigation, the *unsupported-claim rate* is the share of candidate sentences that no cited exhibit covers; "
    "*evidence support* is the share of published sentences that are covered; and *completeness* is the share of required "
    "checks that ran, from a nine-item checklist whose required items depend on the score (for example, the brand registry "
    "is required when a brand token is present). Latency is wall-clock time per investigation."
))

S(h1("Experimental Setup"))
S(h2("Datasets"))
S(body(
    f"PhiUSIIL {{prasad}} provides 235,795 labeled URLs; {n(N_ALL)} could be parsed as http or https URLs. Four real-world lists "
    "add data PhiUSIIL never saw: a snapshot of OpenPhish {openphish}; active links from Phishing.Database {phishdb}; online "
    "malware URLs derived from URLhaus {urlhaus}, taken from the malware-filter urlhaus-filter list {urlhausmirror}, which "
    "republishes URLhaus online entries twice daily without the URL scheme; the mirror lets the evaluation be reproduced without "
    "a (free) abuse.ch Auth-Key, which URLhaus bulk downloads now require; and the top 100,000 domains of the Tranco list {tranco} "
    "generated on 7 November 2026 (list ID 94P72, https://tranco-list.eu/list/94P72), read as https homepages, as popular safe "
    "sites. Every URL or domain is assigned to a split by its MD5 hash: three of ten buckets form the development split and the "
    "rest form the held-out test split. OpenPhish is used only for testing. Table III gives the test sizes; the larger lists are "
    "sampled with a fixed seed."
))
S(table(
    "Evaluation Data (Test Splits)",
    ["Set", "Malicious", "Safe", "Use"],
    [
        ["PhiUSIIL", n(t4["phishing_n"]), n(t4["legitimate_n"]), "Benchmark"],
        ["OpenPhish", n(ext4["openphish"]["n"]), "0", "Phishing recall"],
        ["Phishing.Database", n(ext4["phishing_database"]["n"]), "0", "Phishing recall"],
        ["URLhaus", n(ext4["urlhaus"]["n"]), "0", "Malware recall"],
        ["Tranco top-100k", "0", n(ext4["tranco"]["n"]), "False alarms"],
    ],
    [70, 50, 50, 70],
    f"PhiUSIIL development split: {n(d4['phishing_n'])} phishing and {n(d4['legitimate_n'])} legitimate URLs.",
))
S(h2("Rule Development Protocol"))
S(body(
    "The first rule set (v1, 17 rules) was written from the literature before any data was inspected. Version 2 (20 rules) was "
    "built by studying misses and false alarms on the PhiUSIIL development split: three new rules, typosquat matching, more "
    "brands, suffixes {interisle}, and lure words, and new decision combinations. Version 3 (22 rules) was built after adding the "
    "real-world development splits. It fixed false alarms on brand infrastructure (for example, v2 flagged every "
    "raw.githubusercontent.com link as a GitHub lookalike) and on native-script internationalized names; added the file-download "
    "and hex-folder rules and dynamic DNS hosts for malware and kit hosting; and stopped single weak cues from raising an alert. "
    "Version 4 keeps the 22 rules of v3 and was built from an analysis of the phishing URLs that v3 missed on the development "
    "splits. It widens the lists rather than the rules: cloud storage buckets, IPFS gateways, and shared hosts, including "
    "platforms whose pages sit in the path (sites.google.com, Google Forms, ipfs.io/ipfs/); more shorteners, which now fire only "
    "when a short code follows the host; and more brands (parcel carriers, banks, cryptocurrency, and games). A brand was kept "
    "only when it recovered missed phishing on the development splits and raised at most one or two alerts on popular domains; "
    "short or common-word candidates such as line, att, and meta were rejected for that reason. V4 also closed a gap in which "
    "an exact brand name on a new generic suffix, such as interac.tax, was read as the brand's own domain. "
    "Test splits were used only for the final measurement."
))
S(h2("Implementation"))
S(body(
    "PhishTrace is written in Python 3 with FastAPI for the web interface and only the standard library for detection, "
    "retrieval, and agents. No machine-learning, embedding, or language-model library is installed. The evaluation script "
    "and the investigation chain run in a single process on a laptop CPU."
))

S(h1("Results"))
S(h2("Benchmark Detection (RQ1)"))
S(body(
    f"Table IV reports the four rule sets on the held-out PhiUSIIL test split. At the alert operating point, recall rises from "
    f"{f3(t1['alert']['recall'])} in v1 to {f3(t2['alert']['recall'])} in v2, while the false positive rate falls from "
    f"{pct(t1['alert']['fpr'], 2)} to {pct(t2['alert']['fpr'], 2)} percent. Version 3 gives up some recall "
    f"({f3(t3['alert']['recall'])}) because single weak cues no longer raise an alert, and cuts the false positive rate to "
    f"{pct(t3['alert']['fpr'], 3)} percent; the next subsection shows why that trade pays off on real traffic. Version 4 "
    f"recovers most of that recall ({f3(t4['alert']['recall'])}) and raises accuracy from {f3(t3['alert']['accuracy'])} to "
    f"{f3(t4['alert']['accuracy'])} and F1 from {f3(t3['alert']['f1'])} to {f3(t4['alert']['f1'])}, at a false positive rate "
    f"of {pct(t4['alert']['fpr'], 3)} percent and a precision of {f3(t4['alert']['precision'])}. ROC-AUC is "
    f"{f3(t4['roc_auc'])} in v4 against {f3(t1['roc_auc'])} in v1 (Fig. 2). The development F1 of "
    f"{f3(d4['alert']['f1'])} is close to the test F1 of {f3(t4['alert']['f1'])}, which suggests that the rule changes did "
    "not overfit the development split."
))
S(table(
    "Detection on the PhiUSIIL Test Split",
    ["Rules", "Point", "Acc.", "Prec.", "Rec.", "F1", "FPR"],
    [
        [tag, point.capitalize(), f3(t[point]["accuracy"]), f3(t[point]["precision"]), f3(t[point]["recall"]), f3(t[point]["f1"]), f"{t[point]['fpr']:.4f}"]
        for tag, t in (("v1", t1), ("v2", t2), ("v3", t3), ("v4", t4))
        for point in ("strict", "alert")
    ],
    [26, 32, 36, 36, 36, 36, 38],
    f"ROC-AUC / PR-AUC: v1 {f3(t1['roc_auc'])} / {f3(t1['pr_auc'])}; v2 {f3(t2['roc_auc'])} / {f3(t2['pr_auc'])}; v3 {f3(t3['roc_auc'])} / {f3(t3['pr_auc'])}; v4 {f3(t4['roc_auc'])} / {f3(t4['pr_auc'])}. n = {n(N_TEST)}.",
))
S(figure(HERE / "fig2_v1_v2.png", "Alert-point accuracy, precision, recall, and F1 score with ROC-AUC on the PhiUSIIL test split for the four rule sets."))
S(h2("Real-World Phishing, Malware, and Popular Sites (RQ1)"))
S(body(
    "Table V and Fig. 3 report the real-world lists at the alert point. On the Tranco top 100,000 domains, v2 raises an alert "
    f"on {pct(ext2['tranco']['alert_fpr'])} percent of popular sites, mostly because of a single abused suffix, a digit-heavy name, "
    f"or a brand token on brand infrastructure; v3 lowers this to {pct(ext3['tranco']['alert_fpr'])} percent, a "
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
    ["Measure", "v2", "v3", "v4"],
    [
        [label, fmt(a), fmt(b), fmt(c)]
        for label, fmt, (a, b, c) in [
            ("OpenPhish recall", f3, [e["openphish"]["alert_recall"] for e in (ext2, ext3, ext4)]),
            ("Phishing.Database recall", f3, [e["phishing_database"]["alert_recall"] for e in (ext2, ext3, ext4)]),
            ("URLhaus recall", f3, [e["urlhaus"]["alert_recall"] for e in (ext2, ext3, ext4)]),
            ("URLhaus strict recall", f3, [e["urlhaus"]["strict_recall"] for e in (ext2, ext3, ext4)]),
            ("Tranco false alarms (%)", lambda x: pct(x, 2), [e["tranco"]["alert_fpr"] for e in (ext2, ext3, ext4)]),
            ("Pooled accuracy", f3, [r["alert"]["accuracy"] for r in (rw2, rw3, rw4)]),
            ("Pooled precision", f3, [r["alert"]["precision"] for r in (rw2, rw3, rw4)]),
            ("Pooled recall", f3, [r["alert"]["recall"] for r in (rw2, rw3, rw4)]),
            ("Pooled F1", f3, [r["alert"]["f1"] for r in (rw2, rw3, rw4)]),
        ]
    ],
    [105, 45, 45, 45],
    f"Pooled: {n(rw4['malicious_n'])} malicious URLs (OpenPhish, Phishing.Database, URLhaus) against {n(rw4['safe_n'])} Tranco domains.",
))
S(figure(HERE / "fig3_realworld.png", "Alert-point recall on the three malicious lists and false alarms on the Tranco top 100,000 domains (shaded) for v2, v3, and v4."))
S(h2("Contribution of Individual Rules"))
S(body(
    "Table VI gives the share of PhiUSIIL test URLs on which the most frequent rules fire. The free-hosting rule fires on "
    f"{R['free_hosting']['phishing_pct']:.1f} percent of phishing URLs and on almost no legitimate ones. Explicit HTTP fires on "
    "about half of the phishing URLs and never on legitimate ones; Section VII explains why it is nevertheless kept weak."
))
S(table(
    "Rule Firing Rates on the PhiUSIIL Test Split (Percent)",
    ["Rule", "Phishing", "Legitimate"],
    [
        [R[k]["label"], f"{R[k]['phishing_pct']:.2f}", f"{R[k]['legitimate_pct']:.2f}"]
        for k in ("no_https", "free_hosting", "suspicious_tld", "random_label", "digit_heavy_host", "lure_terms", "brand_mismatch")
    ],
    [110, 65, 65],
))
S(h2("Evidence and Investigation (RQ2 and RQ3)"))
S(body(
    f"All three modes were run on a seeded, class-balanced sample of {CUR['chain']['n']} PhiUSIIL test URLs (Table VII). Rules only "
    "publishes every sentence without an exhibit, so its unsupported-claim rate is 100 percent and it completes "
    f"{pct(ch['rules']['completeness'])} percent of the required checks. A single retrieval pass attaches exhibits, but "
    f"only {pct(ch['retrieval']['evidence_support'])} percent of its published sentences are covered by a matching exhibit "
    f"and it completes {pct(ch['retrieval']['completeness'])} percent of the checks, because it never opens the registries "
    "or runs the verifier. The agentic chain publishes no unsupported sentence and completes every required check, using "
    f"on average {ch['agentic']['exhibit_count']:.2f} exhibits per report. These results answer RQ2 and RQ3: evidence "
    "retrieved by indicator tag supports every finding, while untargeted retrieval mostly does not."
))
S(table(
    "Investigation Modes on 1,000 Test URLs",
    ["Mode", "Unsupp.", "Support", "Compl.", "Time (ms)"],
    [
        [label, pct(ch[mode]["unsupported_rate"]), pct(ch[mode]["evidence_support"] or 0), pct(ch[mode]["completeness"]), f"{ch[mode]['agent_ms']:.3f}"]
        for mode, label in (("rules", "Rules only"), ("retrieval", "Retrieval only"), ("agentic", "Agentic chain"))
    ],
    [64, 44, 44, 44, 44],
    "Unsupp. = unsupported-claim rate, Support = evidence support, Compl. = completeness, all in percent. Time is the mean chain time after detection.",
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
    "The gate introduced in v3, which ignores single weak cues, is a deliberate operating choice. A sensitive variant of v4 that "
    "keeps every v4 rule but lets any single cue raise an alert, as v2 did, reaches a PhiUSIIL F1 of "
    f"{f3(ts['alert']['f1'])} and a pooled real-world recall of {f3(rws['alert']['recall'])}, "
    f"but it raises an alert on {pct(exts['tranco']['alert_fpr'])} percent of popular sites, against "
    f"{pct(ext4['tranco']['alert_fpr'], 2)} percent for v4. The precise gate was chosen because "
    "a tool that flags several of every hundred popular sites trains users to ignore it. Both variants are produced by the same "
    "evaluation script."
))
S(h2("What Limits Recall"))
S(body(
    f"The v4 detector still labels {n(MISSED)} PhiUSIIL test phishing URLs ({pct(MISSED / t4['phishing_n'])} percent) as not "
    "phishing. In the analysis of v3 misses on the development splits that led to v4, about half fired no rule at all, and most "
    "of the rest fired a single weak cue such as explicit HTTP, a long URL, or an abused suffix. Many are bare registered "
    "domains such as http://www.example-shop.com, with no brand token, lure word, or unusual structure. Broader matching was "
    "tested there and rejected: one-edit typos of brand infrastructure names and alerts on an abused suffix alone recovered "
    "thousands of misses but multiplied false alarms on popular sites. A detector that reads only "
    "the URL text cannot separate these from legitimate pages; page content, domain age, or reputation data would be needed. "
    "This is a limit of URL-only evidence rather than of the rule format."
))
S(h2("Dataset Artifacts"))
S(body(
    "Almost every legitimate URL in PhiUSIIL is an https homepage, so explicit HTTP alone would separate the classes there with "
    "high accuracy; the rules treat HTTP as a weak cue so the score does not lean on that artifact. None of the legitimate "
    "development URLs has a path, and the Tranco sites are also homepages, so rules that read the path, such as file download, "
    "hex folder, long URL, lure words in the path, and the path-based hosting platforms added in v4, are not tested for false "
    "alarms on real deep links such as sign-in pages, shared documents, or software downloads. A file download alone is only "
    "suspicious, but it fires on legitimate installers as well, and the high URLhaus recall comes mostly from that rule. "
    "Reported precision should be read as optimistic for path-based rules."
))
S(h2("What the Verifier Guarantees"))
S(body(
    "The zero unsupported-claim rate of the agentic chain holds by construction: the verifier blocks any sentence that no "
    "exhibit covers. Because the knowledge base covers all twenty-two rules, no sentence had to be withheld in the experiment. "
    "The value of the comparison is that it shows how often the baselines publish unsupported text, and that coverage gaps "
    "in the knowledge base would surface as withheld sentences rather than as unsupported claims. Support here means tag "
    "coverage, not semantic entailment, and the exhibits are written for this system rather than drawn from a live threat feed."
))
S(h2("Limitations and Threats to Validity"))
S(body(
    "The rules, weights, thresholds, and lists were set by hand on development splits that share their sources with the test "
    f"splits. The brand list has {N_BRANDS} entries and the brand infrastructure lists are incomplete, so other brands rely on structural "
    "rules and some official domains may still be flagged. On the test split, v4 flags "
    f"{n(t4['alert']['fp'])} legitimate PhiUSIIL URLs against {n(t3['alert']['fp'])} for v3; most of the new alerts are one-edit "
    "matches of the added brands on unrelated names. They were seen only on the test split and were deliberately left unfixed, so "
    "that the test numbers stay unbiased. Feeds and popularity lists change daily and the lists need "
    "maintenance. Phishing.Database marks a link active when it is still reachable, not when it is re-confirmed as phishing, "
    "so some of its labels may be stale. Trained classifiers and language-model baselines from the original proposal were deliberately left out to "
    "keep every decision auditable; comparing against them is future work."
))

S(h1("Conclusion"))
S(body(
    "PhishTrace shows that the detect, retrieve, verify, and report chain of an agentic RAG system can be built without any "
    "trained or generative model. A readable set of twenty-two rules reaches an accuracy of "
    f"{f3(t4['alert']['accuracy'])}, a precision of {f3(t4['alert']['precision'])}, and a ROC-AUC of {f3(t4['roc_auc'])} on "
    f"held-out PhiUSIIL data, flags {pct(ext4['urlhaus']['alert_recall'], 0)} percent of live malware URLs, mostly as risky "
    f"downloads, and raises an alert on only {pct(ext4['tranco']['alert_fpr'])} percent of the most popular sites, giving a "
    f"pooled real-world accuracy of {f3(rw4['alert']['accuracy'])} and F1 of {f3(rw4['alert']['f1'])}. Its main limit is "
    "recall: URL text alone cannot reveal phishing hosted on plain-looking domains. The score-driven agents complete every "
    "required check and publish only verified sentences, "
    "while a single retrieval pass leaves most sentences unsupported. Future work will add page-content and domain-age evidence "
    "through the same tool interface and compare the chain with trained and language-model baselines."
))

S(h5("Code Availability"))
S(body(
    "The implementation, evaluation script, and figure scripts are available at https://github.com/mahapara24/phistrace. "
    "Running python scripts/evaluate.py reproduces every number in this paper from the public data files listed in the "
    "README; adding --sensitive reproduces the sensitive variant. The results of the earlier rule sets are kept in "
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
