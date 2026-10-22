#!/usr/bin/env python3
"""
Look for every Wayback capture around a period that the regular inventory
may have missed: any HTTP status, every capture (not one per URL), RSS feeds,
and related domains. Writes inventory/probe/<name>.csv.
"""

import csv
import json
import os
import time
import urllib.parse
import urllib.request

CDX = "https://web.archive.org/cdx/search/cdx"
UA = "drownedmadonna-archive-probe/1.0 (owner recovering own site)"
FROM, TO = os.environ.get("PROBE_FROM", "20070301"), os.environ.get("PROBE_TO", "20070630")
OUT = os.path.join("inventory", "probe")

QUERIES = {
    # Every capture of the main domain in the period, any status.
    "domain-period": {"url": "drownedmadonna.com", "matchType": "domain", "from": FROM, "to": TO},
    # RSS and headline feeds of PHP-Nuke, any year.
    "feeds": {"url": "drownedmadonna.com/backend.php", "matchType": "prefix"},
    "feeds-ultramode": {"url": "drownedmadonna.com/ultramode", "matchType": "prefix"},
    "feeds-rss": {"url": "drownedmadonna.com/rss", "matchType": "prefix"},
    # Sister sites and other domains the news may have been mirrored on.
    "madonnafanzine": {"url": "madonnafanzine.com", "matchType": "domain", "from": "2006", "to": "2008"},
    "drownedmadonna-it": {"url": "drownedmadonna.it", "matchType": "domain"},
    "drownedmadonna-net": {"url": "drownedmadonna.net", "matchType": "domain"},
    "drownedmadonna-org": {"url": "drownedmadonna.org", "matchType": "domain"},
}


def fetch(params):
    url = CDX + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode("utf-8") or "[]")
        except Exception as exc:
            wait = min(300, 15 * 2 ** attempt)
            print(f"  {exc}; retry in {wait}s", flush=True)
            time.sleep(wait)
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, q in QUERIES.items():
        params = dict(q, output="json", fl="timestamp,original,mimetype,statuscode,length,digest",
                      showResumeKey="true", limit="5000")
        rows, resume = [], None
        while True:
            if resume:
                params["resumeKey"] = resume
            data = fetch(params)
            if data is None:
                print(f"{name}: failed")
                break
            resume = None
            if data and len(data[-1]) == 1 and data[-1][0]:
                resume = data[-1][0]
                data = data[:-2]
            rows += [r for r in data[1:] if len(r) == 6]
            if not resume:
                break
            time.sleep(2)
        with open(os.path.join(OUT, f"{name}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "original", "mimetype", "statuscode", "length", "digest"])
            w.writerows(rows)
        print(f"{name}: {len(rows)} captures", flush=True)
        time.sleep(3)


if __name__ == "__main__":
    main()
