"""Local exhibits, brand list, and suffix notes.

The prose is written for this workbench. It is not a quotation of the papers
in the proposal, and it is not a live threat feed.
"""

from __future__ import annotations

import hashlib

BRANDS: dict[str, list[str]] = {
    "paypal": ["paypal.com", "paypal.co.uk", "paypal.com.au", "paypal.ca", "paypal.de", "paypal.in"],
    "microsoft": [
        "microsoft.com",
        "microsoftonline.com",
        "live.com",
        "office.com",
        "office365.com",
        "outlook.com",
        "windows.com",
    ],
    "google": [
        "google.com",
        "google.co.uk",
        "google.de",
        "google.fr",
        "google.ca",
        "google.com.au",
        "google.co.in",
        "gmail.com",
        "youtube.com",
        "googleapis.com",
        "gstatic.com",
        "googleusercontent.com",
    ],
    "apple": ["apple.com", "apple.co.uk", "icloud.com"],
    "amazon": ["amazon.com", "amazon.co.uk", "amazon.in", "amazon.ca", "amazon.de", "amazonaws.com"],
    "facebook": ["facebook.com", "fb.com"],
    "instagram": ["instagram.com"],
    "netflix": ["netflix.com"],
    "linkedin": ["linkedin.com"],
    "dropbox": ["dropbox.com"],
    "adobe": ["adobe.com"],
    "dhl": ["dhl.com"],
    "fedex": ["fedex.com"],
    "irs": ["irs.gov"],
    "chase": ["chase.com"],
    "wellsfargo": ["wellsfargo.com"],
    "bankofamerica": ["bankofamerica.com"],
    "whatsapp": ["whatsapp.com"],
    "github": ["github.com"],
    "yahoo": ["yahoo.com", "yahoo.co.jp", "ymail.com"],
    "aol": ["aol.com"],
    "office365": ["office365.com", "office.com", "microsoft.com"],
    "onedrive": ["onedrive.com", "live.com", "microsoft.com"],
    "sharepoint": ["sharepoint.com", "microsoft.com"],
    "outlook": ["outlook.com", "live.com", "office.com"],
    "docusign": ["docusign.com", "docusign.net"],
    "coinbase": ["coinbase.com"],
    "binance": ["binance.com"],
    "metamask": ["metamask.io"],
    "steam": ["steampowered.com", "steamcommunity.com"],
    "roblox": ["roblox.com"],
    "ebay": ["ebay.com", "ebay.co.uk", "ebay.de"],
    "walmart": ["walmart.com"],
    "spotify": ["spotify.com"],
    "telegram": ["telegram.org", "t.me"],
    "twitter": ["twitter.com", "x.com"],
    "usps": ["usps.com"],
    "verizon": ["verizon.com"],
    "xfinity": ["xfinity.com", "comcast.net"],
    "rakuten": ["rakuten.co.jp", "rakuten.com"],
    "hsbc": ["hsbc.com", "hsbc.co.uk"],
    "santander": ["santander.com", "santander.co.uk"],
    "citibank": ["citi.com", "citibank.com"],
    "americanexpress": ["americanexpress.com"],
    "mastercard": ["mastercard.com"],
}

BRAND_DISPLAY = {
    "paypal": "PayPal",
    "irs": "IRS",
    "github": "GitHub",
    "linkedin": "LinkedIn",
    "whatsapp": "WhatsApp",
    "wellsfargo": "Wells Fargo",
    "bankofamerica": "Bank of America",
    "aol": "AOL",
    "office365": "Office 365",
    "onedrive": "OneDrive",
    "sharepoint": "SharePoint",
    "docusign": "DocuSign",
    "metamask": "MetaMask",
    "ebay": "eBay",
    "usps": "USPS",
    "hsbc": "HSBC",
    "americanexpress": "American Express",
}

# Brands this short are matched only as a whole piece, never as a prefix or a typo.
EXACT_ONLY = {"aol", "dhl", "irs", "usps", "hsbc", "ebay"}

# Brands that are also ordinary words. A longer piece counts only when the extra
# text is an account or service word, as in appleid or steamcommunitysupport.
WORD_BRANDS = {"apple", "steam", "chase", "outlook", "spotify"}
WORD_BRAND_TAILS = (
    "id", "support", "store", "care", "login", "secure", "account", "verify", "pay", "help",
    "icloud", "online", "community", "service", "services", "billing", "wallet", "bank", "signin",
    "update", "gift", "card", "mail",
)

# Hosted-site and free-hosting platforms. A site on one of these needs no domain
# registration, so the registrable domain says nothing about who runs the page.
# Listed because phishing kits are often deployed there (APWG and Interisle reports).
FREE_HOSTS = {
    "000webhostapp.com", "web.app", "firebaseapp.com", "appspot.com", "workers.dev", "pages.dev",
    "r2.dev", "vercel.app", "netlify.app", "herokuapp.com", "glitch.me", "repl.co", "replit.app",
    "github.io", "gitlab.io", "weebly.com", "weeblysite.com", "wixsite.com", "wix.com",
    "godaddysites.com", "webflow.io", "myportfolio.com", "square.site", "blogspot.com",
    "wordpress.com", "sites.google.com", "run.app", "pantheonsite.io", "webwave.dev",
    "temporary.site", "ngrok.io", "ngrok-free.app", "trycloudflare.com", "dweb.link",
    "ipfs.io", "cf-ipfs.com", "fleek.co", "surge.sh", "onrender.com", "fly.dev", "azurewebsites.net",
    "jimdosite.com", "strikingly.com", "mystrikingly.com", "carrd.co", "framer.app",
    "notion.site", "translate.goog", "linktr.ee", "typedream.app", "zyrosite.com", "site123.me",
    "ukit.me", "tilda.ws", "yolasite.com", "webnode.page", "mobirisesite.com",
}

MULTI_SUFFIXES = {
    "co.uk",
    "org.uk",
    "ac.uk",
    "gov.uk",
    "com.au",
    "net.au",
    "org.au",
    "edu.au",
    "co.in",
    "ac.in",
    "net.in",
    "org.in",
    "co.jp",
    "com.br",
    "com.pk",
    "com.mx",
    "co.za",
    "com.sg",
    "com.hk",
    "co.nz",
    "com.tr",
    "co.id",
    "co.ke", "com.tw", "co.il", "com.ph", "com.ar", "com.cn", "com.ng", "co.kr", "or.jp", "ne.jp", "ac.jp",
    "com.vn", "com.my", "com.eg", "com.sa", "org.br", "gov.in", "edu.in", "co.th", "com.co", "com.pe",
    "com.ua", "com.pl", "co.uk.com", "org.nz", "ac.nz", "com.bd", "com.np", "com.lk", "edu.pk", "gov.pk",
    "org.pk", "net.pk", "web.id", "my.id", "or.id", "ac.id", "go.id", "biz.id",
}

SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
    "rb.gy",
    "shorturl.at",
    "tiny.cc",
}

SUSPICIOUS_TLDS = {
    "tk",
    "ml",
    "ga",
    "cf",
    "gq",
    "xyz",
    "top",
    "click",
    "work",
    "fit",
    "buzz",
    "monster",
    "download",
    "country",
    "rest",
    "cam",
    "loan",
    "men",
    "date",
    "racing",
    "stream",
    "science",
    "gdn",
    "support",
    "review",
    "pw",
    "link",
    "site",
    "online",
    "club",
    "icu",
    "cyou",
    "sbs",
    "cfd",
    "bond",
    "lat",
    "shop",
    "live",
    "vip",
    "biz",
    "ss",
}

LURE_WORDS = (
    "login",
    "signin",
    "verify",
    "verification",
    "secure",
    "account",
    "accounts",
    "update",
    "banking",
    "password",
    "confirm",
    "confirmation",
    "wallet",
    "suspend",
    "unlock",
    "invoice",
    "billing",
    "credential",
    "webscr",
    "webmail",
    "authenticate",
    "authentication",
    "validate",
    "validation",
    "recovery",
    "restore",
    "suspended",
    "locked",
    "payment",
    "refund",
    "reward",
    "airdrop",
    "giveaway",
    "wp-admin",
    "wp-includes",
    "wp-content",
    "redirect",
    "token",
    "otp",
)

DOCS: list[dict[str, object]] = [
    {
        "id": "ex-raw-ip",
        "title": "Raw IP address as the host",
        "tags": ["raw_ip"],
        "source": "Local exhibit · Host",
        "text": (
            "When the host is an IPv4 or IPv6 address, the URL has no domain name. "
            "The usual domain comparison cannot be done, and the address may point at a short-lived server. "
            "This exhibit supports the raw-IP indicator only. An address host is one signal, not a finished finding of fraud."
        ),
    },
    {
        "id": "ex-userinfo",
        "title": "User information before the @ sign",
        "tags": ["userinfo_at"],
        "source": "Local exhibit · Host",
        "text": (
            "Text before an @ sign in the authority is user information. The browser contacts the host that follows the @. "
            "A familiar name written before the @ is not the site being opened. "
            "This exhibit supports the user-information indicator."
        ),
    },
    {
        "id": "ex-brand",
        "title": "Brand token on an unlisted domain",
        "tags": ["brand_mismatch"],
        "source": "Local exhibit · Brand",
        "text": (
            "A brand-like token on a registrable domain that is not that brand's listed domain is a lookalike signal. "
            "The token may swap a digit for a letter. The brand registry, not this paragraph, decides whether the domain is listed. "
            "This exhibit supports the brand-mismatch indicator."
        ),
    },
    {
        "id": "ex-tld",
        "title": "Higher-abuse public suffixes",
        "tags": ["suspicious_tld"],
        "source": "Local exhibit · Suffix",
        "text": (
            "Some suffixes are cheap to register and appear often in abuse reports. In this workbench the higher-abuse list includes "
            "tk, ml, ga, cf, gq, xyz, top, click, work, fit, buzz, monster, download, country, rest, cam, loan, men, date, racing, "
            "stream, science, gdn, support, review, pw, link, site, online, club, icu, cyou, sbs, cfd, bond, lat, shop, live, vip, biz, and ss. "
            "The added suffixes follow the most-abused lists in the Interisle Phishing Landscape and Spamhaus reports. A suffix supports the suspicious-suffix indicator only. "
            "Ordinary sites use these suffixes too, so the signal stays weak on its own."
        ),
    },
    {
        "id": "ex-punycode",
        "title": "Punycode host labels",
        "tags": ["punycode"],
        "source": "Local exhibit · Encoding",
        "text": (
            "A domain label that begins with xn-- is Punycode, the encoding used for internationalized names. "
            "Decoded characters can resemble a Latin brand. This exhibit supports the Punycode indicator. "
            "The workbench does not carry a homoglyph dictionary, so the flag is the encoding itself."
        ),
    },
    {
        "id": "ex-shortener",
        "title": "Shortening hosts hide the destination",
        "tags": ["shortener"],
        "source": "Local exhibit · Host",
        "text": (
            "A shortening host such as bit.ly, tinyurl.com, t.co, goo.gl, ow.ly, is.gd, or cutt.ly replaces the destination with a short path. "
            "The destination is not visible in the URL string. This workbench does not follow redirects. "
            "This exhibit supports the shortener indicator."
        ),
    },
    {
        "id": "ex-https",
        "title": "Explicit plain HTTP",
        "tags": ["no_https"],
        "source": "Local exhibit · Scheme",
        "text": (
            "A page that asks for secrets should use HTTPS. This workbench adds weight only when the typed URL uses the http scheme. "
            "A missing scheme is treated as unknown, not as proof of plain HTTP. A lock is also not proof that the host is honest, "
            "because a certificate can be issued to a lookalike. This exhibit supports the explicit-HTTP indicator."
        ),
    },
    {
        "id": "ex-length",
        "title": "Long URL text",
        "tags": ["long_url", "very_long_url"],
        "source": "Local exhibit · Shape",
        "text": (
            "A long string can push the host out of view behind a trail of path and query text. "
            "This workbench adds weight at 90 characters and adds more at 140. "
            "This exhibit supports the long-URL indicators. Length is also common on ordinary tracking links, so it stays a small weight."
        ),
    },
    {
        "id": "ex-subdomains",
        "title": "Many labels to the left of the registrable domain",
        "tags": ["deep_subdomains"],
        "source": "Local exhibit · Host",
        "text": (
            "Labels to the left of the registrable domain are subdomains. Three or more extra labels leave room for a familiar word "
            "far from the domain that is actually registered. This exhibit supports the deep-subdomain indicator."
        ),
    },
    {
        "id": "ex-hyphens",
        "title": "Hyphens glued into the host",
        "tags": ["many_hyphens"],
        "source": "Local exhibit · Shape",
        "text": (
            "Hyphens join extra words onto a host name. This workbench flags a host with three or more hyphens. "
            "This exhibit supports the hyphen indicator and does not, by itself, name the site as hostile."
        ),
    },
    {
        "id": "ex-lure",
        "title": "Credential and account words",
        "tags": ["lure_terms"],
        "source": "Local exhibit · Wording",
        "text": (
            "Words such as login, signin, verify, verification, secure, account, accounts, update, banking, password, confirm, "
            "wallet, suspend, unlock, invoice, billing, credential, webmail, authenticate, validate, recovery, payment, refund, reward, airdrop, and token are common on real sign-in pages and on copies. "
            "This exhibit supports the lure-word indicator. On a listed official domain the weight is capped, because those words belong there. "
            "The cap does not clear an email leftover such as =3D in the same URL."
        ),
    },
    {
        "id": "ex-quoted-printable",
        "title": "Equals sign left encoded as =3D",
        "tags": ["quoted_printable"],
        "source": "Local exhibit · Email encoding",
        "text": (
            "Quoted-printable mail encodes an equals sign as the three characters =3D. "
            "A command that was typed with a bare equals sign therefore shows up in raw mail with =3D in its place. "
            "PhishTank's high-risk collection, published by Korkmaz, Kocyigit, Sahingoz, and Diri in 2022, contains many copies of that leftover on PayPal-styled addresses. "
            "This exhibit supports the email-encoding indicator. A percent-encoded equals sign (%3D) is ordinary URL encoding and is not this indicator. "
            "The workbench does not open the page. A listed host means the domain is not a lookalike; the encoded command is still the form copied from phishing mail."
        ),
    },
    {
        "id": "ex-port",
        "title": "Nonstandard port",
        "tags": ["unusual_port"],
        "source": "Local exhibit · Host",
        "text": (
            "Ordinary web pages use port 443 or port 80. Another port is recorded as its own indicator. "
            "This exhibit supports the unusual-port indicator. The workbench does not open that port."
        ),
    },
    {
        "id": "ex-encoding",
        "title": "Heavy percent-encoding",
        "tags": ["heavy_encoding"],
        "source": "Local exhibit · Encoding",
        "text": (
            "Percent-encoding writes a character as a percent sign plus two hex digits. A short run of encodings is normal in a query. "
            "Four or more in one URL support the heavy-encoding indicator. Encoding is not proof about the intent of the destination."
        ),
    },
    {
        "id": "ex-digits",
        "title": "Digit-heavy host",
        "tags": ["digit_heavy_host"],
        "source": "Local exhibit · Shape",
        "text": (
            "A host crowded with digits can sit beside a familiar word while looking slightly different. "
            "This workbench flags a host when digits are at least 30 percent of its letters and digits, and the host is not an IP address. "
            "This exhibit supports the digit-heavy host indicator."
        ),
    },
    {
        "id": "ex-slash",
        "title": "Double slash inside the path",
        "tags": ["double_slash_path"],
        "source": "Local exhibit · Shape",
        "text": (
            "A path that contains a double slash can make later text look like a second address. "
            "The host that is named in the authority is still the host in the URL. "
            "This exhibit supports the double-slash indicator."
        ),
    },
    {
        "id": "ex-free-host",
        "title": "Page hosted on a free site platform",
        "tags": ["free_hosting"],
        "source": "Local exhibit · Host",
        "text": (
            "Free hosting and site-builder platforms such as web.app, firebaseapp.com, workers.dev, pages.dev, vercel.app, "
            "weeblysite.com, webflow.io, and IPFS gateways let anyone publish a page without registering a domain. "
            "The registrable domain then belongs to the platform, not to the person who made the page, so domain reputation says nothing about it. "
            "APWG and Interisle phishing reports list these platforms among the hosts most often used for credential pages. "
            "This exhibit supports the free-hosting indicator. Many ordinary projects use these platforms too, so it is one signal."
        ),
    },
    {
        "id": "ex-random-label",
        "title": "Machine-generated host label",
        "tags": ["random_label"],
        "source": "Local exhibit · Shape",
        "text": (
            "A host label with a long run of consonants, or a long mix of letters and digits, is rarely chosen by a person. "
            "Phishing kits often create such labels in bulk on free platforms or cheap suffixes. "
            "This workbench flags a label of at least eight characters with five or more consonants in a row, or with at least four digits mixed among letters. "
            "This exhibit supports the random-label indicator."
        ),
    },
    {
        "id": "ex-embedded-www",
        "title": "www or com glued inside a label",
        "tags": ["embedded_www"],
        "source": "Local exhibit · Host",
        "text": (
            "A label such as wwwofficelogin or a label ending in a glued com, as in examplecom.evil.dev, imitates the start or end of a real address. "
            "A real address separates www and com with dots. This exhibit supports the embedded-www indicator."
        ),
    },
    {
        "id": "ex-typosquat",
        "title": "Brand name with one character changed",
        "tags": ["brand_mismatch", "typosquat"],
        "source": "Local exhibit · Brand",
        "text": (
            "A typosquat changes, adds, drops, or swaps one character of a brand name, as in rakoten for rakuten or paypa1 for paypal. "
            "This workbench checks an edit distance of one against brand names of at least six letters. "
            "This exhibit supports the brand-mismatch indicator when the match is a typo rather than the exact name."
        ),
    },
    {
        "id": "ex-legitimacy",
        "title": "How to read a low score",
        "tags": ["legitimacy"],
        "source": "Local exhibit · Policy",
        "text": (
            "A low rule score means the weights did not reach the moderate band. That is a reason to keep the extra registries closed. "
            "It is not a certificate that the page is safe to trust with a secret. "
            "Open sensitive services from a bookmark or a typed official address when a page asks for them."
        ),
    },
    {
        "id": "ex-path",
        "title": "Which tool runs next",
        "tags": ["path_policy"],
        "source": "Local exhibit · Policy",
        "text": (
            "The next tool depends on the score. Below 21, the light path reads the low-score exhibit and still retrieves any indicator that fired. "
            "From 21 to 49, the standard path retrieves one exhibit per fired indicator. At 50 and above, the deep path also opens the brand registry "
            "and the suffix registry. A brand token or a listed suffix opens its registry even when the score is lower. "
            "Verification is a separate step. The report publishes a sentence only when an exhibit tag covers it."
        ),
    },
]

_BLOB = "|".join(f"{doc['id']}:{doc['title']}" for doc in DOCS)
VERSION = hashlib.sha256(_BLOB.encode()).hexdigest()[:12]
_BY_ID = {str(doc["id"]): doc for doc in DOCS}


def by_id(doc_id: str) -> dict[str, object] | None:
    return _BY_ID.get(doc_id)


def brand_name(key: str) -> str:
    return BRAND_DISPLAY.get(key, key.title())


def brand_rows() -> list[dict[str, str]]:
    rows = [
        {"name": brand_name(key), "domains": ", ".join(sorted(domains))}
        for key, domains in BRANDS.items()
    ]
    rows.sort(key=lambda row: row["name"])
    return rows


def tld_rows() -> list[dict[str, str]]:
    notes = {
        "tk": "Often given away, so new lookalike names are cheap.",
        "ml": "Often given away, so new lookalike names are cheap.",
        "ga": "Often given away, so new lookalike names are cheap.",
        "cf": "Often given away, so new lookalike names are cheap.",
        "gq": "Often given away, so new lookalike names are cheap.",
        "xyz": "Inexpensive generic suffix seen often on newly registered hosts.",
        "top": "Inexpensive generic suffix seen often on newly registered hosts.",
        "click": "The name itself is used as a lure to click.",
        "work": "Inexpensive generic suffix.",
        "fit": "Inexpensive generic suffix.",
        "buzz": "Inexpensive generic suffix.",
        "monster": "Inexpensive generic suffix.",
        "download": "The name invites a file download.",
        "country": "Inexpensive generic suffix.",
        "rest": "Inexpensive generic suffix.",
        "cam": "Inexpensive generic suffix.",
        "loan": "The name is a financial lure.",
        "men": "Inexpensive generic suffix.",
        "date": "Inexpensive generic suffix.",
        "racing": "Inexpensive generic suffix.",
        "stream": "The name invites a media or file action.",
        "science": "Inexpensive generic suffix.",
        "gdn": "Inexpensive generic suffix.",
        "support": "The name imitates a help desk.",
        "review": "Inexpensive generic suffix.",
        "pw": "Inexpensive country suffix marketed as generic.",
        "link": "The name itself is used as a lure to click.",
        "site": "Inexpensive generic suffix.",
        "online": "Inexpensive generic suffix.",
        "club": "Inexpensive generic suffix.",
        "icu": "Inexpensive generic suffix.",
        "cyou": "Inexpensive generic suffix.",
        "sbs": "Inexpensive generic suffix.",
        "cfd": "Inexpensive generic suffix.",
        "bond": "Inexpensive generic suffix.",
        "lat": "Inexpensive generic suffix.",
        "shop": "Inexpensive generic suffix with commerce lures.",
        "live": "Inexpensive generic suffix.",
        "vip": "Inexpensive generic suffix.",
        "biz": "Older generic suffix with a high abuse share.",
        "ss": "Country suffix seen on lookalike hosts such as brand.com.ss.",
    }
    return [{"tld": tld, "note": notes[tld]} for tld in sorted(SUSPICIOUS_TLDS)]


EXAMPLES = [
    {
        "url": "https://www.google.com",
        "mode": "agentic",
        "caption": "Ordinary official host. Expected low signal.",
        "group": "calm",
    },
    {
        "url": "https://www.paypal.com/signin",
        "mode": "agentic",
        "caption": "Listed PayPal domain. Account words stay lightly weighted.",
        "group": "calm",
    },
    {
        "url": "https://login.microsoftonline.com",
        "mode": "agentic",
        "caption": "Listed Microsoft host. A login label here is expected.",
        "group": "calm",
    },
    {
        "url": "http://paypa1-secure-login.tk/verify/account",
        "mode": "compare",
        "caption": "Classroom lookalike: digit swap, .tk, account words, explicit http.",
        "group": "compare",
    },
    {
        "url": "http://linkedin.com.evil.tk/login",
        "mode": "compare",
        "caption": "Brand word sits in a subdomain. The registrable domain is evil.tk.",
        "group": "compare",
    },
    {
        "url": "http://paypal.com@evil.example/login",
        "mode": "compare",
        "caption": "The host is the text after the @ sign. evil.example is documentation-style.",
        "group": "compare",
    },
    {
        "url": "http://192.0.2.10/banking/login",
        "mode": "agentic",
        "caption": "192.0.2.10 is TEST-NET documentation space. The app does not connect.",
        "group": "signal",
    },
    {
        "url": "https://bit.ly/3example",
        "mode": "agentic",
        "caption": "Shortener. The destination is not in the string, and the app does not follow it.",
        "group": "signal",
    },
    {
        "url": "https://amaz0n-billing.xyz/secure/update",
        "mode": "compare",
        "caption": "Digit swap plus a listed suffix and billing words.",
        "group": "compare",
    },
]
