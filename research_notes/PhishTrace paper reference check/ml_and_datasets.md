# ML and Datasets References: Bibliographic and Claim Check (prasad, mohammad12, uci327, sahoo, sahingoz, tang, safi, access25)

Scope: the eight REFS entries in /home/maha/Documents/Dst_project/paper/build_paper.py and the sentences that cite them:
- L262-265 (Intro): "...a classifier separates malicious from legitimate pages {sahoo,sahingoz,tang,safi}."
- L290 (Contributions): "...held-out splits of PhiUSIIL {prasad}..."
- L298-302 (Related Work): "Mohammad et al. {mohammad12,uci327} defined widely used website features, and surveys {sahoo,tang,safi,access25} describe lexical, host-based, and content features combined with classifiers such as logistic regression, decision trees, random forests, support vector machines, and gradient boosting. Sahingoz et al. {sahingoz} reported strong results from URL text alone. Prasad and Chandra {prasad} released PhiUSIIL, a large URL dataset with similarity-index features."
- L322-323 (comparison table rows for Prasad and Sahingoz: "ML")
- L449 (Datasets): "PhiUSIIL {prasad} provides 235,795 labeled URLs; ..."

Summary of verdicts:
| Key | Verdict | Fix needed |
|---|---|---|
| prasad | CORRECT | None (optional wording nuance) |
| mohammad12 | CORRECT | None (optional: venue name uses "for", 7th) |
| uci327 | MINOR ERRORS | Year should be 2012 (not 2015); add DOI 10.24432/C51W2X |
| sahoo | CORRECT | None |
| sahingoz | CORRECT (DOI missing) | Optional: add doi 10.1016/j.eswa.2018.09.029 |
| tang | CORRECT (DOI missing) | Optional: add doi 10.3390/make3030034 |
| safi | CORRECT (DOI missing) | Optional: add doi 10.1016/j.jksuci.2023.01.004 |
| access25 | CORRECT (paper exists) | None |

## prasad: Is the PhiUSIIL reference correct, and do "235,795 labeled URLs" and "similarity-index features" hold?

### Takeaway
The reference is fully correct per Crossref (title, both authors, Computers & Security vol. 136, article 103545, Jan. 2024, DOI). The 235,795 count matches UCI dataset 967 and the authors' Mendeley release (134,850 legitimate + 100,945 phishing), and the UCI release does include a URLSimilarityIndex feature, so both claims are supported.

### Cited Findings
- Crossref record for 10.1016/j.cose.2023.103545: title "PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning"; authors Arvind Prasad, Shalini Chandra; container "Computers & Security"; volume 136; article number 103545; issued 2024-01 — [Crossref](https://api.crossref.org/works/10.1016/j.cose.2023.103545)
- UCI dataset 967 "PhiUSIIL Phishing URL (Website)": 235,795 instances, 54 features; "134,850 legitimate and 100,945 phishing URLs"; creators Arvind Prasad and Shalini Chandra; variables include URLSimilarityIndex, CharContinuationRate, TLDLegitimateProb, URLCharProb; intro paper is the C&S article — [UCI API](https://archive.ics.uci.edu/api/dataset?id=967); [UCI page](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset)
- Mendeley Data release (v2, 15 Nov 2023, DOI 10.17632/shwpxscxy2.2) by the same authors states 134,850 legitimate and 100,945 phishing URLs and points to the C&S paper — [Mendeley Data](https://data.mendeley.com/datasets/shwpxscxy2/2)
- Abstract (via search-indexed mirror, not the publisher page, which returned HTTP 403): the similarity index targets visual-similarity attacks (homograph, punycode, zero-width characters, homophone, bit-squatting, combosquatting); reported accuracy 99.24% (fully incremental) and 99.79% (pre-training) — [DBLP record](https://dblp.org/rec/journals/compsec/PrasadC24); [mirror listing](https://bohrium.dp.tech/paper/arxiv/923036550952911099)

### Inferences
- 134,850 + 100,945 = 235,795, so "provides 235,795 labeled URLs" is exactly right.
- "released PhiUSIIL, a large URL dataset with similarity-index features" is defensible (URLSimilarityIndex is a dataset column), but strictly PhiUSIIL is the name of the detection framework; the dataset is the "PhiUSIIL Phishing URL Dataset", and the similarity index is primarily a framework component. Optional rewording: "Prasad and Chandra {prasad} proposed PhiUSIIL, a similarity-index and incremental-learning framework, and released a large labeled URL dataset with it."
- Semantic Scholar lists year 2023 (online-first); the volume year 2024 used in the reference is the correct IEEE citation year.
- Table rows labeling Prasad as "ML" are consistent with the framework being ML-based (incremental learning).

### Gaps
- Could not read the full abstract on ScienceDirect (HTTP 403); the similarity-index description comes from a search-indexed mirror and the UCI variable list, not the publisher page.

## mohammad12: Is the ICITST 2012 reference (title, pages) correct?

### Takeaway
Correct. Title, author order (R. M. Mohammad, F. Thabtah, L. McCluskey), ICITST 2012, and pp. 492-497 are all confirmed by the University of Huddersfield repository and the UCI dataset page. There is no Crossref DOI; the IEEE Xplore document number is 6470857.

### Cited Findings
- Huddersfield Pure record: "An assessment of features related to phishing websites using an automated technique"; Rami M. Mohammad, Fadi Thabtah, Lee McCluskey; 7th International Conference for Internet Technology and Secured Transactions (ICITST 2012), London, 10-12 Dec 2012; pp. 492-497; IEEE; ISBN 9781467353250 (print); IEEE Xplore document 6470857; no DOI listed — [Huddersfield Pure](https://pure.hud.ac.uk/en/publications/an-assessment-of-features-related-to-phishing-websites-using-an-a/)
- UCI dataset 327 lists this paper as its introductory paper (R. Mohammad, F. Thabtah, L. McCluskey, ICITST, 2012) — [UCI API](https://archive.ics.uci.edu/api/dataset?id=327)
- Abstract: proposes automatic extraction of phishing features (long URLs, IP addresses in URL, prefix/suffix in domain, etc.) and assesses each feature's importance — [Huddersfield Pure](https://pure.hud.ac.uk/en/publications/an-assessment-of-features-related-to-phishing-websites-using-an-a/)
- Crossref bibliographic search returned no match for this title (no DOI registered) — [Crossref query](https://api.crossref.org/works?query.bibliographic=An+assessment+of+features+related+to+phishing+websites+using+an+automated+technique&rows=3)

### Inferences
- The claim "defined widely used website features" is supported: this paper is the intro paper for UCI dataset 327, whose 30 features are widely reused.
- The official venue name uses "for": "International Conference for Internet Technology and Secured Transactions". The current string "Int. Conf. Internet Technology and Secured Transactions" is an acceptable IEEE abbreviation. Optional more precise form:
  `R. M. Mohammad, F. Thabtah, and L. McCluskey, “An assessment of features related to phishing websites using an automated technique,” in Proc. 7th Int. Conf. Internet Technology and Secured Transactions (ICITST), London, U.K., 2012, pp. 492–497.`
- Pure lists publication date 11 March 2013 (Xplore posting), but the conference year 2012 is the standard citation year.

### Gaps
- IEEE Xplore page itself was not fetched; the document number comes from the Huddersfield record.

## uci327: Creators, year, and UCI-recommended citation for "Phishing Websites" (dataset 327)

### Takeaway
MINOR ERRORS. Creators (Rami Mohammad, Lee McCluskey) are right, but UCI's recommended citation uses year 2012 (2015 is only the donation date) and includes DOI 10.24432/C51W2X, which the reference omits.

### Cited Findings
- UCI API: creators "Rami Mohammad", "Lee McCluskey"; year_of_dataset_creation 2012; dataset_doi 10.24432/C51W2X; 11,055 instances, 30 features — [UCI API](https://archive.ics.uci.edu/api/dataset?id=327)
- UCI page: donated 25 March 2015; recommended APA citation "Mohammad, R. & McCluskey, L. (2012). Phishing Websites [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C51W2X."; license CC BY 4.0 — [UCI page](https://archive.ics.uci.edu/dataset/327/phishing+websites)

### Inferences
- Corrected IEEE-format string:
  `R. Mohammad and L. McCluskey, “Phishing Websites,” UCI Machine Learning Repository, 2012, doi: 10.24432/C51W2X.`
  (Optionally keep "Dataset 327": `... UCI Machine Learning Repository, Dataset 327, 2012, doi: 10.24432/C51W2X.`)

### Gaps
- None material.

## sahoo: Is the arXiv:1701.07179 survey reference correct?

### Takeaway
Correct. arXiv metadata confirms title, authors and order (Doyen Sahoo, Chenghao Liu, Steven C. H. Hoi), first posted 25 Jan 2017.

### Cited Findings
- arXiv API for 1701.07179: title "Malicious URL Detection using Machine Learning: A Survey"; authors Doyen Sahoo, Chenghao Liu, Steven C. H. Hoi; published 2017-01-25; last updated 2019-08-21 (later version) — [arXiv](https://arxiv.org/abs/1701.07179)

### Inferences
- Year 2017 (first version) is acceptable; some styles cite the latest version (2019). No change required.
- The survey covers ML-based malicious URL detection with lexical/host/content features, consistent with the citing sentences.

### Gaps
- Did not read the full survey text to confirm each classifier named in the L299-300 sentence (logistic regression, trees, RF, SVM, gradient boosting) is explicitly discussed; the sentence attributes these collectively to four surveys, which is a reasonable general summary.

## sahingoz: Is the ESWA 2019 reference correct, and does it report strong results from URL text alone?

### Takeaway
Correct (all four authors, title, ESWA vol. 117, pp. 345-357, 2019). The claim is supported: Random Forest using only NLP-based features extracted from the URL reached 97.98% accuracy, without third-party services.

### Cited Findings
- Crossref 10.1016/j.eswa.2018.09.029: "Machine learning based phishing detection from URLs"; Ozgur Koray Sahingoz, Ebubekir Buber, Onder Demir, Banu Diri; Expert Systems with Applications vol. 117, pp. 345-357, issued 2019-03 — [Crossref](https://api.crossref.org/works/10.1016/j.eswa.2018.09.029)
- Abstract: real-time system with seven classifiers and NLP-based features; properties include language independence and independence from third-party services; "Random Forest algorithm with only NLP based features gives the best performance with the 97.98% accuracy rate" — [Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.eswa.2018.09.029?fields=abstract)

### Inferences
- Optional addition of DOI:
  `O. K. Sahingoz, E. Buber, O. Demir, and B. Diri, “Machine learning based phishing detection from URLs,” Expert Systems with Applications, vol. 117, pp. 345–357, 2019, doi: 10.1016/j.eswa.2018.09.029.`

### Gaps
- None material.

## tang: Is the MAKE 2021 survey reference correct?

### Takeaway
Correct. Crossref confirms authors, title, Machine Learning and Knowledge Extraction vol. 3, no. 3, pp. 672-694, 2021 (published 20 Aug 2021).

### Cited Findings
- Crossref 10.3390/make3030034: "A Survey of Machine Learning-Based Solutions for Phishing Website Detection"; Lizhen Tang, Qusay H. Mahmoud; vol. 3, issue 3, pp. 672-694; published 2021-08-20 — [Crossref](https://api.crossref.org/works/10.3390/make3030034)

### Inferences
- Optional DOI addition:
  `L. Tang and Q. H. Mahmoud, “A survey of machine learning-based solutions for phishing website detection,” Machine Learning and Knowledge Extraction, vol. 3, no. 3, pp. 672–694, 2021, doi: 10.3390/make3030034.`

### Gaps
- Full text not read; the citing claim (survey of ML phishing-website detection) matches the title.

## safi: Is the JKSU-CIS 2023 reference correct?

### Takeaway
Correct. Crossref confirms authors, title, J. King Saud Univ. Comput. Inf. Sci. vol. 35, no. 2, pp. 590-611, Feb. 2023.

### Cited Findings
- Crossref 10.1016/j.jksuci.2023.01.004: "A systematic literature review on phishing website detection techniques"; Asadullah Safi, Satwinder Singh; Journal of King Saud University - Computer and Information Sciences, vol. 35, issue 2, pp. 590-611, issued 2023-02 — [Crossref](https://api.crossref.org/works/10.1016/j.jksuci.2023.01.004)

### Inferences
- Optional DOI addition:
  `A. Safi and S. Singh, “A systematic literature review on phishing website detection techniques,” J. King Saud Univ. Comput. Inf. Sci., vol. 35, no. 2, pp. 590–611, 2023, doi: 10.1016/j.jksuci.2023.01.004.`

### Gaps
- Full text not read; claim is generic and consistent with the title.

## access25: Does the Kustiawan & Ghauth IEEE Access 2025 review exist, and is the reference correct?

### Takeaway
The paper exists and the reference is correct: Crossref and Semantic Scholar (with a DBLP key) confirm title, authors, IEEE Access vol. 13, pp. 192080-192104, 2025, DOI 10.1109/ACCESS.2025.3630334. Its abstract supports the citing claim (it surveys URL/lexical, HTML/content, domain, behavioral and hybrid features for ML phishing detection). No replacement is needed.

### Cited Findings
- Crossref 10.1109/ACCESS.2025.3630334: "Feature Engineering for Phishing Website Detection Using Machine Learning: A Systematic Review"; IEEE Access vol. 13, pp. 192080-192104, 2025; authors registered as given "Yanche" / family "Ari Kustiawan" and given "Khairil" / family "Imran Ghauth" — [Crossref](https://api.crossref.org/works/10.1109/ACCESS.2025.3630334)
- Semantic Scholar: authors "Yanche Ari Kustiawan", "Khairil Imran Ghauth"; DBLP key journals/access/KustiawanG25c; open access CC BY; abstract says the review categorizes "URL/lexical, HTML/content, domain, behavioral, and emerging derived and hybrid features" and examines feature selection and dimensionality reduction — [Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ACCESS.2025.3630334?fields=title,authors,abstract,year,venue,externalIds); [DOI](https://doi.org/10.1109/ACCESS.2025.3630334)

### Inferences
- Initials "Y. A. Kustiawan and K. I. Ghauth" follow from the registered given/family split (Yanche Ari Kustiawan; Khairil Imran Ghauth). If the authors' own byline treats "Ari Kustiawan" as a compound surname, IEEE would render "Y. Ari Kustiawan"; Crossref's split supports either reading, and the current string is acceptable.
- The citing sentence ("surveys ... describe lexical, host-based, and content features") matches the abstract.

### Gaps
- The IEEE Xplore landing page was not fetched; the author byline formatting is inferred from Crossref/Semantic Scholar metadata.
- DBLP direct query was blocked by a bot-check page, so the DBLP record was seen only via the Semantic Scholar externalIds field.
