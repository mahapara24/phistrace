# PhishTrace paper reference check: heuristics and squatting references (apwg, interisle, garera, cantina, kintis, agten)

Scope: the six REFS entries in /home/maha/Documents/Dst_project/paper/build_paper.py (lines 39, 40, 49–52). Where they are cited:
- `{apwg,interisle}` at line 263 (Introduction): phishing "remain[s] among the most reported forms of online fraud".
- `{garera}`, `{cantina}`, `{kintis}`, `{agten}` at lines 306–308 (Related Work, "Heuristic and Lexical Detection").
- `{kintis}` and `{agten}` at lines 374–375 (Method): brand-token matching. A token "starts with" the brand (combosquatting), or for names of 6+ letters differs by one insertion, deletion, substitution or adjacent swap (typosquatting).
- `{interisle}` at line 474 (Rule Development Protocol): v2 added "suffixes {interisle}".
- The brief says interisle is cited for free hosting used by phishing kits. No sentence in build_paper.py does that. The free-hosting rule text (lines 285, 390, 405, 477, 563) cites nothing. The report would support such a citation (see below).

Checked 2026-11-17 against Crossref, the publisher PDFs, the NDSS site, APWG docs and Interisle's own PDF.

## Summary verdict table

| Key | Verdict | Fix |
|---|---|---|
| apwg | MINOR ERRORS | The series citation resolves, but IEEE expects a specific report. Cite one report, e.g. Q4 2025. |
| interisle | MINOR ERRORS | The cover subtitle is "A Study of…", not "An annual study of…". Add the full date (23 Jul. 2024). |
| garera | MINOR ERRORS (details correct) | All details correct. Add DOI 10.1145/1314389.1314391. Optionally add the location. |
| cantina | MINOR ERRORS (details correct) | All details correct. Add DOI 10.1145/1242572.1242659. |
| kintis | MINOR ERRORS | DOI correct, and 8 authors so "et al." is fine. Pages 569–586 are missing. |
| agten | MINOR ERRORS (details correct) | All details correct. Add DOI 10.14722/ndss.2015.23058. |

None of the six is WRONG or NOT FOUND. Every reference exists and every core detail checked out. Of the "minor errors", only interisle (subtitle) and apwg (series vs. report) have a factual mismatch. The rest are omissions (DOI, pages).

## apwg: APWG Phishing Activity Trends Reports (URL, citing a series, claim support)

### Takeaway
https://apwg.org/trendsreports/ works and lists the quarterly reports. IEEE style cites a specific document, so the reference should name one report (title, quarter, publication date, PDF URL). APWG reports give attack volumes, not a ranking against other fraud types. They only partly support "among the most reported forms of online fraud".

### Cited Findings
- https://apwg.org/trendsreports/ returned HTTP 200 (text/html) on 2026-11-17. The page lists the quarterly Phishing Activity Trends Reports with PDF links on docs.apwg.org. — [APWG Trends Reports page](https://apwg.org/trendsreports/)
- The page I fetched showed 1Q 2025 as its "current" summary. Its 2024 entries were 1Q 2024 (published May 14, 2024), 2Q 2024, 3Q 2024 and 4Q 2024 (published March 19, 2025). Its 3Q 2024 date (August 21, 2024) is impossible for a July–September report, so it is probably a page or extraction error. — [APWG Trends Reports page](https://apwg.org/trendsreports/)
- The Q4 2024 report's cover reads "Phishing Activity Trends Report, 4th Quarter 2024", "Published 19 March 2025". It says "In the fourth quarter of 2024, APWG observed 989,123 phishing attacks". — [APWG Q4 2024 PDF](https://docs.apwg.org/reports/apwg_trends_report_q4_2024.pdf)
- The Q4 2025 report reads "Phishing Activity Trends Report, 4th Quarter 2025", "Activity October-December 2025", "Published 18 February 2026". It states "During 2025, APWG observed 3.8 million phishing attacks, which was up slightly from 3.76 million in 2024", and 853,244 attacks in Q4 2025. — [APWG Q4 2025 PDF](https://docs.apwg.org/reports/apwg_trends_report_q4_2025.pdf)
- PDFs for Q1–Q4 2025 and Q1 2026 also exist at docs.apwg.org/reports/apwg_trends_report_qN_YYYY.pdf. The Q1 2026 PDF opened as a real 14-page report. — [APWG Q1 2026 PDF](https://docs.apwg.org/reports/apwg_trends_report_q1_2026.pdf)
- The trends-reports page offers no recommended citation format and does not rank phishing against other crimes. — [APWG Trends Reports page](https://apwg.org/trendsreports/)

### Inferences
- A series reference ("Phishing Activity Trends Reports, 2024–2025", landing page only) is acceptable in informal practice. It is weak for IEEE because readers cannot check a specific number, and the landing page changes every quarter. IEEE's reference guide treats reports as specific documents (author/organization, title, report number or issue, date, URL).
- Suggested corrected reference (one report covering both years, matching "2024–2025"):
  `Anti-Phishing Working Group, "Phishing activity trends report, 4th quarter 2025," APWG, Feb. 18, 2026. [Online]. Available: https://docs.apwg.org/reports/apwg_trends_report_q4_2025.pdf`
  The Q4 2025 report gives totals for both 2025 (3.8 million) and 2024 (3.76 million). Alternative if the paper should cite only 2024 data: `Anti-Phishing Working Group, "Phishing activity trends report, 4th quarter 2024," APWG, Mar. 19, 2025. [Online]. Available: https://docs.apwg.org/reports/apwg_trends_report_q4_2024.pdf`
- On the claim: APWG supports "phishing is high-volume and persistent" (millions of attacks a year). It does not itself say phishing is "among the most reported forms of online fraud". Interisle does (next section, citing FBI data). The pair `{apwg,interisle}` therefore supports the sentence jointly. Optionally, rephrase to "remain among the most common forms of online fraud, with millions of attacks observed each year". Another option is to add the FBI IC3 annual report as a primary source for "most reported". I did not verify IC3 here.

### Gaps
- I did not open the Q1–Q3 2025 PDFs. I only confirmed they return HTTP 200 with application/pdf.
- I did not verify the correct publication date of the Q3 2024 report.

## interisle: Interisle "Phishing Landscape 2024" (title, date, URL, support for suffix and free-hosting claims)

### Takeaway
The report exists, is dated 23 July 2024, and the given URL works (it redirects to Interisle's insights page). The PDF cover subtitle is "A Study of the Scope and Distribution of Phishing". The web page uses "An Annual Study of…". The report strongly supports both claims: abused, cheap suffixes (new gTLDs, .TOP, .XYZ, .SHOP etc.), and free subdomain/hosting providers, including phishing kits that automate them.

### Cited Findings
- https://interisle.net/PhishingLandscape2024 returned HTTP 200 after redirecting to https://interisle.net/insights/phishing-landscape-2024-an-annual-study-of-the-scope-and-distribution-of-phishing. The web page title is "Phishing Landscape 2024: An Annual Study of the Scope and Distribution of Phishing". It is dated "Jul 23", © 2024, and names David Piscitello as writer. — [Interisle insights page](https://interisle.net/insights/phishing-landscape-2024-an-annual-study-of-the-scope-and-distribution-of-phishing)
- The PDF cover reads "Phishing Landscape 2024 — A Study of the Scope and Distribution of Phishing — INTERISLE CONSULTING GROUP 23 JULY 2024". It has 34 pages, with "About the Authors": Greg Aaron, Lyman Chapin, David Piscitello, Colin Strutt and Karen Rose. — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf) (redirects to a static1.squarespace.com file)
- Study period: "3.9 million phishing reports collected over a year (May 2023 to April 2024)", with year-over-year analysis of over 15 million reports. — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
- Intro claim: the report says phishing "is the most commonly used tactic in the perpetration of these cybercrimes". It cites FBI figures of over 880,000 US cybercrime complaints and US$12.5 billion losses. — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
- Suffix claim:
  - "42% of all domains reported for phishing were registered in new gTLDs, compared to 25% last year". New gTLDs hold only about 10% market share. — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
  - "After the demise of the phish-friendly domain registry Freenom, cybercriminals moved to using inexpensive domain names in new gTLDs". — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
  - The section "Phishers Like Cheap" says "Some registry operators continue to compete by offering cheap and sometimes free registrations". It uses TLD-lists.com price history. — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
  - Its TLD rankings put .TOP, .XYZ, .SHOP, .CN and .INFO among the top 5 by phishing domains across years. Its examples of new gTLDs are .LOL, .SBS, .SHOP and .TOP. — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
- Free hosting / phishing kits:
  - "24% of all phishing attacks took place using resources at subdomain providers… Most of these services are free". — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
  - "Some phishing kits — software used by phishers to launch and manage their phishing sites — integrate the use of subdomain providers, allowing the phishers to sign up for and use subdomains in an automated fashion". — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
  - 454,948 attacks on 750 subdomain-provider SLDs. The provider table names Blogspot/web.app (Google), Weebly, Cloudflare (pages.dev, workers.dev, trycloudflare.com), Hostinger (000webhostapp.com) and GitHub (github.io). — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)
  - IPFS phishing rose 1,300% to about 19,000 sites. Named gateways include dweb.link/ipfs.io, cf-ipfs.com and infura-ipfs.io. — [Interisle PDF](https://interisle.net/s/PhishingLandscape2024.pdf)

### Inferences
- Verdict: MINOR ERRORS. The subtitle should follow the document's cover ("A study of…"), and the full date should be given. Corrected IEEE string:
  `Interisle Consulting Group, "Phishing landscape 2024: A study of the scope and distribution of phishing," Jul. 23, 2024. [Online]. Available: https://interisle.net/PhishingLandscape2024`
  Optionally list the authors: G. Aaron, L. Chapin, D. Piscitello, C. Strutt, and K. Rose. That is five names, so IEEE would list them all; a corporate author is also acceptable. Keeping "An annual study…" is defensible because the publisher's web page uses it. The cover is the more authoritative form.
- The `{interisle}` citation at line 474 (suffixes) is well supported.
- Optional: the free-hosting rule (lines 285/390/477, "free hosting and dynamic DNS hosts", "IPFS", "kit hosting") could also cite `{interisle}`. The report directly covers subdomain providers, IPFS and phishing kits. It does not discuss dynamic DNS specifically.

### Gaps
- The report does not discuss dynamic DNS providers, so it does not support that part of the free-hosting rule.

## garera: Garera, Provos, Chew, Rubin, WORM 2007

### Takeaway
All bibliographic details are correct: authors, order, initials, title, venue, year and pages 1–8. Add the DOI 10.1145/1314389.1314391. The paper does classify URL obfuscation into four types: IP host, host hidden in path/other domain, large host names with brand-like labels, and unknown/misspelled domain. The paper's description "brand names in subdomains and IP hosts" is accurate. I checked this through secondary descriptions, because the primary PDF was not open-access.

### Cited Findings
- Crossref for DOI 10.1145/1314389.1314391 gives title "A framework for detection and measurement of phishing attacks". Container is "Proceedings of the 2007 ACM workshop on Recurring malcode", pages 1-8, published 2007-11-02. Authors: Sujata Garera, Niels Provos, Monica Chew, Aviel D. Rubin. Event: held with CCS 2007, Alexandria, Virginia, USA. — [Crossref](https://api.crossref.org/works/10.1145/1314389.1314391); [DOI](https://doi.org/10.1145/1314389.1314391)
- Semantic Scholar lists the same four authors and marks the paper as closed access. — [Semantic Scholar API](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/1314389.1314391?fields=title,abstract,openAccessPdf,externalIds)
- PhishDef (Le et al.) says Garera et al. "find four distinct categories of obfuscation techniques that phishing URLs use". The categories are "(I) Obfuscating the host with an IP address, (II) Obfuscating the host with another domain, (III) Obfuscating with large host names, and (IV) Domain unknown or misspelled". Type III examples include http://www.volksbank.de.custsupportref1007.dllconf.info/… and http://sparkasse.de.redirector.webservices.aktuell.lasord.info. — [PhishDef, arXiv 1009.2275](https://ar5iv.arxiv.org/html/1009.2275)
- Secondary sources describe the method as a logistic-regression classifier over hand-selected URL features. It was used to measure phishing prevalence across millions of URLs (Google data). — [PhishDef, arXiv 1009.2275](https://ar5iv.arxiv.org/html/1009.2275)

### Inferences
- "Measured URL obfuscation patterns such as brand names in subdomains and IP hosts" is a fair paraphrase. Type I is IP hosts. Type III (large host names) puts brand/bank names in leading labels of an unrelated domain.
- Corrected IEEE string (adds DOI and location; everything else unchanged):
  `S. Garera, N. Provos, M. Chew, and A. D. Rubin, "A framework for detection and measurement of phishing attacks," in Proc. ACM Workshop on Recurring Malcode (WORM), Alexandria, VA, USA, 2007, pp. 1–8, doi: 10.1145/1314389.1314391.`

### Gaps
- I could not reach the primary PDF (ACM paywall; old JHU/Google URLs return 404). The four-type taxonomy rests on PhishDef's verbatim description, not the original text.

## cantina: Zhang, Hong, Cranor, WWW 2007

### Takeaway
All details are correct: authors, initials, title, "16th Int. Conf. World Wide Web", 2007, pp. 639–648. Add the DOI 10.1145/1242572.1242659. The claim is accurate: CANTINA uses TF-IDF lexical signatures sent to Google, combined with heuristics to cut false positives.

### Cited Findings
- Crossref for DOI 10.1145/1242572.1242659 gives title "Cantina" (Crossref truncates titles), container "Proceedings of the 16th international conference on World Wide Web", pages 639-648, date 2007-05-08. Authors: Yue Zhang, Jason I. Hong, Lorrie F. Cranor. Event: WWW'07, Banff, Alberta, Canada. — [Crossref](https://api.crossref.org/works/10.1145/1242572.1242659)
- The full title on the PDF is "CANTINA: A Content-Based Approach to Detecting Phishing Web Sites". — [CANTINA PDF (CMU)](https://www.cs.cmu.edu/~jasonh/publications/www2007-cantina-final.pdf)
- The abstract presents "a novel, content-based approach to detecting phishing web sites, based on the TF-IDF information retrieval algorithm. We also discuss the design and evaluation of several heuristics we developed to reduce false positives". It reports "approximately 95%" of phishing sites labeled correctly. — [CANTINA PDF](https://www.cs.cmu.edu/~jasonh/publications/www2007-cantina-final.pdf)
- Method: CANTINA builds a "lexical signature" from the five top TF-IDF terms and feeds it to Google. Its heuristics (Table 1) are Age of Domain, Known Images, Suspicious URL, Suspicious Links, IP Address, Dots in URL and Forms. — [CANTINA PDF](https://www.cs.cmu.edu/~jasonh/publications/www2007-cantina-final.pdf)

### Inferences
- "Combined term statistics with heuristics" is accurate. "TF-IDF term weights with a search-engine lookup" would be more precise.
- Corrected IEEE string:
  `Y. Zhang, J. I. Hong, and L. F. Cranor, "CANTINA: A content-based approach to detecting phishing web sites," in Proc. 16th Int. Conf. World Wide Web (WWW), Banff, AB, Canada, 2007, pp. 639–648, doi: 10.1145/1242572.1242659.`

### Gaps
- None.

## kintis: Kintis et al., CCS 2017

### Takeaway
The DOI 10.1145/3133956.3134002 resolves to this paper. It has 8 authors, so "P. Kintis et al." is valid IEEE style (IEEE allows et al. for more than six names). Pages 569–586 are missing. Kintis supports the related-work claim that attackers attach words to a brand. The method's "starts with the brand" rule covers only part of Kintis's combosquatting definition, which allows text before or after the brand.

### Cited Findings
- Crossref for DOI 10.1145/3133956.3134002 gives title "Hiding in Plain Sight", subtitle "A Longitudinal Study of Combosquatting Abuse". Container: Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, pages 569-586, 2017-10-30, Dallas, TX, USA. — [Crossref](https://api.crossref.org/works/10.1145/3133956.3134002)
- Authors in Crossref order: Panagiotis Kintis, Najmeh Miramirkhani, Charles Lever, Yizheng Chen, Rosa Romero-Gómez, Nikolaos Pitropakis, Nick Nikiforakis, Manos Antonakakis. That is 8 authors. The PDF spells the fifth name "Roza Romero-Gómez". — [Crossref](https://api.crossref.org/works/10.1145/3133956.3134002); [CCS'17 PDF](https://acmccs.github.io/papers/p569-kintisA.pdf)
- Definition: a domain is combosquatting if "(1) The domain contains the trademark. (2) The domain cannot result by applying the five typosquatting models of Wang et al." Characters may be "prepended or appended to the e2LD". Examples: secure-example[.]com, myexample[.]com, anothercoolexample-here[.]com. — [CCS'17 PDF](https://acmccs.github.io/papers/p569-kintisA.pdf)
- Kintis reports that combosquatting domains are more than 100 times more prevalent than typosquatting domains. — [CCS'17 PDF](https://acmccs.github.io/papers/p569-kintisA.pdf)

### Inferences
- Corrected IEEE string (adds pages and location):
  `P. Kintis et al., "Hiding in plain sight: A longitudinal study of combosquatting abuse," in Proc. ACM SIGSAC Conf. Computer and Communications Security (CCS), Dallas, TX, USA, 2017, pp. 569–586, doi: 10.1145/3133956.3134002.`
- Claim at lines 307–308 ("attackers attach words to a brand name"): supported.
- Claim at line 374 ("starts with it (combosquatting {kintis})"): the paper's rule is narrower than Kintis's definition, which includes brand-in-the-middle and prefix forms such as secure-example and myexample. This is fine if the authors present it as a subset. Suggested wording: "starts with it (a common form of combosquatting {kintis})". Per-token matching after splitting on hyphens would still catch secure-paypal; check how tokens are split.

### Gaps
- None for the bibliographic details.

## agten: Agten, Joosen, Piessens, Nikiforakis, NDSS 2015

### Takeaway
All details are correct: authors, order, initials, title and venue/year. NDSS papers have no page numbers. A DOI exists (10.14722/ndss.2015.23058) and should be added. The paper's typo model is Damerau-Levenshtein distance 1 (insertion, deletion, substitution, adjacent permutation), which matches the paper's one-edit typosquat rule.

### Cited Findings
- Crossref for DOI 10.14722/ndss.2015.23058 gives "Seven Months' Worth of Mistakes: A Longitudinal Study of Typosquatting Abuse". Container: Proceedings 2015 Network and Distributed System Security Symposium, 2015. Authors: Pieter Agten, Wouter Joosen, Frank Piessens, Nick Nikiforakis. — [Crossref](https://api.crossref.org/works/10.14722/ndss.2015.23058)
- The NDSS 2015 programme page lists the same four authors (misspelled there as "Piessensand") and links the paper PDF. — [NDSS 2015 paper page](https://www.ndss-symposium.org/ndss2015/ndss-2015-programme/seven-months-worth-mistakes-longitudinal-study-typosquatting-abuse/); [NDSS PDF](https://www.ndss-symposium.org/wp-content/uploads/2017/09/01_3_1.pdf)
- From the abstract: they "collected data about the typosquatting domains of the 500 most popular sites of the Internet every day, for a period of seven months". They found "95% of the popular domains we investigated are actively targeted by typosquatters". — [NDSS PDF](https://www.ndss-symposium.org/wp-content/uploads/2017/09/01_3_1.pdf)
- Typo model: the most frequent typos "have a Damerau-Levenshtein distance of one… a single character insertion, deletion, substitution or adjacent character permutation". The study uses five models from Wang et al.: missing-dot, character-omission, character-permutation, character-substitution (keyboard-adjacent) and character-duplication. — [NDSS PDF](https://www.ndss-symposium.org/wp-content/uploads/2017/09/01_3_1.pdf)

### Inferences
- Corrected IEEE string:
  `P. Agten, W. Joosen, F. Piessens, and N. Nikiforakis, "Seven months' worth of mistakes: A longitudinal study of typosquatting abuse," in Proc. Network and Distributed System Security Symp. (NDSS), San Diego, CA, USA, 2015, doi: 10.14722/ndss.2015.23058.`
  The San Diego location is from general knowledge of NDSS 2015, not checked in this session; omit it if unsure.
- Claims at lines 307–308 ("change one character of it") and line 375 ("one insertion, deletion, substitution, or adjacent swap"): supported by the Damerau-Levenshtein distance 1 framing. Agten's substitution model uses keyboard-adjacent characters only, and the paper's rule (any substitution) is broader. That is fine because Agten cites general distance-1 typos as the most frequent.

### Gaps
- I did not verify the NDSS 2015 venue city against a source in this session.
