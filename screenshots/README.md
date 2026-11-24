# Testing results (screenshots)

Each screenshot is a full PhishTrace report (agentic chain mode) for one URL, with the **Score and evidence** section opened. It shows the verdict, the risk score, the rules that fired, the agent trail, the completeness checklist, the verified findings, and the exhibits that support them.

PhishTrace reads only the URL text. None of these pages were opened.

> **Warning:** the phishing and malware URLs below are real and may still be live. Do not open them in a browser. Paste them into PhishTrace only.

## How the URLs were chosen

- **Phishing:** real links from [Phishing.Database](https://github.com/Phishing-Database/Phishing.Database) (MIT license), active list of 4 Nov 2026.
- **Malware:** real links from [URLhaus](https://urlhaus.abuse.ch/) via the malware-filter mirror, online list of 8 Nov 2026.
- **Safe:** well-known legitimate sites.

Case 01 is the made-up classroom example from the main README.

**These are hand-picked examples, not a detection test.** The URLs were chosen after looking at their scores. Cases 15–24 were searched for among links that name a well-known brand, and links rated not phishing were skipped, so all ten were certain to raise an alert.

- The real phishing URLs (02–06 and 15–24) are in the held-out test split used by `scripts/evaluate.py`.
- The two malware URLs (07 and 08) are in the **development split**, so they are not held-out examples.

Case 06 is a real phishing link that PhishTrace misses. It is included on purpose, because it shows the recall limit discussed in the paper: some phishing URLs carry no warning sign in their text.

## Results

| # | Screenshot | Type | URL | Verdict | Score | Rules that fired |
|---|---|---|---|---|---|---|
| 01 | [paypal-lookalike](01_phishing_paypal-lookalike.png) | Phishing (classroom example) | `http://paypa1-secure-login.tk/verify/account` | Phishing / malicious | 70 | Brand mismatch, Higher-abuse suffix, Explicit HTTP, Lure words |
| 02 | [steam-brand-mismatch](02_phishing_steam-brand-mismatch.png) | Phishing | `https://steamcommunity.appwallpapersenginse.com/sharedfiles/filedetails/id113426354` | Phishing / malicious | 28 | Brand mismatch |
| 03 | [microsoft-login-on-cloud-storage](03_phishing_microsoft-login-on-cloud-storage.png) | Phishing | `https://objectstorage.eu-paris-1.oraclecloud.com/n/idrlconj5yne/b/fhdjfhfhfd/o/login.microsoftonline.htm` | Phishing / malicious | 38 | Long URL, Lure words, Free hosting platform |
| 04 | [raw-ip-hex-folder](04_phishing_raw-ip-hex-folder.png) | Phishing | `http://206.189.87.184/online/atb/7ded47b5647a197ba615b0eba4790fc4/last.html` | Phishing / malicious | 48 | Raw IP host, Explicit HTTP, Hex-code folder |
| 05 | [free-hosting-hyphens](05_suspicious_free-hosting-hyphens.png) | Phishing | `https://uphold-com--x-cdn-sso.webflow.io` | Suspicious | 30 | Many hyphens, Free hosting platform |
| 06 | [plain-domain (missed)](06_missed_phishing-plain-domain.png) | Phishing | `https://www.artecplan.com.br/mylifebox11/0ffice2023/office-3d8/index.php` | **Not phishing (missed)** | 0 | none |
| 07 | [archive-download](07_malware_archive-download.png) | Malware | `http://github.com/roninelengine/circumvent-discord/releases/download/1.10.1/zapret-discord-youtube-1.10.2.zip` | Suspicious | 34 | Explicit HTTP, Long URL, Program or archive download |
| 08 | [raw-ip-host](08_malware_raw-ip-host.png) | Malware | `http://94.156.166.84` | Phishing / malicious | 40 | Raw IP host, Explicit HTTP |
| 09 | [google](09_safe_google.png) | Safe | `https://www.google.com` | Not phishing | 0 | none |
| 10 | [github](10_safe_github.png) | Safe | `https://github.com` | Not phishing | 0 | none |
| 11 | [wikipedia](11_safe_wikipedia.png) | Safe | `https://www.wikipedia.org` | Not phishing | 0 | none |
| 12 | [nu-edu-pk](12_safe_nu-edu-pk.png) | Safe | `https://nu.edu.pk` | Not phishing | 0 | none |
| 13 | [paypal-official-signin](13_safe_paypal-official-signin.png) | Safe | `https://www.paypal.com/signin` | Not phishing | 6 | Lure words (weak cue only) |
| 15 | [facebook-login-on-tk](15_phishing_facebook-login-on-tk.png) | Phishing | `https://fb-privacy-1000001234897864561200044-hk.tk/login_to_facebook.html` | Phishing / malicious | 52 | Higher-abuse suffix, Many hyphens, Digit-heavy host, Lure words, Machine-generated label |
| 16 | [microsoft-sharepoint-lookalike](16_phishing_microsoft-sharepoint-lookalike.png) | Phishing | `http://sharepoint-microsoft-online-teams.lumagica.com` | Phishing / malicious | 44 | Brand mismatch, Explicit HTTP, Many hyphens |
| 17 | [apple-icloud-billing](17_phishing_apple-icloud-billing.png) | Phishing | `https://www.mybilling-apple.com/icloud/login.php` | Phishing / malicious | 34 | Brand mismatch, Lure words |
| 18 | [coinbase-on-webflow](18_phishing_coinbase-on-webflow.png) | Phishing | `http://secure-app--coinbasepro--cdn-o-oauth.webflow.io` | Phishing / malicious | 72 | Brand mismatch, Explicit HTTP, Many hyphens, Lure words, Free hosting platform |
| 19 | [chase-on-duckdns](19_phishing_chase-on-duckdns.png) | Phishing | `https://secure80verify-chase.duckdns.org/login.php` | Phishing / malicious | 56 | Brand mismatch, Lure words, Free hosting platform |
| 20 | [wellsfargo-glued-www](20_phishing_wellsfargo-glued-www.png) | Phishing | `https://www--wellsfargo--com--ph49329d48d6c.wsipv6.com` | Phishing / malicious | 72 | Brand mismatch, Many hyphens, Machine-generated label, Glued www or com |
| 21 | [usps-parcel-scam](21_phishing_usps-parcel-scam.png) | Phishing | `https://usps.xxogzrcmhf.top` | Phishing / malicious | 58 | Brand mismatch, Higher-abuse suffix, Machine-generated label |
| 22 | [binance-on-web-app](22_phishing_binance-on-web-app.png) | Phishing | `https://cancel14651181-binance-com.web.app` | Phishing / malicious | 72 | Brand mismatch, Free hosting platform, Glued www or com |
| 23 | [instagram-on-blogspot](23_phishing_instagram-on-blogspot.png) | Phishing | `https://instagramlinkprofile.blogspot.am` | Phishing / malicious | 50 | Brand mismatch, Free hosting platform |
| 24 | [dhl-parcel-brand-mismatch](24_phishing_dhl-parcel-brand-mismatch.png) | Phishing | `https://parcel-dhl.pcbasedsolutions.com/public/cs73gwz8o9xdtreygeixay6itfhl3vfz` | Phishing / malicious | 28 | Brand mismatch |

**What these examples show:** the reports for links the rules catch, one link rated suspicious (05), one real phishing link that is missed (06), and five well-known safe sites rated not phishing. The real PayPal sign-in page (13) is not mistaken for a fake.

**Do not read a detection rate from this table.** The measured rates come from `scripts/evaluate.py` on held-out data, counting phishing and suspicious verdicts as alerts: recall is 0.622 on Phishing.Database, 0.797 on OpenPhish, 0.982 on URLhaus and 0.566 on PhiUSIIL, with false alarms on 0.65% of popular Tranco sites. See the paper and `data/eval_results.json`.

## Three-mode comparison

[14_compare_three-modes_paypal-lookalike.png](14_compare_three-modes_paypal-lookalike.png) runs the same URL (case 01) through all three modes:

| Measure | Rules only | Retrieval only | Agentic chain |
|---|---|---|---|
| Risk score | 70 | 70 | 70 |
| Unsupported-claim rate | 100% | 50% | **0%** |
| Evidence support | 0% | 50% | **100%** |
| Investigation completeness | 25% | 37.5% | **100%** |
| Exhibits used | 0 | 3 | 8 |

## Reproducing

Start the app (`python run.py`) and open `http://localhost:8000/run?url=<URL>&mode=agentic` (or `mode=compare`), or paste the URL on the Investigate page. Report IDs and timestamps differ on every run, but the verdicts and scores are the same.
