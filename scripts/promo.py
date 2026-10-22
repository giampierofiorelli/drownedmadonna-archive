"""
Build site/confessions-promo.html: every news item about the promotion of
"Confessions on a Dance Floor" (September-December 2005) found in the archive,
exclusive or not, oldest first, with the summary text as archived.

Most of these stories survive only as summaries on front and category pages,
so the page shows that text in full and links to the archived listing it
comes from.
"""

import datetime as dt
import html
import os
import re
import urllib.parse

import exclusives as ex

START, END = dt.date(2005, 9, 20), dt.date(2005, 12, 31)
TOPIC = re.compile(
    r"G-A-Y|G\.A\.Y|KoKo|\bAOL\b|webcast|promo|Wetten|Parkinson|Star Academy|Children in Need|\bEMAs?\b|"
    r"Europe Music Awards|Lisbon|\bTV\b|TRL|Good Morning America|\bCNN\b|\bET\b|interview|Paris|"
    r"Tokyo|Japan|SMAP|gig|showcase|Top of the Pops|Jonathan Ross|screening|listening party", re.I)
# In the summary text only unambiguous promo terms count, so unrelated stories that
# merely mention an interview or a TV channel stay out.
STRONG = re.compile(
    r"G-A-Y|G\.A\.Y|KoKo|\bAOL\b|webcast|promo|Wetten|Parkinson|Star Academy|Children in Need|\bEMAs?\b|"
    r"Europe Music Awards|TRL|Good Morning America|listening party|screening", re.I)
JUNK = re.compile(r"Warning\s*:.*?on line \d+|\"?>\s*\d+\s*Note:.*$|\(\s*(Read More\.\.\.|comments\?).*$", re.S)


def story_blocks(text, captured):
    """Yield (sid, date, title, summary) for each story on a PHP-Nuke listing page."""
    for block in re.split(r'<table\s+width="100%"', text, flags=re.I):
        sids = re.findall(r"file=article(?:&amp;|&)sid=(\d+)", block)
        if not sids:
            continue
        flat = ex.clean(block)
        m = ex.NUKE_BLOCK_DATE.search(flat)
        if m:
            weekday, month, day, title = m.groups()
            date = ex.infer_year(weekday, month, int(day), captured) if captured else None
            summary = flat[:m.start()]
        else:
            head = ex.NUKE_TITLE_CELL.search(block)
            full = ex.NUKE_FULL_DATE.search(flat)
            if not head or not full:
                continue
            title = ex.clean(head.group(1))
            date = ex.safe_date(*full.groups())
            body = re.search(r'class="?storytext"?[^>]*>(.*?)</font>\s*</div>', block, re.I | re.S)
            summary = ex.clean(body.group(1)) if body else ""
        summary = JUNK.sub("", re.sub(r"^.*?cellpadding=\"5\">", "", summary)).strip(' ">')
        yield int(sids[0]), date, title.strip().rstrip("."), summary


def build(out_dir, era_pages):
    stories = {}
    for era, pages in era_pages.items():
        captured_on = ex.plan_dates(era)
        for key, (rel, original, mime) in pages.items():
            if "file=article" in original or not rel.lower().endswith((".html", ".htm", ".php")):
                continue
            raw = open(os.path.join(ex.MIRROR, era, "files", rel), "rb").read()
            if b"Written by" not in raw:
                continue
            text = raw.decode("cp1252", "replace")
            for sid, date, title, summary in story_blocks(text, captured_on.get(key)):
                if not date or not (START <= date <= END):
                    continue
                if not TOPIC.search(title) and not STRONG.search(summary[:800]):
                    continue
                if ex.is_french(title):
                    continue
                prev = stories.get(sid)
                if not prev or len(summary) > len(prev[2]):
                    stories[sid] = (date, title, summary, f"{era}/{rel}")
    items = sorted(stories.items(), key=lambda kv: (kv[1][0], kv[0]))
    write_page(out_dir, items)
    return len(items)


def write_page(out_dir, items):
    rows = []
    for sid, (date, title, summary, where) in items:
        words = re.sub(r"^\W*(world )?exclusive( preview)?\W*|^scoop\W*", "", title, flags=re.I).split()[:6]
        href = html.escape(urllib.parse.quote(where, safe="/._-,=~"))
        frag = "#:~:text=" + urllib.parse.quote(" ".join(words), safe="") if words else ""
        text = html.escape(summary) if summary else "<em>Only the title survives.</em>"
        rows.append(
            f'<article><p class="d">{date.day} {date.strftime("%b %Y")}</p>'
            f"<h2>{html.escape(title)}</h2><p>{text}</p>"
            f'<p class="src"><a href="{href}{frag}">Archived page</a></p></article>\n')
    page = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Confessions promo news</title>
<style>
:root{{--fg:#1d1d1f;--muted:#6e6e73;--line:#e5e5ea;--bg:#fff;--link:#a3123a}}
@media (prefers-color-scheme: dark){{:root{{--fg:#f5f5f7;--muted:#a1a1a6;--line:#38383a;--bg:#111;--link:#ff6b8b}}}}
body{{font:16px/1.6 system-ui,sans-serif;margin:0;padding:24px 16px;background:var(--bg);color:var(--fg)}}
main{{max-width:760px;margin:0 auto}}
h1{{font:400 2rem/1.2 Georgia,serif;margin:.2em 0}}
h2{{font:600 1.1rem/1.35 system-ui,sans-serif;margin:.2em 0 .4em}}
article{{border-top:1px solid var(--line);padding:18px 0}}
.d,.src,.lede{{color:var(--muted);font-size:14px;margin:0}}
a{{color:var(--link)}}
</style>
<main>
<p><a href="index.html">All eras</a> · <a href="exclusives.html">Exclusives</a></p>
<h1>Confessions promo news</h1>
<p class="lede">{len(items)} news items from September to December 2005 on the promotion of "Confessions on a Dance Floor", oldest first. Most full articles were never archived: the text below is the summary as it appeared on the site's front and category pages.</p>
{''.join(rows)}
</main>"""
    with open(os.path.join(out_dir, "confessions-promo.html"), "w", encoding="utf-8") as f:
        f.write(page)
