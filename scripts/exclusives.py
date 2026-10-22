"""
Build site/exclusives.html: every DrownedMadonna exclusive found in the archive,
in chronological order.

An article counts as an exclusive when
  - an archived "Exclusive" listing lists it (PHP-Nuke category 2, the K2 tag
    "Exclusive", the WordPress category "exclusive"), or
  - its archived WordPress page is filed under the "exclusive" category, or
  - its title or URL slug starts with "exclusive" (the site's own convention).
Articles that only mention "exclusive" elsewhere in the title or slug are listed
separately for review instead of being dropped.

Sources are the downloaded files (mirror/) and, for eras not downloaded yet,
the Wayback inventory (inventory/urls.csv), so the page grows as downloads finish.
"""

import csv
import datetime as dt
import html
import os
import re
import urllib.parse

from urlkeys import site_host

MIRROR = "mirror"
INVENTORY = os.path.join("inventory", "urls.csv")

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}
WP_DATED = re.compile(r"^/(\d{4})/(\d{2})/(\d{2})/([a-z0-9][a-z0-9_%-]*)/?(?:\d{8}/?)?$", re.I)
WP_SLUG_DATE = re.compile(r"^/([a-z0-9][a-z0-9_%-]{8,})/(\d{4})(\d{2})(\d{2})/?$", re.I)
K2_ITEM = re.compile(r"^/(?:index\.php/)?component/k2/item/(\d+)(?:-([^/.]+))?(?:\.html)?/?$", re.I)
ANCHOR = re.compile(r"<a\b[^>]*\bhref\s*=\s*[\"']?([^\"'\s>]+)[^>]*>(.*?)</a>", re.I | re.S)
TAG = re.compile(r"<[^>]+>")
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
NUKE_BLOCK_DATE = re.compile(
    r"Written by .*? on (\w+day), (\w+) (\d{1,2}) @ [\d:]+ \w+ (.*?)\s*\[\d+ reads\]", re.I | re.S)
NUKE_TITLE_CELL = re.compile(r"<font class=\"?testo_notizia\"?[^>]*>(.*?)</font>\s*</td>", re.I | re.S)
NUKE_FULL_DATE = re.compile(r"Written by .*? on (\d{4})-(\d{2})-(\d{2}) \d", re.I | re.S)
NOISE_ANCHORS = re.compile(r"^(read more|comments?|\d+ comments?|more|continue reading|permalink)\b", re.I)


def clean(text):
    text = html.unescape(TAG.sub(" ", text))
    return re.sub(r"\s+", " ", text).strip()


def safe_date(y, mo, d):
    try:
        return dt.date(int(y), int(mo), int(d))
    except ValueError:
        return None


def article_id(url, base=None):
    """Identify an article URL: returns (id, date, slug) or None."""
    url = html.unescape(url).replace("&amp;", "&")
    if base:
        url = urllib.parse.urljoin(base, url)
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not site_host(parts.hostname):
        return None
    path = urllib.parse.unquote(parts.path)
    q = dict(urllib.parse.parse_qsl(parts.query))
    if path.endswith("modules.php") and q.get("file") == "article" and q.get("sid", "").isdigit():
        return (f"nuke:{int(q['sid'])}", None, None)
    m = K2_ITEM.match(path)
    if m:
        return (f"k2:{int(m.group(1))}", None, m.group(2))
    m = WP_DATED.match(path)
    if m:
        y, mo, d, slug = m.groups()
        return (f"wp:{slug.lower()}", safe_date(y, mo, d), slug)
    m = WP_SLUG_DATE.match(path)
    if m:
        slug, y, mo, d = m.groups()
        return (f"wp:{slug.lower()}", safe_date(y, mo, d), slug)
    return None


def infer_year(weekday, month, day, captured):
    """Latest date <= capture date on which month/day fell on the given weekday."""
    if weekday.lower() not in WEEKDAYS:
        return None
    wd = WEEKDAYS.index(weekday.lower())
    mo = MONTHS.get(month.lower())
    if not mo:
        return None
    for year in range(captured.year, captured.year - 12, -1):
        d = safe_date(year, mo, day)
        if d and d <= captured and d.weekday() == wd:
            return d
    return None


def slug_title(slug):
    words = urllib.parse.unquote(slug or "").replace("_", "-").split("-")
    text = " ".join(w for w in words if w)
    return text[:1].upper() + text[1:]


def site_title(raw):
    """Strip the site name the old themes put around article titles."""
    t = clean(raw)
    prefix = re.compile(r"^.*?(Drowned ?Madonna|Putting (the )?news first)[^-]*-\s*", re.I)
    while prefix.match(t):  # titles can stack several site prefixes
        t = prefix.sub("", t, count=1)
    t = re.sub(r"\s*[|–-]\s*Drowned ?Madonna.*$", "", t, flags=re.I)
    return t.strip()


def starts_exclusive(text):
    return bool(re.match(r"^\W*exclusive\b", text or "", re.I))


def mentions_exclusive(text):
    return bool(re.search(r"exclusiv", text or "", re.I))


class Article:
    def __init__(self, aid):
        self.id = aid
        self.title = ""
        self.title_strong = False
        self.date = None
        self.date_exact = False
        self.first_seen = None
        self.exclusive = False
        self.mention = False
        self.local = None      # path relative to the site root
        self.listing = None    # archived listing page that shows its summary
        self.wayback = None
        self.slug = None

    def note_title(self, title, strong=False):
        title = (title or "").strip()
        if not title or NOISE_ANCHORS.match(title):
            return
        if strong or not (self.title_strong or self.title):
            self.title, self.title_strong = title, self.title_strong or strong

    def note_date(self, date, exact):
        if not date:
            return
        if exact and not self.date_exact:
            self.date, self.date_exact = date, True
        elif not self.date:
            self.date, self.date_exact = date, exact


def is_listing(path, query):
    p = path.lower()
    if "/category/exclusive" in p or "/tag/exclusive" in p:
        return True
    return p.endswith("modules.php") and query.get("file") == "categories" and query.get("catid") == "2"


def is_nuke_page(path):
    """Front page or modules.php page of the PHP-Nuke years."""
    p = path.lower()
    return p in ("/", "/index.php") or p.endswith("modules.php")


def plan_dates(era):
    with open(os.path.join(MIRROR, era, "_plan.csv"), encoding="utf-8") as f:
        return {r["key"]: safe_date(r["timestamp"][:4], r["timestamp"][4:6], r["timestamp"][6:8])
                for r in csv.DictReader(f)}


def read_nuke_listing(text, captured, get, listing_path, only_exclusive=False):
    """PHP-Nuke listing page: each story block has a sid link and a 'Written by ... on' line.

    On the Exclusive category page every story is an exclusive; on front pages
    and other listings (only_exclusive) just the stories titled "Exclusive...".
    """
    for block in re.split(r"<table\s+width=\"100%\"", text, flags=re.I):
        sids = re.findall(r"file=article(?:&amp;|&)sid=(\d+)", block)
        if not sids:
            continue
        flat = clean(block)
        date, tagged = None, False
        m = NUKE_BLOCK_DATE.search(flat)
        if m:
            # 2003-2005 theme: "Written by X on Friday, May 27 @ 19:01:08 CEST Title [N reads]"
            weekday, month, day, title = m.groups()
            if captured:
                date = infer_year(weekday, month, int(day), captured)
        else:
            # Late-2005 theme: title in its own cell, "[EXCLUSIVE]" linked to category 2,
            # and "Written by X on 2005-09-13 23:23:07 ..." with the full date.
            head = NUKE_TITLE_CELL.search(block)
            full = NUKE_FULL_DATE.search(flat)
            if not head or not full:
                continue
            title = clean(head.group(1))
            # Every category badge shares one style; what marks an exclusive is
            # the Exclusive category link or a badge reading "... EXCLUSIVE".
            badge = re.match(r"^\[\s*([^\]]+?)\s*\]", title)
            tagged = bool(re.search(r"catid=2[\"&'\s>]", head.group(1))) or \
                bool(badge and re.search(r"exclusive", badge.group(1), re.I))
            date = safe_date(*full.groups())
        if only_exclusive and not (tagged or starts_exclusive(title)):
            continue
        title = re.sub(r"^\[\s*([^\]]*exclusive[^\]]*?)\s*\]\s*", lambda m: m.group(1).upper() + ": ",
                       title.strip(), flags=re.I).rstrip(".")
        a = get(f"nuke:{int(sids[0])}")
        a.exclusive = True
        a.listing = a.listing or listing_path
        a.note_title(title, strong=True)
        a.note_date(date, exact=True)


def build(out_dir, era_pages, config_eras):
    """era_pages: {era: {key: (rel, original, mime)}} for downloaded files."""
    articles = {}

    def get(aid):
        return articles.setdefault(aid, Article(aid))

    # 1. Inventory: every archived article URL, with its first capture.
    with open(INVENTORY, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["category"] != "page":
                continue
            ident = article_id(row["original"])
            if not ident:
                continue
            aid, date, slug = ident
            a = get(aid)
            ts = row["timestamp"]
            seen = safe_date(ts[:4], ts[4:6], ts[6:8])
            if seen and (not a.first_seen or seen < a.first_seen):
                a.first_seen = seen
                a.wayback = f"https://web.archive.org/web/{ts}/{row['original']}"
            a.note_date(date, exact=True)
            a.slug = a.slug or slug
            if starts_exclusive(slug):
                a.exclusive = True
            elif mentions_exclusive(slug):
                a.mention = True

    # 2. Downloaded files: article pages and exclusive listings.
    for era, pages in era_pages.items():
        captured_on = plan_dates(era)
        for key, (rel, original, mime) in pages.items():
            if "html" not in mime and not rel.lower().endswith((".html", ".htm", ".php")):
                continue
            try:
                raw = open(os.path.join(MIRROR, era, "files", rel), "rb").read()
            except OSError:
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = raw.decode("cp1252", "replace")  # the old PHP-Nuke and Joomla pages
            ident = article_id(original)
            if ident:
                aid, date, slug = ident
                a = get(aid)
                a.local = a.local or f"{era}/{rel}"
                a.slug = a.slug or slug
                t = TITLE.search(text)
                if t:
                    a.note_title(site_title(t.group(1)), strong=True)
                a.note_date(date, exact=True)
                if re.search(r"\bcategory-exclusive\b", text, re.I):
                    a.exclusive = True
                continue
            parts = urllib.parse.urlsplit(original.replace("&amp;", "&"))
            query = dict(urllib.parse.parse_qsl(parts.query))
            path = urllib.parse.unquote(parts.path) or "/"
            listed = is_listing(path, query)
            if era.startswith("snapshots") or is_nuke_page(path):
                # Front pages and news listings keep the titles and summaries of
                # stories never archived on their own; the Exclusive category
                # lists only exclusives, other pages are filtered by title/tag.
                read_nuke_listing(text, captured_on.get(key), get, f"{era}/{rel}", only_exclusive=not listed)
                continue
            if not listed:
                continue
            for href, label in ANCHOR.findall(text):
                ident = article_id(href, original)
                if ident:
                    a = get(ident[0])
                    a.exclusive = True
                    a.note_date(ident[1], exact=True)
                    a.note_title(clean(label))

    # 3. Classify and order.
    chosen, review = [], []
    for a in articles.values():
        if not a.title:
            a.title = slug_title(a.slug) or a.id
        if starts_exclusive(a.title):
            a.exclusive = True
        elif mentions_exclusive(a.title):
            a.mention = True
        if not (a.exclusive or a.mention):
            continue
        if not a.date and a.first_seen:
            a.date, a.date_exact = a.first_seen, False
        (chosen if a.exclusive else review).append(a)

    order = lambda a: (a.date or dt.date(1900, 1, 1), a.id)
    chosen.sort(key=order)
    review.sort(key=order)
    write_page(out_dir, chosen, review, config_eras)
    return len(chosen), len(review)


def fmt_date(a):
    if not a.date:
        return "Undated"
    if a.date_exact:
        return f"{a.date.day} {a.date.strftime('%b %Y')}"
    return "c. " + a.date.strftime("%b %Y")


def era_label(a, config_eras):
    if a.local:
        return a.local.split("/", 1)[0]
    year = (a.date or a.first_seen or dt.date(1900, 1, 1)).year
    for era in config_eras:
        if int(str(era["capture_from"])[:4]) <= year <= int(str(era["capture_to"])[:4]):
            return era["era"]
    return ""


def fallback_wayback(a):
    """Wayback search link for articles known only from a listing page."""
    year = (a.date or dt.date(2005, 1, 1)).year
    if a.id.startswith("nuke:"):
        url = f"http://www.drownedmadonna.com/modules.php?name=News&file=article&sid={a.id[5:]}"
    elif a.id.startswith("k2:"):
        url = f"http://www.drownedmadonna.com/component/k2/item/{a.id[3:]}"
    elif a.slug and a.date:
        url = f"https://www.drownedmadonna.com/{a.date:%Y/%m/%d}/{a.slug}/"
    else:
        return "#"
    return f"https://web.archive.org/web/{year}/{url}"


def row_html(a, config_eras):
    if a.local:
        href, where = urllib.parse.quote(a.local, safe="/._-,=~"), "Archive copy"
    elif a.wayback:
        href, where = a.wayback, "Wayback Machine"
    elif a.listing:
        # The article itself was never archived: open the category page that
        # shows its summary, scrolled to it with a text fragment.
        words = re.sub(r"^\W*exclusive\W*", "", a.title, flags=re.I).split()[:6]
        fragment = urllib.parse.quote(" ".join(words), safe="")
        href = urllib.parse.quote(a.listing, safe="/._-,=~") + (f"#:~:text={fragment}" if words else "")
        where = "Summary only"
    else:
        href, where = fallback_wayback(a), "Wayback search"
    return (f'<tr><td class="d">{html.escape(fmt_date(a))}</td>'
            f'<td><a href="{html.escape(href)}">{html.escape(a.title)}</a></td>'
            f'<td class="e">{html.escape(era_label(a, config_eras))}</td><td class="e">{where}</td></tr>')


def write_page(out_dir, chosen, review, config_eras):
    local = sum(1 for a in chosen if a.local)
    summary = sum(1 for a in chosen if not a.local and not a.wayback and a.listing)
    rows = "\n".join(row_html(a, config_eras) for a in chosen)
    review_rows = "\n".join(row_html(a, config_eras) for a in review)
    page = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>DrownedMadonna exclusives</title>
<style>
:root{{--fg:#1d1d1f;--muted:#6e6e73;--line:#e5e5ea;--bg:#fff;--link:#a3123a}}
@media (prefers-color-scheme: dark){{:root{{--fg:#f5f5f7;--muted:#a1a1a6;--line:#38383a;--bg:#111;--link:#ff6b8b}}}}
body{{font:15px/1.5 system-ui,sans-serif;margin:0;padding:24px 16px;background:var(--bg);color:var(--fg)}}
main{{max-width:960px;margin:0 auto}}
h1{{font:400 2rem/1.2 Georgia,serif;margin:.2em 0}}
h2{{font:400 1.4rem/1.2 Georgia,serif;margin-top:2em}}
p{{color:var(--muted);max-width:44rem}}
a{{color:var(--link)}}
table{{width:100%;border-collapse:collapse;margin:16px 0 24px}}
th,td{{text-align:left;padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-weight:500;color:var(--muted);font-size:13px}}
td.d{{white-space:nowrap;font-variant-numeric:tabular-nums}}
td.e{{color:var(--muted);font-size:13px;white-space:nowrap}}
@media (max-width:640px){{td.e,th.e{{display:none}}}}
</style>
<main>
<p><a href="index.html">All eras</a></p>
<h1>DrownedMadonna exclusives</h1>
<p>{len(chosen)} exclusives found so far, oldest first. {local} open the recovered copy. {summary} were never archived as full articles: they open the recovered Exclusive category page, at their title and summary. The others open on the Wayback Machine until their era finishes downloading. A date marked "c." is when the page was first archived, not its publication date.</p>
<table><thead><tr><th>Date</th><th>Title</th><th class="e">Era</th><th class="e">Opens</th></tr></thead>
<tbody>
{rows}
</tbody></table>
<h2>To review</h2>
<p>{len(review)} articles mention "exclusive" in the title or address but are not filed as exclusives: some may be other outlets' exclusives.</p>
<table><thead><tr><th>Date</th><th>Title</th><th class="e">Era</th><th class="e">Opens</th></tr></thead>
<tbody>
{review_rows}
</tbody></table>
</main>"""
    with open(os.path.join(out_dir, "exclusives.html"), "w", encoding="utf-8") as f:
        f.write(page)
