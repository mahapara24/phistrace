# PhishTrace references hold up; six claims need repair

All 22 references in the PhishTrace paper are real. For 20 of them, the authors, title, venue and year are correct. Numbering, in-text format and the citation-free abstract already follow the 2025 IEEE Reference Guide. The paper is not yet ready to submit, though, because of six must-fix problems. They are one wrong year, one outdated citation, three places where the wording claims more than the source says, and one data-terms problem:

- **UCI "Phishing Websites" [17] is dated 2015 but should be 2012.**
- **PhishIntentionLLM [10] is cited as an arXiv preprint although it was formally published by Springer in 2026.** Its Table I row also calls it an LLM detector, which it is not.
- **APWG [1] does not support "most reported forms of online fraud".**
- **Nicklas et al. [9] uses no agents.** The sentence citing [9] and [10] says recent work "uses both" RAG and agents.
- **The URLhaus sentence and its reference describe the data path in a way that invites a terms-of-use question.**
- **The public repository the paper links to shows verbatim OpenPhish URLs that OpenPhish's terms do not allow you to redistribute.**

Each fix is an edit of one sentence or one string. The paste-ready strings are at the end of this report. Below the must-fix tier are some provenance gaps that a careful reviewer would notice: the Tranco list ID, the feed snapshot dates, and the uncited phrase "written from the literature". Below those is the polish: DOIs, abbreviations, italics and layout. Do the polish only after the first two tiers are done.

## All 22 references exist, and the numbering already follows IEEE

Each entry was checked against Crossref, DataCite, arXiv, the publishers' pages or the live site. None is fabricated or not found. Seven are fully correct as written:

- Prasad and Chandra [11] ([Crossref](https://api.crossref.org/works/10.1016/j.cose.2023.103545))
- Mohammad et al. [16] ([Huddersfield Pure](https://pure.hud.ac.uk/en/publications/an-assessment-of-features-related-to-phishing-websites-using-an-a/))
- Sahoo et al. [3] ([arXiv](https://arxiv.org/abs/1701.07179))
- Kustiawan and Ghauth [18] ([Crossref](https://api.crossref.org/works/10.1109/ACCESS.2025.3630334))
- Lewis et al. [7] ([NeurIPS BibTeX](https://proceedings.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Bibtex.bib))
- Yao et al. [8] ([arXiv](https://arxiv.org/abs/2210.03629))
- Le Pochat et al. [15] ([NDSS](https://www.ndss-symposium.org/ndss-paper/tranco-a-research-oriented-top-sites-ranking-hardened-against-manipulation/))

The PhiUSIIL count in the Datasets section is exact: **134,850 legitimate + 100,945 phishing = 235,795** ([UCI 967](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset)). Every claim made about prior work holds up against the source:

- **Sahingoz [4] "strong results from URL text alone":** 97.98% with NLP-only URL features ([Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.eswa.2018.09.029?fields=abstract)).
- **Garera [19] obfuscation types:** the four-type taxonomy includes IP hosts and brand-laden host names ([PhishDef summary](https://ar5iv.arxiv.org/html/1009.2275)).
- **CANTINA [20] "term statistics with heuristics":** TF-IDF signatures plus heuristics ([CMU PDF](https://www.cs.cmu.edu/~jasonh/publications/www2007-cantina-final.pdf)).
- **Agten [22] one-character typos:** Damerau-Levenshtein distance 1 ([NDSS PDF](https://www.ndss-symposium.org/wp-content/uploads/2017/09/01_3_1.pdf)).
- **Nicklas [9] output:** a boolean label parsed from JSON ([URAI PDF](https://journals.hs-offenburg.de/index.php/urai/article/download/23/20)).

| # | Key | Verdict | What is wrong |
|---|---|---|---|
| [1] | apwg | Minor + claim | Cites a series, not one report. Does not support "most reported". No access date |
| [2] | interisle | Minor | Cover subtitle is "A Study of…", not "An annual study of…". Full date is 23 Jul. 2024 |
| [3] | sahoo | Correct | Only the arXiv field order is off |
| [4]–[6] | sahingoz, tang, safi | Correct | No DOIs or months. Journal names not abbreviated |
| [7], [8] | lewis, yao | Correct | [7] lacks "Proc." and the abbreviation |
| [9] | nicklas | Minor | Missing pp. 159–166 and doi 10.60643/urai.v2024p159 |
| [10] | li26 | **Must fix** | Published version exists (Springer, 2026, pp. 88–106). Table I cells wrong |
| [11] | prasad | Correct | Journal name not abbreviated |
| [12] | openphish | **Terms issue** | No snapshot date. Repository redistributes feed URLs |
| [13] | phishdb | Minor | No maintainers, version or access date |
| [14] | urlhaus | **Must fix** | Mirror is folded into a free-text parenthetical. Key wording invites a terms question |
| [15] | tranco | Minor | No DOI. Paper never names the list used (ID 94P72) |
| [16] | mohammad12 | Correct | Could add location and month |
| [17] | uci327 | **Must fix** | Year 2015 should be 2012. No DOI |
| [18] | access25 | Correct | — |
| [19]–[22] | garera, cantina, kintis, agten | Correct details | DOIs missing. [21] missing pp. 569–586 |

The citation mechanics are correct, and that is the main good news. `cite()` in [build_paper.py](file:///home/maha/Documents/Dst_project/paper/build_paper.py) numbers each key the first time it is used. The PDF runs monotonically from [1] to [22] with no gaps. The abstract and keywords carry no citations. Every key in Table I is cited in the body before the table appears. All 22 REFS keys are used, and an undefined key would raise a `KeyError`, so it could not slip through silently. **Do not "fix" "[3], [4], [5], [6]" into "[3]–[6]".** The current IEEE Reference Guide says ranges are no longer used and every number is written out. It also places citations "on the line, in square brackets, inside the punctuation", which the paper already does ([IEEE Reference Guide 2025](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)). One trap to watch: `cite()` keeps the order in which you write keys inside a group. If you write a new group as `{tranco,prasad}`, it prints "[15], [11]". Write new groups in ascending order.

## Six must-fix errors, each a one-sentence edit

**1. Wrong year on [17].** DataCite and UCI both give the UCI "Phishing Websites" dataset a creation year of **2012**. The 25 March 2015 date is only when the dataset was donated. UCI's own recommended citation uses 2012 and **doi 10.24432/C51W2X** ([UCI page](https://archive.ics.uci.edu/dataset/327/phishing+websites), [DataCite](https://api.datacite.org/dois/10.24432/C51W2X)). The reference also prints the author as "R. Mohammad", while [16] prints "R. M. Mohammad". This is the same person, Rami M. Mohammad, so use "R. M. Mohammad" in both.

**2. Outdated citation and inaccurate Table I row for [10].** The arXiv details of PhishIntentionLLM are correct. However, the paper was published as a chapter in *Digital Forensics and Cyber Crime* (ICDF2C 2025), Springer LNICST, **2026, pp. 88–106, doi 10.1007/978-3-032-22545-0_6** ([Crossref](https://api.crossref.org/works/10.1007/978-3-032-22545-0_6)). IEEE style says to cite the published version once it exists ([IEEE RG 2025](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)). Your key is even named `li26`.

The Table I row has two problems:

- **"Detector = LLM" is not accurate.** The system assumes its input is already phishing and classifies *why* (credential theft, financial fraud, and so on). It does not detect phishing versus benign.
- **"Verifier = No" is open to challenge.** The system has a "Validation Agent" that "integrates specialist findings, resolves conflicts, weighs evidence" ([arXiv HTML](https://arxiv.org/html/2507.15419v1)). That agent combines the other agents' outputs. It does not check whether each sentence is grounded in evidence, so you can defend "No", but only if Table I defines "verifier".

Change the row to `[cite("Li {li26}"), "LLM (intent)", "Yes", "Partial‡", "Text"]` and add this table note: "‡Aggregates agent outputs but does not check each report sentence against retrieved evidence."

**3. "Most reported forms of online fraud" goes beyond [1].** APWG's trends reports count attacks, for example "3.8 million phishing attacks" in 2025 ([APWG Q4 2025](https://docs.apwg.org/reports/apwg_trends_report_q4_2025.pdf)). They never rank phishing against other kinds of fraud. Interisle calls phishing "the most commonly used tactic" in cybercrime and cites FBI complaint figures ([Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)). That is close to your claim, but it is not about "most reported". The quickest safe fix is to reword line 263:

> "...and they remain among the most common forms of online fraud, with millions of attacks observed each year {apwg,interisle}."

While you are editing this reference, replace the APWG series citation ("2024–2025", pointing to a landing page that changes every quarter) with the specific Q4 2025 report. That report gives the totals for both 2024 and 2025.

**4. "Recent phishing work uses both" RAG and agents, but [9] has no agents.** Nicklas et al. insert retrieved phishing examples into a single prompt. Only [10] is multi-agent ([URAI PDF](https://journals.hs-offenburg.de/index.php/urai/article/download/23/20)). Reword line 270:

> "Recent phishing work uses retrieval and, in one case, multiple agents, usually with a large language model in the loop {nicklas,li26}."

**5. The URLhaus sentence understates the access terms and misdescribes the data.** The claim that bulk downloads now need a key is **true**. The old unauthenticated URLs return HTTP 410, and the URLhaus API documentation requires an Auth-Key ([URLhaus API](https://urlhaus.abuse.ch/api/)). But the key is free.

The current abuse.ch Terms of Use (updated 21 Oct 2026) say three things that matter here ([abuse.ch Terms](https://abuse.ch/terms-of-use/)):

- Access is granted only to authenticated users.
- URLhaus is **not** among the feeds placed under CC0.
- Using the data to "train, or otherwise improve any artificial intelligence model" is barred without consent.

The mirror you used also says it is "not endorsed by Abuse.ch". It rewrites entries into adblock syntax and **removes the http/https scheme**, and it treats Tranco-popular domains differently from other domains ([urlhaus-filter README](https://gitlab.com/malware-filter/urlhaus-filter)). As a result:

- **"Online malware URLs from URLhaus, read from the mirror because the download requires an account key" reads like a workaround of an access control.**
- **Your "Explicit HTTP" rule cannot fire on these items the way it would on raw URLhaus URLs.**

A rule-based system whose rules were only inspected on a development split does not plausibly count as "training" an AI model. Still, never call this data CC0. Give the mirror its own reference and replace lines 450–452 with:

> "...online malware URLs derived from URLhaus {urlhaus}, taken from the malware-filter urlhaus-filter list {urlhausmirror}, which republishes URLhaus online entries twice daily without the URL scheme; the mirror lets the evaluation be reproduced without a (free) abuse.ch Auth-Key, which URLhaus bulk downloads now require..."

The cleanest alternative is to register for the free key and download the export directly. That is not realistic before tomorrow.

**6. The linked repository redistributes OpenPhish data.** OpenPhish's Terms of Use allow academic research. Without written permission, though, they forbid any user to "license, sell, rent, lease, transfer" the information, or to distribute or display it ([OpenPhish Terms](https://openphish.com/terms.html)). [`data/public_sets.json`](file:///home/maha/Documents/Dst_project/data/public_sets.json) is committed to the public GitHub repository that the paper's Code Availability section points to. That file contains **six verbatim OpenPhish URLs**, and the app's Data page displays them. Before you submit, remove the OpenPhish sample URLs from that file and from the page. Keep the aggregate statistics, which carry far less risk. The raw feed in `data/raw/` is not committed, which is correct. Phishing.Database is MIT-licensed, so it raises no such issue ([GitHub](https://github.com/Phishing-Database/Phishing.Database)).

## Provenance gaps a reviewer will notice

These are not wrong facts, but they hurt the paper's main selling point: "reproducible every number". Fix them if you have an hour left.

**State which Tranco list you used.** Tranco asks users to cite the NDSS paper, and it advises naming the specific list together with its generation date and permanent link ([Tranco list page](https://tranco-list.eu/list/K97GW/1000000)). Your local `tranco_top1m.csv` is **byte-identical (same SHA-256) to list 94P72, generated 7 Nov 2026** ([Tranco API](https://tranco-list.eu/api/lists/date/2026-11-07)). Without the ID, the false-alarm figures on the Tranco top 100k cannot be reproduced. Change the phrase in the Datasets section to:

> "...the top 100,000 domains of the Tranco list {tranco} generated on 7 November 2026 (list ID 94P72, https://tranco-list.eu/list/94P72)..."

**Give snapshot dates for the feeds.** For a live feed, the "Accessed:" date is the snapshot date:

- OpenPhish and Phishing.Database: downloaded **4 Nov 2026**.
- URLhaus mirror: downloaded **8 Nov 2026** (file header `Updated: 2026-11-08T00:10:55Z`).

Phishing.Database's ACTIVE lists were last refreshed on **2 Oct 2026 (version V.2026-10-02.17)** ([GitHub API](https://api.github.com/repos/Phishing-Database/Phishing.Database)). "Active" means PyFunceble found the URL reachable at its last test. It does not mean the page was re-confirmed as phishing. One limitation sentence about possible label noise covers this. The corrected reference strings below include all of these dates.

**Cite what is currently uncited.**

- **"The first rule set (v1, 17 rules) was written from the literature"** (line 472) names no source. Change it to "written from the literature {sahingoz,mohammad12,garera,cantina,kintis,agten}", keeping the keys in that order so they print in ascending order. Before you do, confirm that those six papers really informed v1.
- **The free-hosting rule** (contribution at line 285 and Table II) and **the abused-suffix rule** (Table II, line 394) cite nothing where they are introduced. Interisle directly supports both:
  - "24% of all phishing attacks took place using resources at subdomain providers", with phishing kits that automate their use ([Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)).
  - 42% of phishing domains sit in new gTLDs ([Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)).

  Add `{interisle}` at both points. Interisle does **not** discuss dynamic DNS, so attach the citation to "free hosting", not to "dynamic DNS".
- `app/corpus.py` credits Spamhaus for the suffix list, but Spamhaus is not in the reference list. Drop it from the code comment, or add a verified Spamhaus reference.

**Narrow the combosquatting wording.** Kintis defines combosquatting as the brand plus text added before *or* after it, for example `secure-example[.]com` ([CCS'17 PDF](https://acmccs.github.io/papers/p569-kintisA.pdf)). Your rule covers tokens that "start with" the brand, which is only a subset. At line 374, write "starts with it (a common form of combosquatting {kintis})".

**Pin the code version.** Code Availability gives a bare URL, `github.com/mahapara24/phistrace`, which points at a moving branch. Add a reference that names a commit hash or tag. A Zenodo DOI would be better still. Also be aware that "phistrace" without the h looks like a typo to a reader.

**Explain the "proposal" mention.** Section III refers to "the proposal", which readers cannot see. Either drop the reference or mark the proposal as unpublished.

## Polish: DOIs, pages, abbreviations and layout

**DOIs are inconsistent.** Only [11], [18] and [21] carry one. Verified DOIs exist for:

- [4] 10.1016/j.eswa.2018.09.029
- [5] 10.3390/make3030034
- [6] 10.1016/j.jksuci.2023.01.004
- [9] 10.60643/urai.v2024p159
- [15] 10.14722/ndss.2019.23386
- [17] 10.24432/C51W2X
- [19] 10.1145/1314389.1314391
- [20] 10.1145/1242572.1242659
- [22] 10.14722/ndss.2015.23058

The Crossref and DataCite links are in the sections above. [16] has no DOI (IEEE Xplore document 6470857).

**Other string-level fixes:**

- **Missing page ranges.** IEEE says all published proceedings papers have page numbers, so add pp. 569–586 to Kintis [21] and pp. 159–166 to Nicklas [9].
- **Abbreviate journal names:** *Expert Syst. Appl.*, *Mach. Learn. Knowl. Extr.*, *Comput. Secur.*
- **arXiv field order.** Put the year before the arXiv number: `…," 2017, arXiv:1701.07179.`
- **Add months** where the source records them.
- **Interisle subtitle.** Match it to the PDF cover, "A study of…". The publisher's web page uses "An Annual Study", so the current title is defensible, but the cover is the authoritative form.

All of these are already folded into the strings below.

**Layout and generator:**

- **No italics.** `references_xml()` writes each reference as a single `run()`, so journal and proceedings titles cannot be italicised. Switching it to `rich()` and wrapping the venue names in `*…*` fixes this.
- **Stretched reference lines.** The `references` style is justified, which stretches lines around long URLs. Set it to left-aligned.
- **Unbalanced last page.** Page 6 holds [14]–[22] in the left column only. IEEE templates want the two columns of the last page balanced.
- **Wrong font in the PDF.** LibreOffice substituted Liberation Serif for Times New Roman. Export from Word, or install Times New Roman first.
- **Table I names.** It uses bare surnames ("Prasad [11]"). "Prasad and Chandra [11]" and "Sahingoz et al. [4]" would match the body text. This is cosmetic.

**Coverage of the literature** is adequate for a 6-page paper: 22 references, 14 of them peer reviewed. About 36% are grey literature, which is acceptable for a feed-based evaluation as long as those entries are complete. Several research lines are missing: reference-based brand detection (Phishpedia/PhishIntention), LLM-based phishing URL detection, and RAG citation-faithfulness evaluation, which is relevant to your unsupported-claim metric. Several sentences would also benefit from a citation:

- the Punycode/homograph check
- the ROC-AUC/PR-AUC definitions
- the alert-fatigue claim in Section VII-A

The bibliographic details of these candidate references were not verified. Adding unverified entries the night before a deadline creates exactly the kind of error this check exists to catch. Leave them out for tomorrow and consider them for a camera-ready version.

## Paste-ready REFS dictionary

This replaces lines 37–60 of [build_paper.py](file:///home/maha/Documents/Dst_project/paper/build_paper.py). It adds one new key, `urlhausmirror`. Cite it in the Datasets section (must-fix 5). Because it first appears there, it is automatically numbered [23]. Access dates for apwg and interisle are set to the verification date. Change them if you read those sources on another day. Location fields were left out wherever they were not verified, which IEEE allows because location is optional.

```python
REFS = {
    "apwg": "Anti-Phishing Working Group, “Phishing activity trends report, 4th quarter 2025,” APWG, Feb. 18, 2026. Accessed: Nov. 17, 2026. [Online]. Available: https://docs.apwg.org/reports/apwg_trends_report_q4_2025.pdf",
    "interisle": "Interisle Consulting Group, “Phishing landscape 2024: A study of the scope and distribution of phishing,” Jul. 23, 2024. Accessed: Nov. 17, 2026. [Online]. Available: https://interisle.net/PhishingLandscape2024",
    "prasad": "A. Prasad and S. Chandra, “PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning,” Comput. Secur., vol. 136, Art. no. 103545, Jan. 2024, doi: 10.1016/j.cose.2023.103545.",
    "mohammad12": "R. M. Mohammad, F. Thabtah, and L. McCluskey, “An assessment of features related to phishing websites using an automated technique,” in Proc. 7th Int. Conf. Internet Technol. Secured Trans. (ICITST), London, U.K., Dec. 2012, pp. 492–497.",
    "uci327": "R. M. Mohammad and L. McCluskey, 2012, “Phishing Websites,” UCI Machine Learning Repository, Dataset 327, doi: 10.24432/C51W2X.",
    "sahoo": "D. Sahoo, C. Liu, and S. C. H. Hoi, “Malicious URL detection using machine learning: A survey,” 2017, arXiv:1701.07179.",
    "sahingoz": "O. K. Sahingoz, E. Buber, O. Demir, and B. Diri, “Machine learning based phishing detection from URLs,” Expert Syst. Appl., vol. 117, pp. 345–357, Mar. 2019, doi: 10.1016/j.eswa.2018.09.029.",
    "tang": "L. Tang and Q. H. Mahmoud, “A survey of machine learning-based solutions for phishing website detection,” Mach. Learn. Knowl. Extr., vol. 3, no. 3, pp. 672–694, Aug. 2021, doi: 10.3390/make3030034.",
    "safi": "A. Safi and S. Singh, “A systematic literature review on phishing website detection techniques,” J. King Saud Univ. Comput. Inf. Sci., vol. 35, no. 2, pp. 590–611, Feb. 2023, doi: 10.1016/j.jksuci.2023.01.004.",
    "access25": "Y. A. Kustiawan and K. I. Ghauth, “Feature engineering for phishing website detection using machine learning: A systematic review,” IEEE Access, vol. 13, pp. 192080–192104, 2025, doi: 10.1109/ACCESS.2025.3630334.",
    "garera": "S. Garera, N. Provos, M. Chew, and A. D. Rubin, “A framework for detection and measurement of phishing attacks,” in Proc. ACM Workshop Recurring Malcode (WORM), Alexandria, VA, USA, Nov. 2007, pp. 1–8, doi: 10.1145/1314389.1314391.",
    "cantina": "Y. Zhang, J. I. Hong, and L. F. Cranor, “CANTINA: A content-based approach to detecting phishing web sites,” in Proc. 16th Int. Conf. World Wide Web (WWW), Banff, AB, Canada, May 2007, pp. 639–648, doi: 10.1145/1242572.1242659.",
    "kintis": "P. Kintis et al., “Hiding in plain sight: A longitudinal study of combosquatting abuse,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur. (CCS), Dallas, TX, USA, Oct. 2017, pp. 569–586, doi: 10.1145/3133956.3134002.",
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
```

The LNICST volume number for [10] could not be confirmed: Crossref has no volume field. Leave "vol." out unless the [Springer book page](https://link.springer.com/book/10.1007/978-3-032-22545-0) shows one. The NDSS 2015 and 2019 locations and the ICLR 2023 location were not verified either, so they are left out. After you paste the dictionary and make the sentence edits, rerun `build_paper.py`. Then confirm that the new [23] appears and that no citation group prints out of order.

## Conclusion

The bibliography's biggest risk is not fabrication, because none was found. The risk is in how the sources are used. The wrong year on [17] and the preprint version of [10] are clerical errors. The real exposure is in sentences where the paper claims slightly more than its source supports ("most reported", "uses both", "LLM detector"), and in how the data was obtained. A paper whose contribution is a verifier that "keeps only sentences that an exhibit covers" should hold its own prose to the same standard, and the six must-fix edits do exactly that.

The data-terms work outlasts this deadline. URLhaus's licence has moved away from CC0 under Spamhaus-managed terms, OpenPhish forbids redistribution, and the Phishing.Database lists the paper uses were last refreshed six weeks ago. A paper built on live feeds needs to record dated snapshots, list IDs and licence terms with the same care it gives its rules. Doing that is what makes the claim "reproducible every number" true.
