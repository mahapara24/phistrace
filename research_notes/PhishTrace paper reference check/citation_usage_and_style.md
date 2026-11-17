# Citation Usage and IEEE Reference Style in the PhishTrace Paper

Scope: how citations are placed and numbered, and how the reference list is formatted. Whether the cited works exist or say what the paper claims is out of scope (other researchers cover that). No project files were edited.

Local evidence used:
- Generator: `/home/maha/Documents/Dst_project/paper/build_paper.py` (REFS dict lines 38-61, `cite()` lines 65-77, `references_xml()` lines 682-685)
- Built PDF: `/home/maha/Documents/Dst_project/paper/Mahapara_PhishTrace_IEEE.pdf` (6 pages, A4, read with `pdftotext`)
- Built DOCX: `/home/maha/Documents/Dst_project/paper/Mahapara_PhishTrace_IEEE.docx` (`word/styles.xml`, style `references`)
- Data provenance notes: `/home/maha/Documents/Dst_project/README.md` (Data table), `/home/maha/Documents/Dst_project/app/corpus.py` (lines 211, 447, 591)

Style authority used: the official IEEE Reference Guide. The IEEE Author Center PDF link now redirects to a Google Doc, version "V 3.28.2025", © 2025 IEEE ([IEEE Reference Guide, Author Center link](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf) → [Google Doc it redirects to](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)). Below this is called "IEEE RG 2025".

---

## Q1. Are references numbered strictly in order of first appearance, and are any cited in the abstract, keywords or Table I?

### Takeaway
Yes. All 22 references are numbered strictly in order of first appearance in the body. There are no citations in the abstract or the keywords. Every citation in Table I ([11], [4], [9], [10]) was already cited in the text above the table, so the table does not change the order.

### Cited Findings
- `cite()` assigns each key a number the first time it is used and emits the reference list in that same order (`_order`). An unknown key raises `KeyError`, so a citation to an undefined key cannot reach the output. — [build_paper.py lines 62-77, 682-685](file:///home/maha/Documents/Dst_project/paper/build_paper.py)
- The abstract and keywords are written with `run()`, not `rich()`/`cite()`, so a `{key}` there would show as literal braces rather than become a citation. Neither string contains a `{key}`, and the PDF abstract and keywords have no bracketed numbers. — [build_paper.py lines 236-253, 719-720](file:///home/maha/Documents/Dst_project/paper/build_paper.py); PDF page 1
- First-appearance sequence in the PDF: Introduction [1], [2] → [3]-[6] → [7] → [8] → [9], [10] → contributions list [11], [12], [13], [14], [15] → Related Work [16], [17], then [18] (with [3], [5], [6] repeated) → [19], [20], [21], [22]. This is monotonic, with no gaps or skips. — Mahapara_PhishTrace_IEEE.pdf pp. 1-2 (pdftotext)
- Table I (p. 2) cites "Prasad [11]", "Sahingoz [4]", "Nicklas [9]", "Li [10]". All four were first cited earlier in the body. — PDF p. 2
- Later re-uses are consistent: [21] and [22] in Section IV-B, [11]-[15] in Section V-A, and [2] for suffixes in Section V-B. — PDF pp. 2-3
- The abstract rule: IEEE editorial guidance says abstracts should not contain numbered references. The paper complies. — [IEEE Editorial Style Manual for Authors (copy hosted by Masaryk Univ.)](https://is.muni.cz/el/fi/jaro2023/VV070/IEEE-Editorial-Style-Manual-for-Authors.pdf?kod=VVc031) (seen only as a search snippet; the full text was not opened)
- IEEE RG 2025 says in-text citations go "on the line, in square brackets, inside the punctuation". The paper follows this (e.g., "online fraud [1], [2]."). — [IEEE RG 2025](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)

### Inferences
- The ordering is correct only because `S()` calls run in document order and tables are built inline. If someone moves a section or table in the script, or cites a new key first in a table note or figure caption, the numbering will still be correct, but a citation that first appears in a float will then define the order. That is IEEE-acceptable, but worth knowing.
- `cite()` keeps keys in a group in the order written; it does not sort them. Every current group happens to come out ascending ([3], [5], [6], [18]; [16], [17], and so on). A future group written as `{tranco,prasad}` would print "[15], [11]". The fix is to sort `nums` before joining.

### Gaps
- I did not open the full text of the IEEE Editorial Style Manual. The rule against citations in abstracts comes from the search-result snippet of that manual and from standard IEEE practice.

---

## Q2. Is the format for multiple citations and named citations correct ("[3], [4], [5], [6]", "Mohammad et al. [16], [17]")?

### Takeaway
The paper's style of listing every number ("[3], [4], [5], [6]") matches the current IEEE Reference Guide. That guide now forbids en-dash ranges, so the premise that IEEE prefers "[3]–[5]" is out of date. The named citations are acceptable. There are two small consistency points: "Mohammad et al. [16], [17]", where [17] has only two authors, and the short names in Table I.

### Cited Findings
- IEEE RG 2025 says en-dash ranges are no longer used in text and every reference number is written out: "[1]–[4]" becomes "[1], [2], [3], [4]". Its examples include "as shown by Brown [4], [5]" and "Smith [4] and Brown and Jones [5]; Wood et al. [7]". — [IEEE RG 2025](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)
- Older third-party guides showed ranges such as "[3]-[6]" in running text, which matches the older IEEE convention. — [IEEE Editorial Style Manual copies, e.g. CSUDH](https://www.csudh.edu/Assets/csudh-sites/csc/docs/IEEE-StyleManual.pdf) (search snippet). This conflicts with IEEE RG 2025, which is newer and takes precedence.
- IEEE RG 2025 says to use "et al." in text when three or more names are given for a cited reference. — [IEEE RG 2025](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)
- The paper uses: "Mohammad et al. [16], [17]" ([16] has three authors, [17] has two), "Sahingoz et al. [4]" (4 authors), "Prasad and Chandra [11]" (2), "Garera et al. [19]" (4), "Nicklas et al. [9]" (3), and "Li et al. [10]" (4). — PDF p. 2; REFS in build_paper.py
- Table I uses first-author surnames only: "Prasad [11]", "Sahingoz [4]", "Nicklas [9]", "Li [10]". — PDF p. 2

### Inferences
- No change is needed to the multiple-citation format. Do not "fix" it to "[3]–[6]", because that would go against IEEE RG 2025.
- "Mohammad et al. [16], [17]" is acceptable shorthand, since both works share the first author and "et al." applies to [16]. A stricter wording would be "Mohammad et al. [16] and Mohammad and McCluskey [17]".
- For consistency with the body text, Table I could read "Prasad and Chandra [11]", "Sahingoz et al. [4]", "Nicklas et al. [9]", "Li et al. [10]". Many IEEE papers do use bare surnames in tables, so this is cosmetic.
- The body never uses "Ref. [n]" or "reference [n]" in mid-sentence, which is correct.

### Gaps
- None material.

---

## Q3. Does each reference string follow the IEEE Reference Guide?

### Takeaway
The entries are mostly well formed (author initials, quoted sentence-case titles, "in Proc.", "vol./no./pp."). They have five systematic problems: (a) no web, feed, dataset or GitHub source has an "Accessed:" date; (b) DOIs appear on only 3 of 22 entries, although DOIs exist for at least 9 more; (c) four journal names are spelled out instead of abbreviated, and months are missing; (d) both arXiv entries put the year after the arXiv number; (e) the generator writes every reference as one plain run, so periodical and proceedings titles cannot be italicised. There is also one factual metadata error: the UCI "Phishing Websites" dataset [17] is dated 2015, but its DOI record gives 2012.

### Cited Findings
**IEEE templates (IEEE RG 2025, [link](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing))**
- Periodical: `J. K. Author, "Name of paper," Abbrev. Title of Periodical, vol. x, no. x, pp. xxx-xxx, Abbrev. Month, year, doi: xxx.` An article number replaces the page range as "Art. no.".
- Conference proceedings: `J. K. Author, "Title of paper," in Abbreviated Name of Conf., (location of conference is optional), (Month and day(s) if provided) year, pp. xxx-xxx.` The guide states that all published conference or proceedings papers have page numbers, and that "USA" must follow city and state for U.S. locations. Example: "in Proc. IEEE Antennas Propag. Soc. Int. Symp., Jul. 2006, pp. 4301–4304."
- arXiv/preprint: `J. K. Author, "Title of paper," year, arXiv number.` Example: "... nanopillars," 2003, arXiv:0303149." If the paper has since been published, cite the published version, not the arXiv version.
- Online and website sources: the accessed date is given as "Accessed: Abbrev. month day, year", followed by "[Online]. Available: URL", with no period after the URL. Example: "J. Smith. "Obama inaugurated as President." CNN.com. Accessed: Feb. 1, 2009. [Online.] Available: http://..." The guide writes "[Online]." in one section and "[Online.]" in another without reconciling them.
- Datasets: `Author, Date, "Title of Dataset," Source, doi: xxx.` or `... Source. [Online]. Available: URL`.
- Software: `J. K. Author. Title of Software. (Date). Repository or Archive. (version or year). Publisher Name.`, with an accessed date and URL where applicable. The guide has no GitHub-specific example.
- Reference list "et al.": for IEEE publications, list up to six names; with more than six, use the first author followed by "et al.".
- Periodical titles are abbreviated and set in italics. — [JCU IEEE LibGuide](https://libguides.jcu.edu.au/IEEE/journal-article); [Fort Lewis College IEEE guide](https://subjectguides.fortlewis.edu/citations/ieee). Use IEEE's own abbreviation list, and spell a title out in full only when it is not listed. Abbreviate consistently. — [Cornell CHEC IEEE entries](https://chec.engineering.cornell.edu/ieee-reference-page-entries)

**Generator mechanics**
- `references_xml()` writes each entry as `run(REFS[key])`, one unformatted run, so no part of a reference can be italic. — [build_paper.py line 684](file:///home/maha/Documents/Dst_project/paper/build_paper.py)
- The DOCX `references` style is justified (`<w:jc w:val="both"/>`), 8 pt, auto-numbered (numId 8). — `word/styles.xml` in the DOCX

**Metadata used to propose fixes (Crossref/DataCite API lookups, 2026-11-17)**
- [4] Sahingoz: Expert Syst. Appl. 117:345-357, published Mar. 2019, doi 10.1016/j.eswa.2018.09.029 — [Crossref](https://api.crossref.org/works/10.1016/j.eswa.2018.09.029)
- [5] Tang: Mach. Learn. Knowl. Extr. 3(3):672-694, Aug. 2021, doi 10.3390/make3030034 — [Crossref](https://api.crossref.org/works/10.3390/make3030034)
- [6] Safi: J. King Saud Univ. Comput. Inf. Sci. 35(2):590-611, Feb. 2023, doi 10.1016/j.jksuci.2023.01.004 — [Crossref](https://api.crossref.org/works/10.1016/j.jksuci.2023.01.004)
- [11] Prasad: Comput. Secur. vol. 136, Art. 103545, Jan. 2024, doi 10.1016/j.cose.2023.103545 — [Crossref](https://api.crossref.org/works/10.1016/j.cose.2023.103545)
- [15] Tranco: NDSS 2019, San Diego, CA, doi 10.14722/ndss.2019.23386 — [Crossref](https://api.crossref.org/works/10.14722/ndss.2019.23386)
- [17] UCI Phishing Websites: DataCite gives publication year 2012, creators Rami Mohammad and Lee McCluskey, doi 10.24432/C51W2X. The paper says 2015. — [DataCite](https://api.datacite.org/dois/10.24432/C51W2X)
- [18] Kustiawan: IEEE Access 13:192080-192104, 2025, doi 10.1109/ACCESS.2025.3630334. The paper's entry matches. — [Crossref](https://api.crossref.org/works/10.1109/ACCESS.2025.3630334)
- [19] Garera: Proc. 2007 ACM Workshop on Recurring Malcode, pp. 1-8, Alexandria, VA, USA, Nov. 2007, doi 10.1145/1314389.1314391 — [Crossref](https://api.crossref.org/works/10.1145/1314389.1314391)
- [20] CANTINA: Proc. 16th Int. Conf. WWW, pp. 639-648, Banff, AB, Canada, May 2007, doi 10.1145/1242572.1242659 — [Crossref](https://api.crossref.org/works/10.1145/1242572.1242659)
- [21] Kintis: Proc. 2017 ACM SIGSAC CCS, pp. 569-586, Dallas, TX, USA, Oct.-Nov. 2017, doi 10.1145/3133956.3134002 — [Crossref](https://api.crossref.org/works/10.1145/3133956.3134002)
- [22] Agten: NDSS 2015, San Diego, CA, doi 10.14722/ndss.2015.23058 — [Crossref](https://api.crossref.org/works/10.14722/ndss.2015.23058)
- The README says the PhiUSIIL data actually used is the UCI distribution "UCI 967 (CC BY 4.0)" at https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset. The OpenPhish file used is `https://openphish.com/feed.txt`, and the URLhaus file is `https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-online.txt`. — [README.md Data table](file:///home/maha/Documents/Dst_project/README.md)

**Per-reference problems and fixes** (numbers as printed)

| # | Type | Problems | Suggested fix |
|---|---|---|---|
| [1] APWG | Report series / web | No Accessed date; cites a whole series ("2024–2025") rather than a specific report; "APWG" given as both author and publisher | Cite a specific quarterly report, e.g. `Anti-Phishing Working Group, "Phishing activity trends report, 4th quarter 2024," APWG, <Mon.> 2025. Accessed: Nov. 17, 2026. [Online]. Available: https://apwg.org/trendsreports/` |
| [2] Interisle | Report / web | No Accessed date | Add `Accessed: Mon. DD, YYYY.` before `[Online]. Available:` |
| [3] Sahoo | arXiv | Year after the arXiv number | `..., "Malicious URL detection using machine learning: A survey," 2017, arXiv:1701.07179.` |
| [4] Sahingoz | Journal | Journal not abbreviated; no month; no DOI | `Expert Syst. Appl., vol. 117, pp. 345–357, Mar. 2019, doi: 10.1016/j.eswa.2018.09.029.` |
| [5] Tang | Journal | Journal not abbreviated; no month; no DOI | `Mach. Learn. Knowl. Extr., vol. 3, no. 3, pp. 672–694, Aug. 2021, doi: 10.3390/make3030034.` |
| [6] Safi | Journal | No month; no DOI | `..., Feb. 2023, doi: 10.1016/j.jksuci.2023.01.004.` |
| [7] Lewis | Conference | Lacks "Proc."; conference name not abbreviated | `in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 33, 2020, pp. 9459–9474.` "et al." is correct because the paper has more than six authors. |
| [8] Yao | Conference | Name could be abbreviated; no location or month (both optional) | `in Proc. Int. Conf. Learn. Represent. (ICLR), Kigali, Rwanda, May 2023.` ICLR has no page numbers, which is acceptable. Location and month were not verified here. |
| [9] Nicklas | Conference | No pages or DOI/URL, although IEEE RG says all published conference papers have page numbers | Add pages or a DOI/URL for the URAI 2024 proceedings (not found in Crossref; see Gaps) |
| [10] Li | arXiv | Year after the arXiv number; the key name `li26` hints at a 2026 published version | `..., 2025, arXiv:2507.15419.` If a 2026 venue version exists, cite that instead, as IEEE RG requires |
| [11] Prasad | Journal | "Computers & Security" not abbreviated; no month | `Comput. Secur., vol. 136, Art. no. 103545, Jan. 2024, doi: 10.1016/j.cose.2023.103545.` |
| [12] OpenPhish | Feed / web | No Accessed or snapshot date; URL is the homepage, not the feed file used | Add `Accessed: <snapshot date>.` and cite `https://openphish.com/feed.txt`, or state the snapshot date in the text |
| [13] Phishing.Database | GitHub repo | No Accessed date; no maintainer names, commit or version; "2026" is the access year, not a release date | Follow the software format: maintainer(s) as author, `Phishing.Database`, GitHub repository, accessed date, and ideally a commit hash or tag |
| [14] URLhaus | Feed / web | No Accessed date; free-text parenthetical "(read via the malware-filter mirror, ...)" is not IEEE form | Split it: [14] URLhaus with an accessed date, plus a separate reference (or footnote) for the malware-filter mirror `https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-online.txt` with an accessed date |
| [15] Tranco | Conference | No location, month or DOI; does not identify the list version used | `in Proc. Netw. Distrib. Syst. Secur. Symp. (NDSS), San Diego, CA, USA, Feb. 2019, doi: 10.14722/ndss.2019.23386.` Also give the Tranco list ID and download date in the text or a separate dataset reference |
| [16] Mohammad 2012 | Conference | Name not abbreviated; no location, month or DOI; author shown as "R. M. Mohammad" here and "R. Mohammad" in [17] | `in Proc. Int. Conf. Internet Technol. Secured Trans. (ICITST), London, U.K., Dec. 2012, pp. 492–497.` Make the author's initials consistent with [17] (DOI not found; see Gaps) |
| [17] UCI 327 | Dataset | Year should be 2012 per DataCite, not 2015; no DOI or URL; dataset not marked | `R. Mohammad and L. McCluskey, 2012, "Phishing Websites," UCI Machine Learning Repository, doi: 10.24432/C51W2X.` |
| [18] Kustiawan | Journal | Compliant (IEEE Access has no issue number). A month could be added | Optional |
| [19] Garera | Workshop | No location, month or DOI | `in Proc. ACM Workshop Recurring Malcode (WORM), Alexandria, VA, USA, Nov. 2007, pp. 1–8, doi: 10.1145/1314389.1314391.` |
| [20] CANTINA | Conference | No location, month or DOI | `in Proc. 16th Int. Conf. World Wide Web (WWW), Banff, AB, Canada, May 2007, pp. 639–648, doi: 10.1145/1242572.1242659.` |
| [21] Kintis | Conference | Missing pages (IEEE RG says proceedings papers have page numbers); no location or month | `in Proc. ACM SIGSAC Conf. Comput. Commun. Secur. (CCS), Dallas, TX, USA, 2017, pp. 569–586, doi: 10.1145/3133956.3134002.` |
| [22] Agten | Conference | No location, month or DOI | `in Proc. Netw. Distrib. Syst. Secur. Symp. (NDSS), San Diego, CA, USA, Feb. 2015, doi: 10.14722/ndss.2015.23058.` |

**Problems across the list**
- DOIs are inconsistent: only [11], [18] and [21] carry one, while at least [4], [5], [6], [15], [17] (dataset DOI), [19], [20] and [22] have DOIs (Crossref/DataCite links above). Either add DOIs everywhere they exist (recommended) or drop them everywhere.
- Conference names are abbreviated inconsistently: [11] and [7] use "&" or full words, while [6] and [18] are abbreviated. IEEE RG and library guides ask for the IEEE abbreviations, applied consistently.
- Accessed dates are missing in all six web, feed, dataset and repository entries ([1], [2], [12], [13], [14], [17]). For the feeds, the accessed date is effectively the data-snapshot date, so it matters for reproducibility as well as style.
- Titles: all article titles are in sentence case, which matches the IEEE RG examples. Report titles [1] "Phishing Activity Trends Reports" and [2] "Phishing Landscape 2024: An annual study..." mix title case and sentence case; pick one convention.
- Punctuation: the IEEE RG examples write "[Online]." (general section) and "[Online.]" (website section). The paper consistently uses "[Online]. Available:", which is acceptable. No entry ends with a period after a URL, which is correct.

### Inferences
- The highest-value fixes are: add accessed or snapshot dates to [1], [2], [12], [13], [14]; add DOIs to the 8 to 9 entries that have them; correct the year of [17] to 2012; and reorder the arXiv entries [3] and [10].
- To allow italic journal and proceedings titles, `references_xml()` would need to call `rich()` (which already italicises `*...*` segments) instead of `run()`, with the REFS strings marked up as `*Expert Syst. Appl.*` and so on. One caveat: `rich()` also calls `cite()`, which is harmless because reference strings contain no `{...}`.

### Gaps
- I could not find a DOI or page numbers for [9] (Nicklas et al., URAI 2024) or a DOI for [16] (ICITST 2012) through Crossref bibliographic search. The existence-check researchers should confirm both.
- ICLR 2023's location and month for [8] are from memory and were not verified.
- The maintainers of Phishing.Database and of the malware-filter mirror were not checked; take them from the repository pages.
- I did not confirm the UCI DOI for PhiUSIIL dataset 967.

---

## Q4. Which sentences state facts about prior work, datasets, statistics or tools without a citation?

### Takeaway
The Related Work section is well cited. The gaps are in Methodology, Experimental Setup and Discussion. Several rule-design facts come from APWG, Interisle or Spamhaus (according to the code's own comments) but are not cited where the rule is introduced. The URLhaus access-policy claim, the "written from the literature" v1 rule set, the IDN-homograph and public-suffix concepts, the tools (FastAPI, Python) and the evaluation metrics all lack citations.

### Cited Findings
Quoted sentences from the PDF/generator, with recommended citations. "Existing" means a reference already in the list.

1. Sec. IV-A: *"...derives the public suffix and the registrable domain using a table of multi-label suffixes such as co.uk and com.pk..."* No citation. Cite the Mozilla Public Suffix List (publicsuffix.org) as the concept the hand-built table approximates, or say explicitly that a reduced hand-built table is used instead. — [build_paper.py lines 359-363](file:///home/maha/Documents/Dst_project/paper/build_paper.py)
2. Sec. IV-B: *"A Punycode label fires only when it decodes to Latin letters mixed with letters of another script, the homograph form..."* No citation. Cite RFC 3492 (Punycode) and an IDN-homograph source such as Gabrilovich and Gontmakher, "The homograph attack," Commun. ACM, 2002, or Unicode TS #39 (mixed-script detection). New references are needed. — build_paper.py lines 378-379
3. Sec. IV-B: *"...on a newer generic suffix (interac.tax) it is not, because anyone can register it."* This is a claim about new-gTLD registration policy. Cite ICANN's New gTLD Program or Interisle [2] (existing).
4. Table II, "Free hosting†", and Sec. V-B, *"...dynamic DNS hosts for malware and kit hosting"* and *"cloud storage buckets, IPFS gateways, and shared hosts..."*. No citation in the paper, but the code says the host list was taken from APWG and Interisle reports ("Listed because phishing kits are often deployed there (APWG and Interisle reports)"). Cite [1], [2] (existing) where the rule is introduced. — [corpus.py lines 211, 591](file:///home/maha/Documents/Dst_project/app/corpus.py)
5. Table II, "Abused suffix ... on a N-entry abuse list". Not cited in Sec. IV. It is first cited only later ("suffixes [2]" in Sec. V-B). The code says the list follows "the most-abused lists in the Interisle Phishing Landscape and Spamhaus reports", and Spamhaus is not in the reference list at all. Cite [2] at first mention and add a Spamhaus TLD-abuse reference (or drop Spamhaus from the code comment). — [corpus.py line 447](file:///home/maha/Documents/Dst_project/app/corpus.py)
6. Table II, "Email leftover — URL contains =3D from email encoding". This depends on quoted-printable encoding. Optionally cite RFC 2045.
7. Sec. V-A: *"...read from the public malware-filter mirror because the URLhaus bulk download now requires an account key"*. This is a factual claim about a third party's access policy with no citation. Cite the abuse.ch/URLhaus announcement or API documentation with an accessed date, and cite the mirror itself (see Q3 [14]). — build_paper.py lines 450-452
8. Sec. V-A: *"...and the top 100,000 domains of the Tranco list [15]..."*. The method is cited, but the list version is not. The Tranco site provides permanent list IDs so that researchers can "refer to it later on", and it notes that researchers "overwhelmingly lack any comment" on download date. Give the list ID and date. — [Tranco site](https://tranco-list.eu/); README says "latest list, top 1M" ([README.md](file:///home/maha/Documents/Dst_project/README.md))
9. Sec. V-A: *"PhiUSIIL [11] provides 235,795 labeled URLs"*. Cited to the article, but the data actually downloaded is the UCI dataset 967 distribution (CC BY 4.0), which also deserves a dataset reference or a URL alongside [11]. — [README.md](file:///home/maha/Documents/Dst_project/README.md)
10. Sec. V-A: *"Every URL or domain is assigned to a split by its MD5 hash"*. Citing RFC 1321 is optional; low priority.
11. Sec. V-B: *"The first rule set (v1, 17 rules) was written from the literature before any data was inspected."* "The literature" is uncited. Cite the specific sources, likely [4], [16], [19], [20], [21], [22] (existing).
12. Sec. V-C: *"PhishTrace is written in Python 3 with FastAPI for the web interface..."*. Tools are uncited. IEEE allows software references (RG 2025 software format). Add FastAPI (S. Ramírez, FastAPI, with version and URL) and optionally Python. Many venues accept a footnote URL instead.
13. Sec. IV-G: *"ROC-AUC uses the uncapped score with average ranks for ties, and PR-AUC is average precision over score thresholds."* The metric definitions are uncited. Cite a standard source, e.g., T. Fawcett, "An introduction to ROC analysis," Pattern Recognit. Lett., 2006, and J. Davis and M. Goadrich, "The relationship between precision-recall and ROC curves," ICML 2006. New references are needed.
14. Sec. III: *"The questions and objectives of the proposal were revised..."*. This refers to an unpublished course proposal that the reader cannot see. Either remove the sentence or describe the proposal as unpublished. IEEE practice is to cite unpublished work as "unpublished".
15. Sec. VII-A: *"...a tool that flags several of every hundred popular sites trains users to ignore it."* This is a behavioural (alert-fatigue) claim with no citation. Cite warning-fatigue literature, e.g., D. Akhawe and A. P. Felt, "Alice in Warningland," USENIX Security 2013. New reference.
16. Sec. VII-B: *"...page content, domain age, or reputation data would be needed."* Cite CANTINA [20] (existing) for content features, and a domain-age or host-feature source such as Ma et al., "Beyond blacklists," KDD 2009. New reference.
17. Sec. VII-C: *"Almost every legitimate URL in PhiUSIIL is an https homepage..."*. This is the author's own observation. Optionally cite [11] for how PhiUSIIL collected its legitimate URLs, so readers can see the artifact comes from the dataset's construction.
18. Sec. VII-E: *"Feeds and popularity lists change daily and the lists need maintenance."* Cite [15] (existing). The Tranco paper's premise is list instability and manipulation.
19. Sec. I: *"...they remain among the most reported forms of online fraud [1], [2]."* It is cited, but APWG and Interisle count phishing attacks and domains, not fraud reports across fraud types. A victim-report source such as the FBI IC3 annual Internet Crime Report fits "most reported" better. The support-check researchers should confirm.

### Inferences
- Items 4, 5, 7, 8, 11 and 14 are the most important, because they involve undisclosed provenance (Spamhaus), third-party policy claims, or vague appeals to "the literature".
- Items 2, 12, 13, 15 and 16 would add about 5 to 7 new references. That is within normal limits for a 6-page paper (see Q6).
- The abstract makes quantitative claims, but it correctly has no citations. The supporting citations appear in the body.

### Gaps
- I did not verify the wording or contents of FBI IC3, Spamhaus, RFC 3492, Unicode TS #39, Fawcett 2006, Davis and Goadrich 2006, Akhawe and Felt 2013, or Ma et al. 2009 in this session. They are suggestions from domain knowledge, and the existence-check team should verify them before adding.

---

## Q5. Are all 22 REFS entries cited? Any undefined keys? Self-reference issues?

### Takeaway
All 22 REFS keys are cited and appear in the reference list. There are no orphans and no undefined keys. The GitHub repository appears only as a bare URL in the Code Availability paragraph, which is acceptable, but it is the paper's main artifact and should get a reference (or footnote) with a version or commit.

### Cited Findings
- REFS defines 22 keys (apwg, interisle, prasad, mohammad12, uci327, sahoo, sahingoz, tang, safi, access25, garera, cantina, kintis, agten, lewis, yao, nicklas, li26, openphish, urlhaus, tranco, phishdb). The PDF reference list has exactly 22 entries, [1]-[22], so every key was reached by `cite()`, because the list is emitted only from `_order`. — [build_paper.py lines 38-61, 682-685](file:///home/maha/Documents/Dst_project/paper/build_paper.py); PDF pp. 5-6
- Undefined keys are impossible in the output, because `cite()` raises `KeyError`. — build_paper.py lines 70-71
- Code Availability gives "https://github.com/mahapara24/phistrace". The git remote confirms that this spelling ("phistrace", without the "h" of "Phish") is the real repository name. — `git remote -v` in /home/maha/Documents/Dst_project
- The IEEE RG software format includes repository, version or year, accessed date and URL. — [IEEE RG 2025](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)

### Inferences
- Recommended: add a reference such as `Mahapara, "PhishTrace," GitHub repository, commit <hash> / tag v4, 2026. Accessed: ... [Online]. Available: https://github.com/mahapara24/phistrace`, and cite it in Code Availability and in the Sec. I contribution "reproducible evaluation". Without a commit or tag, the claim to reproduce "every number in this paper" is tied to a moving branch. An archived DOI (for example from Zenodo) would be better still.
- "phistrace" versus "PhishTrace" could look like a typo to reviewers. Consider renaming the repository or adding a note.
- For double-blind venues, the repository URL and author name would need anonymising. A course submission does not need this.

### Gaps
- None.

---

## Q6. Is the reference list adequate for a 6-page IEEE paper on this topic (count, recency, balance)?

### Takeaway
Twenty-two references is a reasonable count for a 6-page IEEE conference paper. However, 8 of 22 (36%) are not peer reviewed (6 web, feed or dataset entries and 2 arXiv preprints). Only 6 of the 14 peer-reviewed works are from 2021 or later. Several directly relevant research lines are missing: LLM-based phishing URL detection, reference-based (brand-logo) phishing detection, deep URL models, and RAG attribution/faithfulness evaluation. The last one matters because the paper's main investigation metric is an unsupported-claim rate.

### Cited Findings
- Composition (from REFS):
  - Peer-reviewed journals (5): [4] 2019, [5] 2021, [6] 2023, [11] 2024, [18] 2025.
  - Peer-reviewed conferences and workshops (9): [7] 2020, [8] 2023, [9] 2024, [15] 2019, [16] 2012, [19] 2007, [20] 2007, [21] 2017, [22] 2015.
  - arXiv (2): [3] 2017, [10] 2025.
  - Industry reports (2): [1], [2].
  - Feeds, datasets and repositories (4): [12], [13], [14], [17].
  - [build_paper.py REFS](file:///home/maha/Documents/Dst_project/paper/build_paper.py)
- Peer-reviewed works from 2021 to 2026: [5], [6], [8], [9], [11], [18] (6 of 14). Works from before 2016: [16], [17] (2012), [19], [20] (2007), [22] (2015). — same
- [3] Sahoo et al. is still cited as an arXiv preprint dated 2017. IEEE RG says to cite the published version when one exists. — [IEEE RG 2025](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)
- The paper's keywords include "explainability", "retrieval-augmented generation" and "agents", but RAG and agents are supported by only [7], [8], [9], [10], and no explainability reference is cited. — PDF p. 1; REFS

### Inferences
- Count: about 20 to 30 references is common for 6-page IEEE conference papers. This is an observation from practice, not an IEEE rule (see Gaps). 22 is fine, and adding 5 to 8 targeted references (Q4 items and the gaps below) would still be well within norms.
- Topic coverage gaps (suggestions to verify):
  - Reference-based phishing detection with brand lists (Phishpedia, USENIX Security 2021; PhishIntention, USENIX Security 2022). These are closely related to the brand-mismatch rule.
  - LLM-based phishing website detection (for example, Koide et al., 2023-2024, on detecting phishing sites with ChatGPT). This would support the Sec. I claim that "recent phishing work uses both [RAG and agents], usually with a large language model in the loop", which currently rests on only two papers ([9] is email, not URL).
  - Deep URL classifiers (for example, URLNet, 2018).
  - RAG attribution and citation evaluation (for example, Gao et al., "Enabling large language models to generate text with citations," EMNLP 2023, or RAGAS). These would position the "unsupported-claim rate" and "evidence support" metrics.
  - An explainable phishing detection study, to justify the "explainability" keyword.
- Balance: about 36% grey literature is acceptable here because the paper evaluates on public feeds, but those entries must then be complete (accessed or snapshot dates; see Q3). Replacing arXiv [3] with its published version, if any, and checking [10] would raise the peer-reviewed share.
- Table I compares against only four works. Adding one rule or heuristic system (e.g., [19] or [20]) and one RAG-for-security system would make the "gap" claim more convincing.

### Gaps
- IEEE does not publish a required or typical reference count for conference papers. I found no authoritative source for a norm, so the "20 to 30" figure is a practitioner heuristic.
- I did not verify the bibliographic details of the suggested missing works (Phishpedia, PhishIntention, Koide et al., URLNet, Gao et al., RAGAS) in this session.

---

## Q7. Formatting issues in the generated document

### Takeaway
The document is 6 A4 pages, and the citation and reference numbering renders correctly. There are visible layout problems: an unbalanced last page (references [14]-[22] fill only part of the left column of page 6), wide justified gaps in several reference entries, no italics in references, and the PDF was rendered with Liberation Serif rather than Times New Roman.

### Cited Findings
- `pdfinfo`: 6 pages, A4 (595.3 × 841.9 pt), produced by LibreOffice 24.2. — Mahapara_PhishTrace_IEEE.pdf
- Page 6 contains only references [14]-[22] in the left column. The right column is empty. — `pdftotext -layout -f 6 -l 6` output
- Justification produces stretched lines in the reference list: "APWG,               2024–2025.            [Online].        Available:" in [1], and similar gaps in [13], [18] ("Access,       vol.    13,    pp.") and [21] ("Communications            Security       (CCS),        2017,         doi:"). The cause is the `references` style `jc=both` combined with long unbreakable URLs and DOIs. — PDF pp. 5-6; DOCX `word/styles.xml`
- `pdffonts` lists LiberationSerif (Regular, Italic, Bold, BoldItalic), all embedded. The DOCX itself requests Times New Roman, but the PDF converter substituted a metric-compatible font. — `pdffonts` output
- References are plain runs with no italics (Q3). — build_paper.py line 684
- The abstract and keywords contain no citations, and the "Abstract—" and "Keywords—" lead-ins follow the template. — PDF p. 1
- Cross-references "Section IV-G" (Evaluation Metrics = IV-G) and "Section VII" (Discussion, Dataset Artifacts) point to the correct sections, given the order I Introduction, II Related Work, III Research Questions, IV Methodology (A-G), V Experimental Setup, VI Results, VII Discussion, VIII Conclusion. — PDF / build_paper.py
- The IEEE copyright footer was deliberately blanked "for a course submission". — build_paper.py lines 746-748
- "Code Availability" and "References" use the template's Heading 5 style (rendered "CODE AVAILABILITY", "REFERENCES"), which matches how the template styles Acknowledgment and References. — PDF p. 5; build_paper.py lines 672, 679

### Inferences
- Balance the last-page columns. IEEE conference templates ask for equal column lengths on the last page; one way is a continuous section break before the end of the references. Alternatively, the space could be used for the extra references suggested in Q4 and Q6.
- To reduce justified gaps, set the `references` paragraphs to left-aligned (many IEEE LaTeX outputs are effectively ragged for URLs), or let URLs and DOIs break at "/" or "." with zero-width spaces.
- Export the PDF with Times New Roman installed (or use Word), because IEEE PDF eXpress-style checks expect Times. Liberation Serif is metric-compatible, so the layout would not change.
- The author block includes a student ID ("MS (Data Science), 26I8005_A"). This is fine for a course, but it is not IEEE affiliation format.

### Gaps
- I could not access the IEEE conference template's own instruction text in this session, so the column-balancing and Times-font expectations are stated from general IEEE template practice rather than quoted.
