#!/usr/bin/env python3
"""
Build an inventory of everything the Wayback Machine has archived for a domain.

Queries the CDX API (one row per unique URL, first successful capture),
writes inventory/urls.csv and a human-readable inventory/SUMMARY.md.
Only reads from archive.org; downloads no page content.
"""

import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

DOMAIN = os.environ.get("ARCHIVE_DOMAIN", "drownedmadonna.com")
OUT_DIR = os.environ.get("OUT_DIR", "inventory")
CDX = "https://web.archive.org/cdx/search/cdx"
PAGE_SIZE = 5000
USER_AGENT = "drownedmadonna-archive-inventory/1.0 (owner recovering own site)"


def fetch(params, attempts=6):
    """GET the CDX API with retries and exponential backoff."""
    url = CDX + "?" + urllib.parse.urlencode(params)
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8") or "[]")
        except Exception as exc:  # network errors, 429, 5xx
            wait = min(300, 10 * 2 ** attempt)
            print(f"  request failed ({exc}); retrying in {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"CDX request kept failing: {url}")


def classify(url, mimetype):
    """Rough content category, used only for the summary."""
    path = urllib.parse.urlsplit(url).path.lower()
    if mimetype.startswith("image/") or path.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")):
        return "image"
    if mimetype == "text/css" or path.endswith(".css"):
        return "css"
    if "javascript" in mimetype or path.endswith(".js"):
        return "js"
    if path.endswith((".mp3", ".mp4", ".pdf", ".zip")):
        return "media/file"
    if "/forum" in path or "viewtopic" in path or "showthread" in path:
        return "forum"
    if "/wp-content/" in path or "/wp-includes/" in path:
        return "wordpress-asset"
    if "/media/k2/" in path or "/components/" in path or "/templates/" in path:
        return "joomla-asset"
    if mimetype.startswith("text/html"):
        return "page"
    return "other"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    resume_key = None
    page = 0

    while True:
        params = {
            "url": DOMAIN,
            "matchType": "domain",          # includes www. and other subdomains
            "output": "json",
            "fl": "original,timestamp,mimetype,statuscode,length",
            "filter": "statuscode:200",
            "collapse": "urlkey",           # one row per unique URL
            "limit": PAGE_SIZE,
            "showResumeKey": "true",
        }
        if resume_key:
            params["resumeKey"] = resume_key

        data = fetch(params)
        page += 1
        if not data:
            break

        header, body = data[0], data[1:]
        resume_key = None
        # When more pages exist, an empty row is followed by the resume key.
        if len(body) >= 2 and body[-2] == []:
            resume_key = body[-1][0]
            body = body[:-2]

        for item in body:
            if len(item) == len(header):
                rows.append(dict(zip(header, item)))

        print(f"page {page}: {len(body)} rows (total {len(rows)})", flush=True)
        if not resume_key:
            break
        time.sleep(2)  # be gentle with archive.org

    # Full list.
    csv_path = os.path.join(OUT_DIR, "urls.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "year", "timestamp", "mimetype", "length", "original"])
        for r in rows:
            cat = classify(r["original"], r.get("mimetype", ""))
            writer.writerow([cat, r["timestamp"][:4], r["timestamp"], r.get("mimetype", ""),
                             r.get("length", ""), r["original"]])

    # Summary.
    by_cat = Counter()
    by_year = defaultdict(Counter)
    prefixes = Counter()
    size_by_cat = Counter()
    for r in rows:
        cat = classify(r["original"], r.get("mimetype", ""))
        by_cat[cat] += 1
        by_year[r["timestamp"][:4]][cat] += 1
        size_by_cat[cat] += int(r["length"]) if str(r.get("length", "")).isdigit() else 0
        parts = [p for p in urllib.parse.urlsplit(r["original"]).path.split("/") if p]
        prefixes["/" + parts[0] if parts else "/"] += 1

    lines = [f"# Wayback inventory for {DOMAIN}", "",
             f"Unique archived URLs (status 200): **{len(rows)}**", "",
             "## By category", "", "| Category | URLs | Compressed size (MB) |", "|---|---:|---:|"]
    for cat, n in by_cat.most_common():
        lines.append(f"| {cat} | {n} | {size_by_cat[cat] / 1048576:.1f} |")

    cats = [c for c, _ in by_cat.most_common()]
    lines += ["", "## By year of first successful capture", "",
              "| Year | " + " | ".join(cats) + " |", "|---|" + "---:|" * len(cats)]
    for year in sorted(by_year):
        lines.append(f"| {year} | " + " | ".join(str(by_year[year][c]) for c in cats) + " |")

    lines += ["", "## Top path prefixes", "", "| Prefix | URLs |", "|---|---:|"]
    for prefix, n in prefixes.most_common(40):
        lines.append(f"| `{prefix}` | {n} |")

    with open(os.path.join(OUT_DIR, "SUMMARY.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"done: {len(rows)} URLs -> {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
