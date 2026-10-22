#!/usr/bin/env python3
"""
Turn the downloaded Wayback files into a browsable static site in ./site.

For every era folder in mirror/:
  - copy each downloaded file to site/<era>/...;
  - in HTML and CSS, rewrite links that point to drownedmadonna.com so they lead
    to the local copy; links to pages not (yet) downloaded go to the Wayback
    Machine instead, so navigation never dead-ends;
  - write site/<era>/index-of-pages.html listing every page with its title.
A top-level site/index.html links to each era.
"""

import csv
import html
import os
import posixpath
import re
import shutil
import urllib.parse

import json

import exclusives
from urlkeys import normalize, site_host

MIRROR = "mirror"
OUT = "site"
ATTR_RE = re.compile(r"""(?P<attr>\b(?:href|src|background|action|lowsrc|data)\s*=\s*)"""
                     r"""(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)'|(?P<bare>[^\s>"']+))""", re.I)
REFRESH_RE = re.compile(r"""(content\s*=\s*["']\s*\d+\s*;\s*url\s*=\s*)([^"'>\s]+)""", re.I)
CSS_URL_RE = re.compile(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""", re.I)
TITLE_RE = re.compile(rb"<title[^>]*>(.*?)</title>", re.I | re.S)
SKIP_SCHEMES = ("mailto:", "javascript:", "data:", "#", "about:", "tel:")
# Hosting cannot send X-Robots-Tag headers, so every archived page gets a noindex tag.
NOINDEX_TAG = '<meta name="robots" content="noindex, nofollow">'
NOINDEX_RE = re.compile(r"<head[^>]*>", re.I)


def load_era(era):
    """Map normalized URL key -> (local path relative to era root, original URL, mimetype)."""
    base = os.path.join(MIRROR, era)
    mimes = {}
    plan_path = os.path.join(base, "_plan.csv")
    if os.path.exists(plan_path):
        with open(plan_path, encoding="utf-8") as f:
            mimes = {r["key"]: r["mimetype"] for r in csv.DictReader(f)}
    pages = {}
    with open(os.path.join(base, "_manifest.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["status"] == "200" and r["file"] and os.path.exists(r["file"]):
                rel = os.path.relpath(r["file"], os.path.join(base, "files"))
                pages[r["key"]] = (rel.replace(os.sep, "/"), r["original"], mimes.get(r["key"], ""))
    return pages


def era_year(era):
    """Last year of the era label (e.g. '2002-2005-phpnuke' -> '2005') for Wayback fallbacks."""
    found = re.findall(r"(?:19|20)\d{2}", era)
    return found[-1] if found else "2005"


ALL_PAGES = {}  # normalized key -> (era, rel) across every downloaded era


def make_rewriter(pages, page_rel, page_url, year, era):
    """Return a function mapping a raw link value to its rewritten value."""
    here = posixpath.dirname(page_rel)

    def rewrite(value):
        raw = html.unescape(value.strip())
        if not raw or raw.lower().startswith(SKIP_SCHEMES):
            return value
        absolute = urllib.parse.urljoin(page_url, raw)
        parts = urllib.parse.urlsplit(absolute)
        if parts.scheme not in ("http", "https") or not site_host(parts.hostname):
            return value  # external link, leave untouched
        key = normalize(urllib.parse.urlunsplit(parts._replace(fragment="")))
        frag = "#" + parts.fragment if parts.fragment else ""
        target = pages.get(key) or pages.get(key.rstrip("/")) or pages.get(key + "/")
        if target:
            rel = posixpath.relpath(target[0], here or ".")
            return urllib.parse.quote(rel, safe="/._-,=~") + frag
        # The same file may have been archived in a later (or earlier) era:
        # an image a 2005 page shows is often only captured in 2007.
        other = ALL_PAGES.get(key) or ALL_PAGES.get(key.rstrip("/")) or ALL_PAGES.get(key + "/")
        if other:
            rel = posixpath.relpath(f"{other[0]}/{other[1]}", posixpath.join(era, here) or ".")
            return urllib.parse.quote(rel, safe="/._-,=~") + frag
        return f"https://web.archive.org/web/{year}/{absolute}"

    return rewrite


def rewrite_html(text, rewrite):
    def attr(m):
        val = m.group("dq") if m.group("dq") is not None else (
            m.group("sq") if m.group("sq") is not None else m.group("bare"))
        return f'{m.group("attr")}"{rewrite(val)}"'

    text = ATTR_RE.sub(attr, text)
    text = REFRESH_RE.sub(lambda m: m.group(1) + rewrite(m.group(2)), text)
    text = CSS_URL_RE.sub(lambda m: f"url({m.group(1)}{rewrite(m.group(2))}{m.group(1)})", text)
    return text


def is_html(rel, mime):
    return "html" in mime or rel.lower().endswith((".html", ".htm", ".php", ".asp", ".shtml"))


def build_era(era):
    pages = load_era(era)
    year = era_year(era)
    src_root = os.path.join(MIRROR, era, "files")
    dst_root = os.path.join(OUT, era)
    listing = []

    for key, (rel, original, mime) in pages.items():
        src = os.path.join(src_root, rel)
        dst = os.path.join(dst_root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if is_html(rel, mime) or rel.lower().endswith(".css") or "css" in mime:
            data = open(src, "rb").read()
            text = data.decode("latin-1")  # byte-preserving round trip
            rewrite = make_rewriter(pages, rel, original, year, era)
            if rel.lower().endswith(".css") or "css" in mime:
                text = CSS_URL_RE.sub(lambda m: f"url({m.group(1)}{rewrite(m.group(2))}{m.group(1)})", text)
            else:
                text = rewrite_html(text, rewrite)
                text = NOINDEX_RE.sub(lambda m: m.group(0) + NOINDEX_TAG, text, count=1) \
                    if NOINDEX_RE.search(text) else NOINDEX_TAG + text
                t = TITLE_RE.search(data)
                title = re.sub(r"\s+", " ", t.group(1).decode("latin-1")).strip() if t else ""
                listing.append((rel, title or rel, original))
            with open(dst, "wb") as f:
                f.write(text.encode("latin-1"))
        else:
            shutil.copyfile(src, dst)

    listing.sort(key=lambda x: x[0].lower())
    rows = "\n".join(
        f'<li><a href="{urllib.parse.quote(r, safe="/._-,=~")}">{html.escape(t)}</a>'
        f' <small>{html.escape(o)}</small></li>' for r, t, o in listing)
    with open(os.path.join(dst_root, "index-of-pages.html"), "w", encoding="utf-8") as f:
        f.write(f"""<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">
<title>{html.escape(era)} - archived pages</title>
<style>body{{font:15px/1.5 system-ui,sans-serif;margin:24px;max-width:900px}}small{{color:#777}}li{{margin:4px 0}}</style>
<p><a href="../index.html">All eras</a></p>
<h1>{html.escape(era)}</h1><p>{len(listing)} pages, {len(pages)} files in total.</p><ol>{rows}</ol>""")
    return len(listing), len(pages), pages


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    eras = sorted(d for d in os.listdir(MIRROR)
                  if os.path.exists(os.path.join(MIRROR, d, "_manifest.csv")))
    items = []
    era_pages = {}
    for era in eras:
        for key, (rel, _, _) in load_era(era).items():
            ALL_PAGES.setdefault(key, (era, rel))
    for era in eras:
        n_pages, n_files, era_pages[era] = build_era(era)
        items.append(f'<li><a href="{era}/index-of-pages.html">{era}</a> '
                     f'<small>{n_pages} pages, {n_files} files</small></li>')
        print(f"{era}: {n_pages} pages, {n_files} files")
    with open(os.path.join("config", "download.json"), encoding="utf-8") as f:
        config_eras = json.load(f)["eras"]
    n_excl, n_review = exclusives.build(OUT, era_pages, config_eras)
    print(f"exclusives: {n_excl} listed, {n_review} to review")
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(f"""<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">
<title>DrownedMadonna archive</title>
<style>body{{font:15px/1.5 system-ui,sans-serif;margin:24px;max-width:900px}}small{{color:#777}}</style>
<h1>DrownedMadonna archive</h1>
<p>Earlier versions of drownedmadonna.com recovered from the Wayback Machine. Download in progress: this site rebuilds as files arrive.</p>
<p><a href="exclusives.html">All exclusives, in chronological order</a> <small>{n_excl} so far</small></p>
<ul>{''.join(items)}</ul>""")


if __name__ == "__main__":
    main()
