# RAG and agent references (lewis, yao, nicklas, li26): bibliographic and claim check

Source of current strings: `/home/maha/Documents/Dst_project/paper/build_paper.py`, lines 53–56 (REFS). Citing sentences: lines 269–271 (intro), 313–314 (Related Work, "Retrieval and Agents for Phishing Analysis"), and Table I rows at lines 324–325.

Summary of verdicts:
| Key | Verdict |
|---|---|
| lewis | CORRECT |
| yao | CORRECT |
| nicklas | MINOR ERRORS: the reference exists and the details are right, but pages and DOI are missing. The claim is accurate. |
| li26 | MINOR ERRORS: the reference exists and the arXiv details are right, but the paper is now formally published (Springer LNICST, ICDF2C 2025, 2026, pp. 88–106), so the citation should be updated. The Table I "Verifier = No" and "Detector = LLM" cells are questionable. |

## lewis: Lewis et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks", NeurIPS 33, 2020, pp. 9459–9474

### Takeaway
CORRECT. Title, venue, volume 33, year 2020 and pages 9459–9474 all match the official NeurIPS proceedings BibTeX. "P. Lewis et al." is acceptable IEEE style for 12 authors. The citing claim fits what the paper does.

### Cited Findings
- Official BibTeX: title "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"; booktitle Advances in Neural Information Processing Systems; volume 33; pages 9459--9474; year 2020; publisher Curran Associates; editors Larochelle, Ranzato, Hadsell, Balcan, Lin. — [NeurIPS BibTeX](https://proceedings.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Bibtex.bib)
- Authors in order: Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela. The first author is P. Lewis. — [NeurIPS abstract page](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)
- The paper is cited as "Retrieval-augmented generation (RAG) attaches retrieved context to an answer {lewis}". RAG conditions a seq2seq generator on passages retrieved from a dense index, so the paraphrase is a fair, if simple, description. — [NeurIPS abstract page](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)

### Inferences
- No change needed. An optional, more complete IEEE form would be: P. Lewis *et al.*, "Retrieval-augmented generation for knowledge-intensive NLP tasks," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 33, 2020, pp. 9459–9474. The current string is already acceptable.

### Gaps
- None.

## yao: Yao et al., "ReAct: Synergizing reasoning and acting in language models", ICLR 2023

### Takeaway
CORRECT. The authors, title and venue (ICLR 2023) are confirmed: arXiv v3 is labeled the ICLR camera-ready version. ICLR has no volume or page numbers, so leaving them out is correct. The citing claim fits what the paper does.

### Cited Findings
- arXiv:2210.03629 title "ReAct: Synergizing Reasoning and Acting in Language Models". Authors in order: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao. The comment on v3 (10 Mar 2023) says it "is the ICLR camera ready version". — [arXiv abs](https://arxiv.org/abs/2210.03629)
- Secondary sources say it was published at ICLR 2023, with the same authors. — [Princeton research portal](https://collaborate.princeton.edu/en/publications/react-synergizing-reasoning-and-acting-in-language-models/); [ReAct GitHub](https://github.com/ysymyth/ReAct)
- The paper is cited as "agent frameworks let a system choose tools step by step {yao}". ReAct interleaves reasoning traces with actions such as Wikipedia search and lookup calls, so the claim is a fair paraphrase. — [arXiv abs](https://arxiv.org/abs/2210.03629)

### Inferences
- No change needed. Optionally, add "Kigali, Rwanda" or the OpenReview URL (openreview.net/forum?id=WE_vluYUL-X).

### Gaps
- The OpenReview page and API both returned a bot challenge, which I did not bypass, so I could not read the official ICLR record or the "notable top 5%" status directly. The ICLR 2023 venue is confirmed by the arXiv camera-ready note and secondary sources. The oral/top-5% status matters only if the paper claims it, and it does not.

## nicklas: Nicklas, Ventulett, Conrad, URAI 2024

### Takeaway
The reference EXISTS and the authors (in order), title, venue and year are correct. MINOR ERRORS: it is missing pages 159–166 and DOI 10.60643/urai.v2024p159, both of which the publisher supplies. The claim and the Table I row are accurate: retrieved phishing examples are added to the prompt, and the output is a boolean phishing/not-phishing value parsed from JSON.

Corrected IEEE reference:
F. Nicklas, N. Ventulett, and J. Conrad, "Enhancing phishing email detection with context-augmented open large language models," in *Proc. Upper-Rhine Artificial Intelligence Symp. (URAI)*, Offenburg, Germany, 2024, pp. 159–166, doi: 10.60643/urai.v2024p159.

### Cited Findings
- Publisher page (OJS, Hochschule Offenburg): title "Enhancing Phishing Email Detection with Context-Augmented Open Large Language Models"; authors Fabian Nicklas, Nicolas Ventulett, Jan Conrad (all at University of Applied Sciences Kaiserslautern); journal "Proceedings of the Upper-Rhine Artificial Intelligence Symposium"; published 31.10.2024. — [URAI article page](https://journals.hs-offenburg.de/index.php/urai/article/view/23)
- The page's citation metadata gives citation_firstpage 159, citation_lastpage 166, DC.Identifier.pageNumber "159-166", DOI 10.60643/urai.v2024p159, and citation_date 2024/10/31. The PDF footers are numbered 159 to 166 (8 pages). — [URAI article page](https://journals.hs-offenburg.de/index.php/urai/article/view/23); [PDF](https://journals.hs-offenburg.de/index.php/urai/article/download/23/20)
- The PDF byline order is "Fabian Nicklas, Nicolas Ventulett, and Prof. Dr.-Ing. Jan Conrad", which matches the reference. The order of the citation_author meta tags is different (Nicklas, Conrad, Ventulett), but the PDF and the copyright line both give Nicklas, Ventulett, Conrad. — [PDF](https://journals.hs-offenburg.de/index.php/urai/article/download/23/20)
- URAI 2024 was held 13–14 Nov 2024 at Hochschule Offenburg, Badstraße 24, Offenburg, so "Offenburg, Germany" is correct. — [URAI 2024 event page](https://events.hs-offenburg.de/event/355/)
- Title variant: the earlier event abstract is titled "...Context-Augmented Open-Source Large Language Models". The published proceedings version says "Open Large Language Models", which matches the paper's string. — [URAI 2024 abstract PDF](https://events.hs-offenburg.de/event/355/contributions/134/attachments/66/156/Phishing_Email_Detection_Abstract.pdf); [URAI article page](https://journals.hs-offenburg.de/index.php/urai/article/view/23)
- Method, from the full PDF, §3.4: the knowledge base is a set of phishing emails, split into blocks of up to 200 characters and embedded with Sentence-BERT (all-MiniLM-L6-v2). Cosine-similarity search retrieves the k = 5 most similar phishing examples, which are inserted into the prompt as few-shot examples ("RAG FSL"). — [PDF](https://journals.hs-offenburg.de/index.php/urai/article/download/23/20)
- Output, from the full PDF, §3.3: a parser extracts the classification from the model's text output "as JSON, holding a boolean variable". RAG FSL uses the same parser, and the prompt asks "Is the following email a phishing mail?" No explanation or report is generated, and there is no verifier component. — [PDF](https://journals.hs-offenburg.de/index.php/urai/article/download/23/20)
- Tested on 5,800 emails (2,900 phishing from Phishing Pot, 2,900 legitimate from CSDMC), with eleven open models. — [PDF](https://journals.hs-offenburg.de/index.php/urai/article/download/23/20)

### Inferences
- "added retrieved context to open language models for phishing email detection, but the output is still a class label" is accurate.
- Table I row (LLM / Retrieval Yes / Verifier No / Report Label) is accurate.
- In the intro, "Recent phishing work uses both [RAG and agent frameworks] ... {nicklas,li26}" is slightly loose, because Nicklas uses RAG with few-shot prompting but no agents. A safer wording would be "uses retrieval and, in some cases, agents".

### Gaps
- None material. The URAI proceedings have no volume number, only the "2024" issue reflected in the DOI.

## li26: Li, Manickam, Chong, Karuppayah, "PhishIntentionLLM", arXiv:2507.15419, 2025

### Takeaway
The reference EXISTS. The arXiv ID, authors (in order) and title are correct, and 2025 is correct for the arXiv version. Since then it has been formally published as a chapter in Springer LNICST, *Digital Forensics and Cyber Crime* (ICDF2C 2025, Part II), pp. 88–106, 2026, DOI 10.1007/978-3-032-22545-0_6. The citation should point to the published version.

The prose claim ("used multi-agent RAG to explain phishing intention") is accurate. Two cells in the Table I row are questionable:
- **Verifier = No:** the framework includes a "Validation Agent" that combines specialist findings, resolves conflicts and weighs evidence.
- **Detector = LLM:** it does not do phishing-versus-benign detection. It assumes the input is phishing and classifies the intention.

Corrected IEEE reference, published version (preferred):
W. Li, S. Manickam, Y.-W. Chong, and S. Karuppayah, "PhishIntentionLLM: Uncovering phishing website intentions through multi-agent retrieval-augmented generation," in *Digital Forensics and Cyber Crime (ICDF2C 2025)*, Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering. Cham, Switzerland: Springer, 2026, pp. 88–106, doi: 10.1007/978-3-032-22545-0_6.

(If the LNICST volume number can be confirmed, insert "vol. NNN" after the series name. I could not confirm it; see Gaps.)

If the authors prefer to keep the arXiv form, the current string is correct as it stands: "...," arXiv:2507.15419, 2025.

### Cited Findings
- arXiv:2507.15419: title "PhishIntentionLLM: Uncovering Phishing Website Intentions through Multi-Agent Retrieval-Augmented Generation". Authors in order: Wenhao Li, Selvakumar Manickam, Yung-wey Chong, Shankar Karuppayah. Single version v1, 21 Jul 2025. Comment: "Accepted by EAI ICDF2C 2025". Subject cs.CR. — [arXiv abs](https://arxiv.org/abs/2507.15419)
- Crossref record: book chapter, same title and authors (Yung-Wey Chong), in "Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering" / "Digital Forensics and Cyber Crime"; pages 88–106; published 2026, first online 3 June 2026; Springer Nature Switzerland, Cham; ISBN 978-3-032-25544-3 (print) and 978-3-032-25545-0 (electronic); event ICDF2C (16th), Miami, USA, 17–19 Nov 2025; series ISSN 1867-8211. — [Crossref DOI 10.1007/978-3-032-22545-0_6](https://api.crossref.org/works/10.1007/978-3-032-22545-0_6)
- Book record: "Digital Forensics and Cyber Crime: 16th EAI International Conference, ICDF2C 2025, Miami, FL, USA, November 17–19, 2025, Proceedings, Part II". Editors: K.-K. R. Choo, A. Perez-Pons, H. Upadhyay, R. Lu, K. P. Chow. The Crossref record has no volume field. — [Crossref book DOI 10.1007/978-3-032-22545-0](https://api.crossref.org/works/10.1007/978-3-032-22545-0)
- Note: the ISBNs returned for the chapter (…25544-3 / …25545-0) do not follow the DOI prefix (…22545-0). I am reporting them as Crossref gives them. Do not cite an ISBN unless you check it on Springer.
- The framework uses vision-language LLMs on website screenshots. Agents: Vision Analysis, Context Enrichment, Classification (multi-label, confidence scores, attached evidence), four category specialists, and a Validation Agent that "integrates specialist findings, resolves conflicts, weighs evidence" and gives the final classification. A feedback loop runs when confidence is low. — [arXiv HTML](https://arxiv.org/html/2507.15419v1)
- RAG knowledge base: a basic threat-pattern repository plus category-specific knowledge repositories. The output is one or more of four intention categories (Credential Theft, Financial Fraud, Malware Distribution, Personal Information Harvesting), with evidence chains and reasoning. — [arXiv HTML](https://arxiv.org/html/2507.15419v1); [arXiv abs](https://arxiv.org/abs/2507.15419)
- The evaluation uses phishing samples only, and the abstract treats detection as prior work. The paper focuses on why a site is phishing, not whether it is. Micro-precision is 0.7895 with GPT-4o, about 95% better than a single-agent baseline. — [arXiv abs](https://arxiv.org/abs/2507.15419); [arXiv HTML](https://arxiv.org/html/2507.15419v1)

### Inferences
- "used multi-agent RAG to explain phishing intention" is accurate.
- **Report = Text:** defensible. The output is intention labels plus evidence and reasoning. "Labels + text" would be more precise.
- **Verifier = No:** contestable. A reviewer could point to the Validation Agent. It reconciles agent outputs and is not a grounding check that drops unsupported report sentences against retrieved evidence, so "No" can be defended under the paper's narrow definition of verifier. The safest fix is to make that definition explicit, for example a footnote: "verifier = a component that checks each report sentence against retrieved evidence; [li26]'s validation agent aggregates agent outputs but does not check grounding". Another option is "Partial".
- **Detector = LLM:** imprecise. PhishIntentionLLM classifies intention for pages already known to be phishing and does not detect phishing. Consider "LLM (intent)" or a footnote.
- "Neither work joins a URL detector, retrieved evidence, and a verifier..." still holds: Li works on screenshots and has no URL detector, and Nicklas works on email.
- The citation key "li26" fits the 2026 published version. If the arXiv form is kept, the printed year 2025 is correct for arXiv.

### Gaps
- I could not confirm the LNICST volume number for ICDF2C 2025 Part II: the Crossref record has no volume field, and the Springer book page returned nothing parseable. Check it on link.springer.com/book/10.1007/978-3-032-22545-0 before adding "vol.".
- The ISBN mismatch noted above is unresolved.
- I read the arXiv v1 HTML, not the published Springer chapter. The camera-ready version may differ slightly (for example, in the agent names).
