# Data-source references (openphish, urlhaus, tranco, phishdb): verification

Checked 2026-11-17 against the live sites and the project's local files. Where the paper cites each key (in `paper/build_paper.py`):
- Line ~290 (contributions list): "two phishing feeds {openphish,phishdb}, a malware feed {urlhaus}, and the Tranco top sites {tranco}".
- Line ~450 (Data section): "a snapshot of OpenPhish {openphish}; active links from Phishing.Database {phishdb}; online malware URLs from URLhaus {urlhaus}, read from the public malware-filter mirror because the URLhaus bulk download now requires an account key; and the top 100,000 domains of the Tranco list {tranco}, read as https homepages, as popular safe sites."
- Table III and the results text (lines ~462-665) name the sources but have no further citation keys.

Local download dates, from `ls -l data/raw/` and the file headers: openphish.txt, phishing-links-active.txt and phishing-ips-active.txt on 2026-11-04. tranco_top1m.csv and urlhaus_filter_online.txt on 2026-11-08 (the mirror header says `Updated: 2026-11-08T00:10:55Z`).

Summary of verdicts:
| Key | Verdict |
|---|---|
| openphish | MINOR ERRORS: add the access date and the official feed name/URL; there is a terms-of-use problem with redistributing samples |
| urlhaus | MINOR ERRORS: the Auth-Key claim is true but should be worded better. Cite the mirror as its own source and describe how it transforms the data. URLhaus is no longer CC0 under the current abuse.ch terms |
| tranco | MINOR ERRORS: authors, title, venue and year are correct. Add the DOI and the list ID 94P72, which I verified byte-for-byte |
| phishdb | MINOR ERRORS: the name and URL are correct. Name the authors, the MIT licence, the version and the access date |

## openphish: name, URL, terms of use for the community feed

### Takeaway
The source exists and the official name is the "Community Feed" (the GitHub repository calls it the "OpenPhish Community Phishing Feed"). It is free, limited and updated every 12 hours. The OpenPhish Terms of Use allow academic research use but forbid commercial use and redistribution or display of the data without written permission. The reference should add an access date, and the project should check that it does not publish OpenPhish URLs (the committed `data/public_sets.json` holds 300-row summary stats and 6 sample URLs).

### Cited Findings
- OpenPhish offers three feeds: Community, Premium and Platinum (plus a Premium Gov Feed for law enforcement). The free one is the "Community Feed", marked "Limited", updated every 12 hours. Its official URL is now `https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt`, and the footnote says "By using the Community Feed, you accept the Terms of Use" — [OpenPhish Phishing Feeds](https://openphish.com/phishing_feeds.html)
- The GitHub repository `openphish/public_feed` has the description "OpenPhish Community Phishing Feed" and was last pushed 2026-11-17 — [GitHub API: openphish/public_feed](https://api.github.com/repos/openphish/public_feed)
- The URL in the README, `https://openphish.com/feed.txt`, still works: today it returns HTTP 200 after redirecting to the GitHub raw URL above (16,023 bytes) — curl check 2026-11-17 of [openphish.com/feed.txt](https://openphish.com/feed.txt)
- The homepage title is "OpenPhish - Phishing Intelligence" — [OpenPhish](https://openphish.com/)
- Terms of Use: "You may use the Services and the information obtained through them for academic, independent, or personal research". Commercial use is prohibited without prior written consent. Without written permission, users may not "license, sell, rent, lease, transfer" the information, create derivative works, or distribute or display the information. The terms disclaim all warranties ("AS IS"). They state no attribution requirement and show no last-updated date — [OpenPhish Terms of Use](https://openphish.com/terms.html)
- The separate Academic Use programme (a real-time academic feed plus a 30-day archive, 60-day access, open only to applicants from accredited institutions) asks users to cite OpenPhish as the data source with the website address and to "Indicate the date the data was accessed". It prohibits commercial use and sharing with third parties — [OpenPhish Academic Use](https://openphish.com/academic_use.html)

### Inferences
- The name "OpenPhish community phishing feed" is acceptable. The official capitalisation is "Community Feed" or "Community Phishing Feed".
- The academic-programme attribution rules (website and access date) formally apply to the academic feed, not the Community Feed. Following them anyway is best practice, and IEEE style for online sources expects an access date in any case.
- Describing the data as "a snapshot of OpenPhish" is accurate. The paper should give the snapshot date (2026-11-04). The ~300 URLs in `data/public_sets.json` are consistent with the Community Feed being a limited sample, which the paper could mention as a limitation (small n).
- Possible terms-of-use problem: `data/public_sets.json` is committed to the public GitHub repository (`mahapara24/phistrace`) and holds 6 verbatim OpenPhish URLs plus derived statistics. The PhishTrace Data page displays them. The terms restrict distributing or displaying the information without written permission. The safe option is to remove the OpenPhish sample URLs from committed or published files, or to ask OpenPhish for permission. Statistics alone are lower risk. The raw feed itself is not committed (`data/raw/` is ignored), which is good.
- Corrected IEEE reference (website/dataset form):
  `OpenPhish, “OpenPhish Community Phishing Feed,” OpenPhish. Accessed: Nov. 4, 2026. [Online]. Available: https://openphish.com/phishing_feeds.html`
  (Using `https://openphish.com/` is also fine. Optionally add the feed file URL `https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt`.) Replacing the bare "2026" with the access date is the main fix.
- The README Data table could list the GitHub raw feed URL as the canonical one. The current link redirects there and still works.

### Gaps
- The Terms of Use page shows no version date, so I could not tell when the current wording took effect.
- I found no explicit OpenPhish statement on whether the Community Feed in particular needs attribution.

## urlhaus: naming, the Auth-Key claim, licence, the malware-filter mirror

### Takeaway
The name "URLhaus: Malware URL exchange" by abuse.ch is correct (the site title is "URLhaus | Malware URL exchange"). The paper's claim that bulk downloads now need an account key is TRUE: abuse.ch has required an Auth-Key since 30 June 2025, and the old free download URLs now return HTTP 410 Gone. However, the key is free. The current abuse.ch Terms of Use (last updated 21 Oct 2026) do NOT put URLhaus under CC0, and they give platform access only to authenticated users. Reading the data through a third-party mirror "because the bulk download requires a key" is therefore a weak justification for reviewers. The mirror also transforms the data (adblock syntax, URL scheme removed, popular-site handling), so it should be cited as its own source.

### Cited Findings
- The page title is "URLhaus | Malware URL exchange" — [URLhaus](https://urlhaus.abuse.ch/)
- "In order to interact with the URLhaus API, you need to obtain an `Auth-Key` first." and "Whenever you try to download a dataset or file from below, you must include your `Auth-Key` in the URL". Example export: `https://urlhaus-api.abuse.ch/v2/files/exports/YOUR-AUTH-KEY-HERE/recent.csv`. The community API is "available free of charge under the fair use principles" — [URLhaus API docs](https://urlhaus.abuse.ch/api/)
- "Starting June 30th 2025, abuse.ch is requiring a new authentication method with 'Auth-Key' header." (release notes dated 26 June 2025) — [Palo Alto Cortex Marketplace: URLhaus Feed](https://cortex.marketplace.pan.dev/marketplace/details/FeedURLhaus)
- The old unauthenticated bulk URLs `https://urlhaus.abuse.ch/downloads/text_online/` and `https://urlhaus.abuse.ch/downloads/csv_recent/` both return HTTP 410 "Gone … Please remove all references to this resource" — curl check 2026-11-17 of [urlhaus.abuse.ch/downloads/text_online/](https://urlhaus.abuse.ch/downloads/text_online/)
- abuse.ch Terms of Use show "Last Updated: 21st October 2026" and "Effective Date: 4th November 2025". Section 3.4 places only Feodo Tracker, SSL Blacklist and YARAify under CC0; URLhaus is not among them. Section 3.1 lets authenticated users use the platforms for "not-for-profit purposes, subject to usage limitations". Section 4.1 says commercial use of MalwareBazaar, URLhaus and ThreatFox "may require a paid subscription, which will be managed by Spamhaus". Section 2.1 gives access only to authenticated users. Section 7.3 prohibits copying or modifying without consent and bars using the data to "customise, train, or otherwise improve any artificial intelligence model" without Spamhaus's written consent. No attribution requirement is stated — [abuse.ch Terms of Use](https://abuse.ch/terms-of-use/)
- The malware-filter project describes itself as "A blocklist of malicious websites that are being used for malware distribution, based on the Database dump (CSV) of Abuse.ch URLhaus", updated twice a day. The README title is "Malicious URL Blocklist" and it says "This repository is not endorsed by Abuse.ch." It is licensed CC0 plus MIT, and it still lists "URLhaus: CC0" — [malware-filter/urlhaus-filter README](https://gitlab.com/malware-filter/urlhaus-filter)
- In the mirror's "Lite version (online links only)", the online status of URLs "is checked by URLhaus" and "the test is not 100% accurate" — [malware-filter/urlhaus-filter README](https://gitlab.com/malware-filter/urlhaus-filter)
- The mirror normally blocks the whole website. For "popular" websites it lists individual pages instead. "Popular" means the Umbrella top 1M (domains + subdomains), the Tranco top 1M, the Cloudflare Radar top 1M, and a custom exclusion list — [malware-filter/urlhaus-filter README](https://gitlab.com/malware-filter/urlhaus-filter)
- The file used (`urlhaus-filter-online.txt`) has the header "Title: Online Malicious URL Blocklist … Expires: 12 hours … Source: https://urlhaus.abuse.ch/api/". On 2026-11-17 it had ~107,200 entries in adblock syntax `||host/path^$all` with the scheme removed, plus ~1,800 bare IP/host lines — download and inspection of [urlhaus-filter-online.txt](https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-online.txt). The project's own parser confirms it strips `||`, `^` and `$…` (`scripts/evaluate.py`, `_urlhaus()`).

### Inferences
- "requires an account key" is accurate but incomplete. Better wording: "requires a free abuse.ch Auth-Key (since June 2025)". As written, a reviewer may read it as working around an access control. Section 2.1 of the terms gives access only to authenticated users, and the mirror is "not endorsed by Abuse.ch". Two options: (a) register for the free key and download the URLhaus export directly, which is the cleanest; or (b) keep the mirror but say it was chosen for reproducibility (no key needed to reproduce), cite it separately, and state its transformations.
- Licence: anyone claiming CC0 for URLhaus (including the mirror's README) is out of date relative to the current abuse.ch terms. The paper should not say CC0. It can say the data are free for not-for-profit use under the abuse.ch fair-use terms. The AI-training ban does not appear to apply to a rule-based system. Rules were inspected on a development split; this is not model training, but the authors should judge whether "improve" could be read broadly.
- Methodological caveats for the paper: (1) the mirror removes the http/https scheme, so any scheme-based rule (e.g. the "Explicit HTTP" indicator) cannot fire on these items the way it would on raw URLhaus URLs; (2) the mirror's "online" status comes from URLhaus and is not 100% accurate; (3) the mirror handles Tranco/Umbrella/Radar-popular domains differently from other domains, which links the malware set to the Tranco benign set. The paper should state (1) and (3) briefly.
- The paper text says "online malware URLs from URLhaus". This is accurate in substance, but the items are adblock filter entries derived from URLhaus, not raw URLhaus URLs.
- Corrected IEEE references, splitting into two entries (recommended):
  `abuse.ch, “URLhaus: Malware URL exchange,” abuse.ch. Accessed: Nov. 8, 2026. [Online]. Available: https://urlhaus.abuse.ch/`
  `malware-filter, “Malicious URL Blocklist (urlhaus-filter), online version,” GitLab repository. Accessed: Nov. 8, 2026. [Online]. Available: https://gitlab.com/malware-filter/urlhaus-filter`
  If one entry must stay, the current string is acceptable after replacing "2026" with "Accessed: Nov. 8, 2026." and changing the parenthetical to "(accessed via the malware-filter urlhaus-filter mirror, https://gitlab.com/malware-filter/urlhaus-filter, version of Nov. 8, 2026)".

### Gaps
- I could not find a primary abuse.ch announcement dating when URLhaus moved away from CC0, or confirming that it was ever CC0. The Auth-Key date (30 June 2025) comes from a vendor release note (Palo Alto Cortex), not from abuse.ch itself.
- I did not identify the individual maintainer of malware-filter from a primary source, so the reference uses the project name as the author.

## tranco: authors, title, venue; citation practice and list ID

### Takeaway
The authors, title, venue and year are correct. Tranco asks users to cite the NDSS 2019 paper and advises giving the specific list's generation date and permanent link in the text or a footnote. The local `tranco_top1m.csv` is byte-identical (same SHA-256) to Tranco list **94P72**, generated 7 Nov 2026. The paper should state this ID, which it currently does not.

### Cited Findings
- Each Tranco list page says: "We request that you cite our publication: Victor Le Pochat, Tom Van Goethem, Samaneh Tajalizadehkhoob, Maciej Korczyński, and Wouter Joosen. 2019. 'Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation,' Proceedings of the 26th Annual Network and Distributed System Security Symposium (NDSS 2019). https://doi.org/10.14722/ndss.2019.23386". It continues: "We also advise you to reference the list in your text and include a link to this specific list as a footnote, for example as follows: We use the Tranco list [1] generated on <date> … Available at https://tranco-list.eu/list/<ID>." — [Tranco list page (example K97GW)](https://tranco-list.eu/list/K97GW/1000000)
- The BibTeX given there has booktitle "Proceedings of the 26th Annual Network and Distributed System Security Symposium", series NDSS 2019, month Feb, doi 10.14722/ndss.2019.23386 — [Tranco list page](https://tranco-list.eu/list/K97GW/1000000)
- The NDSS page lists the five authors with affiliations (imec-DistriNet KU Leuven; Delft University of Technology; Grenoble Alps University) and links the paper PDF `ndss2019_01B-3_LePochat_paper.pdf` — [NDSS 2019 paper page](https://www.ndss-symposium.org/ndss-paper/tranco-a-research-oriented-top-sites-ranking-hardened-against-manipulation/)
- The DOI 10.14722/ndss.2019.23386 resolves (HTTP 302) to that NDSS PDF — curl check of [doi.org/10.14722/ndss.2019.23386](https://doi.org/10.14722/ndss.2019.23386)
- The Tranco homepage describes the service as providing "permanent citable references" — [Tranco](https://tranco-list.eu/)
- The Tranco API shows that the daily list for 2026-11-07 is ID `94P72`, created 2026-11-07T22:00 UTC. It is built from crux, farsight, majestic, radar and umbrella, over 2026-10-09 to 2026-11-07, using the Dowdall rule with pay-level-domain filtering — [Tranco API, lists by date](https://tranco-list.eu/api/lists/date/2026-11-07)
- I downloaded `https://tranco-list.eu/download/94P72/1000000` and compared it with `data/raw/tranco_top1m.csv`: SHA-256 `2019dae9…2776` for both, and `cmp` reports them IDENTICAL — [Tranco list 94P72](https://tranco-list.eu/list/94P72)

### Inferences
- The current reference string is correct but bare. Add the edition number, the month and the DOI:
  `V. Le Pochat, T. Van Goethem, S. Tajalizadehkhoob, M. Korczyński, and W. Joosen, “Tranco: A research-oriented top sites ranking hardened against manipulation,” in Proc. 26th Annu. Netw. Distrib. Syst. Secur. Symp. (NDSS), Feb. 2019, doi: 10.14722/ndss.2019.23386.`
  (The long form "in Proc. 26th Annual Network and Distributed System Security Symposium (NDSS 2019)" is also fine. Location: NDSS 2019 was in San Diego, CA, but this came from general knowledge and was not verified in this session.)
- The paper should name the list, e.g. in the Data section: "…the top 100,000 domains of the Tranco list [n] generated on 7 November 2026 (ID 94P72, https://tranco-list.eu/list/94P72)". It can do this in the text or a footnote, or as a second reference: `Tranco, “Tranco list 94P72,” generated Nov. 7, 2026. [Online]. Available: https://tranco-list.eu/list/94P72`. Without the ID, the false-alarm numbers on "Tranco top-100k" cannot be reproduced, because the README says only "latest list".
- "Top sites" / "popular safe sites" is a reasonable description, but Tranco measures popularity, not safety. A short caveat that some ranked domains may host abuse would strengthen the paper (the paper already notes "brand token on brand infrastructure" alarms).

### Gaps
- I could not reach DBLP (its API returned non-JSON), so the bibliographic data rests on the Tranco site, the NDSS page and the DOI, all primary sources.
- The NDSS 2019 page range is not shown on the pages I fetched. NDSS papers are usually cited without pages.

## phishdb: name, owner, licence

### Takeaway
The name "Phishing.Database" and the URL are correct. The repository belongs to the GitHub organisation **Phishing-Database**. It was previously `mitchellkrogza/Phishing.Database`, which now redirects with HTTP 301. The README credits Mitchell Krog (@mitchellkrogza) and Nissar Chababy (@funilrys) plus "Phishing.Database Contributors". It is MIT-licensed. Its files were last updated 2 Oct 2026 (version V.2026-10-02.17), so the "active" lists the paper used were about a month old when downloaded.

### Cited Findings
- The repository is maintained under the Phishing-Database organisation. The README lists Mitchell Krog (@mitchellkrogza) and Nissar Chababy (@funilrys) as authors. The licence is MIT, "Copyright (c) 2018-2025 Mitchell Krog, Nissar Chababy, and Phishing.Database Contributors". The current version is V.2026-10-02.17. It provides `phishing-links-ACTIVE.txt` and `phishing-IPs-ACTIVE.txt`, also served from `https://phish.co.za/latest/…`. The repository is not archived — [Phishing.Database on GitHub](https://github.com/Phishing-Database/Phishing.Database)
- GitHub API: full_name "Phishing-Database/Phishing.Database", created 2018-04-20, pushed_at 2026-10-02T15:30:35Z, archived false, licence spdx_id MIT. Description: "Phishing Domains, urls websites and threats database. We use the PyFunceble testing tool to validate the status of all known Phishing domains…" — [GitHub API](https://api.github.com/repos/Phishing-Database/Phishing.Database)
- `https://github.com/mitchellkrogza/Phishing.Database` returns 301 to `https://github.com/Phishing-Database/Phishing.Database` — curl check 2026-11-17 of [github.com/mitchellkrogza/Phishing.Database](https://github.com/mitchellkrogza/Phishing.Database)
- "ACTIVE" status comes from automated testing with PyFunceble, by Nissar Chababy (@funilrys). The project actively retests domains and URLs on a regular basis — [Phishing.Database README](https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/master/README.md)
- The README gives no citation format. It asks: "If you've featured Phishing.Database in an article or research paper, let us know" (contact@phish.co.za) — [Phishing.Database README](https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/master/README.md)
- Today the GitHub raw `phishing-links-ACTIVE.txt` is 65,823,890 bytes and `phishing-IPs-ACTIVE.txt` is 100,533 bytes. These are exactly the sizes of the project's local copies (downloaded 2026-11-04), consistent with no update since 2026-10-02. `https://phish.co.za/latest/phishing-links-ACTIVE.txt` returned HTTP 503 today — curl checks 2026-11-17 of [phishing-links-ACTIVE.txt](https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/master/phishing-links-ACTIVE.txt)

### Inferences
- The author is better given as people than as "Phishing Database Project". Corrected IEEE reference:
  `M. Krog, N. Chababy, and Phishing.Database contributors, “Phishing.Database,” GitHub repository, version V.2026-10-02.17, 2026. Accessed: Nov. 4, 2026. [Online]. Available: https://github.com/Phishing-Database/Phishing.Database`
  (Using the organisation "Phishing.Database" as the author is also acceptable. The present string's organisation name, title and URL are all correct.)
- "Active links" is accurate, but "active" means PyFunceble found the URL reachable at its last test. It does not mean the page was re-confirmed as phishing. The list is cumulative and was last refreshed on 2 Oct 2026. The paper should note this as possible label noise (some "active" URLs may be parked or cleaned).
- The MIT licence allows academic use and redistribution with the copyright notice. Unlike OpenPhish, there is no terms-of-use concern.
- Consistency fix in the project, not the paper: the committed `data/public_sets.json` still cites `https://github.com/mitchellkrogza/Phishing.Database` and "Mitchell Krog" alone. The link redirects, but the canonical URL is the Phishing-Database organisation. The README names the files `phishing-links-active.txt` and `phishing-ips-active.txt` in lowercase; upstream they are `phishing-links-ACTIVE.txt` and `phishing-IPs-ACTIVE.txt`.
- The README says both the links file and the IPs file are used. The paper sentence mentions only "active links". If the IP list is also part of the Phishing.Database test set, the paper should say so.

### Gaps
- I did not check whether `scripts/evaluate.py` includes the IPs file in the Phishing.Database recall set, because that is outside the scope of reference verification.
- I found no explicit statement of how often the ACTIVE lists are retested beyond "regularly", and none on why the repository has not been updated since 2 Oct 2026.
