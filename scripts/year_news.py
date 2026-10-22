"""
Build site/news-<year>.html: every English news story of a given year found
anywhere in the archive (article pages, front pages, topic and category
listings), oldest first, with the full text as archived.

A story seen in several places is listed once, keeping its longest text
(usually the article page itself; otherwise the listing summary).
"""

import html
import os
import re
import urllib.parse

import exclusives as ex
import promo

STORY_TABLE = re.compile(r"<table\s+width=\"100%\"\s+border=\"0\"\s+bgcolor=\"#FFFFFF\"[^>]*>(.*?)</table>", re.I | re.S)
TITLE_CELL = re.compile(r"<td[^>]*>(.*?)</td>", re.I | re.S)
TOPIC_LINK = re.compile(r"<a[^>]+new_topic=\d+[^>]*>(.*?)</a>", re.I | re.S)
BADGE = re.compile(r"\[\s*<a[^>]+catid=(\d+)[^>]*>(.*?)</a>\s*\]", re.I | re.S)
BODY = re.compile(r"<font class=\"?storytext\"?[^>]*>(.*?)</font>\s*</div>", re.I | re.S)
BYLINE = re.compile(
    r"(?:Written by|Article published by|Articolo pubblicato da|Scritto da|Publi[ée] par|Enviado por)\s*"
    r"(?:<a[^>]*>)?\s*([^<\s][^<]*?)\s*(?:</a>)?\s+(?:on|il|le|el)\s+(\d{4})-(\d{2})-(\d{2})\s+([\d:]{8})",
    re.I)
SID = re.compile(r"file=article(?:&amp;|&)sid=(\d+)", re.I)
BLOCK_TAGS = re.compile(r"<\s*(?:br|/p|p|/div|div|li|/tr)\b[^>]*>", re.I)

# Common words used to tell the English edition from the French and Italian ones.
EN = {"the", "and", "of", "to", "is", "with", "for", "her", "she", "this", "that", "on", "will", "has", "was", "are", "by"}
FR = {"le", "la", "les", "des", "est", "et", "du", "une", "dans", "sur", "pour", "avec", "qui", "au", "aux", "sa", "son",
      "par", "de", "d'", "hier", "français", "française", "allemagne", "n'est", "pas", "elle"}
IT = {"il", "di", "che", "è", "per", "della", "del", "sono", "una", "gli", "nel", "alla", "anche", "sulla", "dal", "ha"}
ES = {"el", "los", "las", "sobre", "para", "por", "más", "ningún", "ahora", "y", "con", "nominación", "evento", "promocional"}
NON_LATIN = re.compile(r"[\u0400-\u04ff\u3000-\u9fff\uac00-\ud7af]")


def language(text):
    if NON_LATIN.search(text):
        return "other"
    words = re.findall(r"[a-zà-ÿñ]+'?", text.lower())
    words += [w + "'" for w in re.findall(r"\b([a-z])'", text.lower())]
    scores = {k: sum(1 for w in words if w in s) for k, s in (("en", EN), ("fr", FR), ("it", IT), ("es", ES))}
    best = max(scores, key=scores.get)
    return "en" if not any(scores.values()) or scores["en"] == scores[best] else best


def paragraphs(fragment):
    """Story HTML -> list of plain-text paragraphs."""
    text = BLOCK_TAGS.sub("\n", fragment)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    out = []
    for line in text.split("\n"):
        line = re.sub(r"[ \t\xa0]+", " ", line).strip()
        if line:
            out.append(line)
    return out


def stories_dated(text, page_sid=None):
    """Stories in the 2006-2007 theme: title cell, storytext body, dated byline."""
    for m in STORY_TABLE.finditer(text):
        block = m.group(1)
        by = BYLINE.search(block)
        cell = TITLE_CELL.search(block)
        if not by or not cell:
            continue
        head = cell.group(1)
        topic = TOPIC_LINK.search(head)
        badge = BADGE.search(head)
        title_html = BADGE.sub("", TOPIC_LINK.sub("", head, count=1), count=1)
        body = BODY.search(block)
        sids = SID.findall(block)
        yield {
            "sid": int(sids[0]) if sids else page_sid,
            "date": ex.safe_date(by.group(2), by.group(3), by.group(4)),
            "time": by.group(5), "author": by.group(1).strip(),
            "topic": ex.clean(topic.group(1)) if topic else "",
            "badge": ex.clean(badge.group(2)) if badge else "",
            "title": ex.clean(title_html).strip(" []"),
            "paras": paragraphs(body.group(1)) if body else [],
        }


def build(out_dir, era_pages, year):
    stories = {}

    def keep(st, where):
        if not st["date"] or st["date"].year != year or not st["title"]:
            return
        text = " ".join(st["paras"])
        title_words = set(re.findall(r"[a-zàèéìòù']+", st["title"].lower()))
        # The title decides; the body only vetoes when it has little English in it
        # (some English stories quote a French or Italian source at length).
        body_en = sum(1 for w in re.findall(r"[a-z]+", text.lower()) if w in EN)
        if (language(st["title"]) != "en" or ex.is_french(st["title"])
                or title_words & (ex.ITALIAN_HINTS | {"dalla", "già", "nelle", "regno"})
                or (language(st["title"] + " " + text) != "en" and body_en < 10)):
            return
        key = st["sid"] or st["title"].lower()
        prev = stories.get(key)
        if not prev or len(text) > len(" ".join(prev["paras"])):
            st["where"] = where
            stories[key] = st

    for era, pages in era_pages.items():
        captured_on = ex.plan_dates(era)
        for key, (rel, original, mime) in pages.items():
            if not rel.lower().endswith((".html", ".htm", ".php")):
                continue
            raw = open(os.path.join(ex.MIRROR, era, "files", rel), "rb").read()
            if str(year).encode() not in raw and b"reads]" not in raw:
                continue
            text = raw.decode("cp1252", "replace")
            m = re.search(r"sid=(\d+)", original)
            page_sid = int(m.group(1)) if m and "file=article" in original else None
            where = f"{era}/{rel}"
            for st in stories_dated(text, page_sid):
                keep(st, where)
            # Older theme: "Written by X on Weekday, Month Day" listings.
            if b"reads]" in raw and "file=article" not in original:
                for sid, date, title, summary in promo.story_blocks(text, captured_on.get(key)):
                    keep({"sid": sid, "date": date, "time": "", "author": "", "topic": "", "badge": "",
                          "title": title, "paras": [summary] if summary else []}, where)

    items = sorted(stories.values(), key=lambda s: (s["date"], s["time"], s["sid"] or 0))
    write_page(out_dir, items, year)
    return len(items)


def write_page(out_dir, items, year):
    rows, month = [], None
    for st in items:
        if st["date"].month != month:
            month = st["date"].month
            rows.append(f'<h2 class="m">{st["date"].strftime("%B %Y")}</h2>\n')
        meta = " · ".join(x for x in (st["topic"], st["badge"] and f'[{st["badge"]}]', st["author"]) if x)
        body = "".join(f"<p>{html.escape(p)}</p>" for p in st["paras"]) or "<p><em>Only the title survives.</em></p>"
        href = html.escape(urllib.parse.quote(st["where"], safe="/._-,=~"))
        rows.append(
            f'<article><p class="d">{st["date"].day} {st["date"].strftime("%b %Y")}'
            f'{" · " + html.escape(meta) if meta else ""}</p>'
            f'<h3>{html.escape(st["title"])}</h3>{body}'
            f'<p class="src"><a href="{href}">Archived page</a></p></article>\n')
    page = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{year} news</title>
<style>
:root{{--fg:#1d1d1f;--muted:#6e6e73;--line:#e5e5ea;--bg:#fff;--link:#a3123a}}
@media (prefers-color-scheme: dark){{:root{{--fg:#f5f5f7;--muted:#a1a1a6;--line:#38383a;--bg:#111;--link:#ff6b8b}}}}
body{{font:16px/1.6 system-ui,sans-serif;margin:0;padding:24px 16px;background:var(--bg);color:var(--fg)}}
main{{max-width:760px;margin:0 auto}}
h1{{font:400 2rem/1.2 Georgia,serif;margin:.2em 0}}
h2.m{{font:400 1.5rem/1.2 Georgia,serif;margin:1.6em 0 .2em}}
h3{{font:600 1.1rem/1.35 system-ui,sans-serif;margin:.2em 0 .4em}}
article{{border-top:1px solid var(--line);padding:18px 0}}
article p{{margin:.4em 0}}
.d,.src,.lede{{color:var(--muted);font-size:14px;margin:0}}
a{{color:var(--link)}}
</style>
<main>
<p><a href="index.html">All eras</a> · <a href="exclusives.html">Exclusives</a></p>
<h1>{year} news</h1>
<p class="lede">{len(items)} English news stories from {year} found in the archive, oldest first. Where the article page was archived the full text is shown; otherwise the summary from the front, topic or category page.</p>
{''.join(rows)}
</main>"""
    with open(os.path.join(out_dir, f"news-{year}.html"), "w", encoding="utf-8") as f:
        f.write(page)
