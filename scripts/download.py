#!/usr/bin/env python3
"""
Download the original files of one era of drownedmadonna.com from the Wayback Machine.

For the capture window [CAPTURE_FROM, CAPTURE_TO] (years, inclusive):
  1. list every successful capture via the CDX API;
  2. collapse URL variants (http/https, www, :80, &amp;, session ids, param order)
     into one key and keep only the most recent capture of each key;
  3. drop captures whose content digest is identical to an already kept, newer one;
  4. fetch the raw original bytes (id_ mode) at ~1 request/second and save them
     under mirror/<ERA_LABEL>/, recording everything in a manifest.

The run is resumable: entries already in the manifest are skipped, and the script
stops cleanly before TIME_BUDGET_MIN so the workflow can commit and continue.
"""

import csv
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from urlkeys import normalize

DOMAIN = os.environ.get("ARCHIVE_DOMAIN", "drownedmadonna.com")
ERA = os.environ["ERA_LABEL"]
YEAR_FROM = os.environ["CAPTURE_FROM"]
YEAR_TO = os.environ["CAPTURE_TO"]
TIME_BUDGET_MIN = float(os.environ.get("TIME_BUDGET_MIN", "320"))
# archive.org throttles bursts (roughly 15 requests/minute); stay just under it.
DELAY = float(os.environ.get("REQUEST_DELAY", "4.0"))
CHECKPOINT_MIN = float(os.environ.get("CHECKPOINT_MIN", "10"))

ROOT = os.path.join("mirror", ERA)
PLAN_PATH = os.path.join(ROOT, "_plan.csv")
MANIFEST_PATH = os.path.join(ROOT, "_manifest.csv")
CDX = "https://web.archive.org/cdx/search/cdx"
USER_AGENT = "drownedmadonna-archive-downloader/1.0 (owner recovering own site)"
START = time.time()
STATS = {}  # retry reasons this run, reported in _status.md


def out_of_time():
    return (time.time() - START) / 60 > TIME_BUDGET_MIN


def http_get(url, attempts=6, raw=False):
    """GET with retries; backs off hard on 429/5xx to respect archive.org."""
    empty = b"" if raw else ""
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read()
                return resp.status, body if raw else body.decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 403, 410):
                return exc.code, empty
            STATS[f"http_{exc.code}"] = STATS.get(f"http_{exc.code}", 0) + 1
            wait = min(600, 30 * 2 ** attempt)
        except Exception as exc:
            name = type(exc).__name__
            STATS[name] = STATS.get(name, 0) + 1
            wait = min(300, 10 * 2 ** attempt)
        STATS["wait_seconds"] = STATS.get("wait_seconds", 0) + wait
        print(f"  retry in {wait}s: {url[:120]}", flush=True)
        time.sleep(wait)
    return None, empty


def list_captures():
    """All successful captures in the window, following CDX pagination."""
    rows, resume_key = [], None
    while True:
        params = {
            "url": DOMAIN, "matchType": "domain", "output": "json",
            "fl": "original,timestamp,mimetype,digest,length",
            "filter": "statuscode:200", "from": YEAR_FROM, "to": YEAR_TO,
            "limit": 10000, "showResumeKey": "true",
        }
        if resume_key:
            params["resumeKey"] = resume_key
        status, text = http_get(CDX + "?" + urllib.parse.urlencode(params))
        if status != 200 or not text.strip():
            break
        data = json.loads(text)
        header, body = data[0], data[1:]
        resume_key = None
        if len(body) >= 2 and body[-2] == []:
            resume_key = body[-1][0]
            body = body[:-2]
        rows += [dict(zip(header, r)) for r in body if len(r) == len(header)]
        print(f"listed {len(rows)} captures", flush=True)
        if not resume_key:
            break
        time.sleep(2)
    return rows


def build_plan():
    """Pick the newest capture per URL key, then drop identical content."""
    latest = {}
    for r in list_captures():
        key = normalize(r["original"])
        if key not in latest or r["timestamp"] > latest[key]["timestamp"]:
            latest[key] = r

    by_digest = {}
    for key, r in sorted(latest.items(), key=lambda kv: kv[1]["timestamp"], reverse=True):
        by_digest.setdefault(r["digest"], (key, r))  # newest wins on identical content

    plan = sorted(by_digest.values(), key=lambda kv: kv[0])
    os.makedirs(ROOT, exist_ok=True)
    with open(PLAN_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "timestamp", "mimetype", "digest", "length", "original"])
        for key, r in plan:
            w.writerow([key, r["timestamp"], r["mimetype"], r["digest"], r["length"], r["original"]])
    print(f"plan: {len(latest)} unique URLs, {len(plan)} after removing identical content", flush=True)


def local_path(key, mimetype):
    """Map a URL key to a safe file path inside the era folder."""
    path, _, query = key.partition("?")
    path = path.split("/", 1)[1] if "/" in path else ""
    if not path or path.endswith("/"):
        path += "index"
    if query:
        path += "__" + re.sub(r"[^A-Za-z0-9=._-]+", "_", query)[:150]
    path = re.sub(r"[^A-Za-z0-9/._,=-]+", "_", path)
    if "html" in mimetype and not re.search(r"\.(html?|php|asp)$", path, re.I):
        path += ".html"
    return os.path.join(ROOT, "files", path)


def checkpoint(done_count, total):
    """Write a progress file and push everything downloaded so far (CI only)."""
    with open(os.path.join(ROOT, "_status.md"), "w", encoding="utf-8") as f:
        f.write(f"# {ERA}\n\nProcessed {done_count} of {total} files "
                f"({100 * done_count / max(total, 1):.0f}%).\n\n"
                f"Last update: {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}\n\n"
                f"Delay between requests: {DELAY}s. "
                f"Retries this run: {json.dumps(STATS) if STATS else 'none'}\n")
    if not os.environ.get("GITHUB_ACTIONS"):
        return
    skip = ""
    cmds = [
        ["git", "add", "mirror/"],
        ["git", "commit", "-q", "-m", f"Wayback download: {ERA} checkpoint {done_count}/{total}" + skip],
        ["git", "pull", "--rebase", "-q"],
        ["git", "push", "-q"],
    ]
    for cmd in cmds:
        if subprocess.run(cmd).returncode != 0 and cmd[1] != "commit":
            print(f"  checkpoint step failed: {' '.join(cmd)}", flush=True)
            return
    print(f"checkpoint pushed: {done_count}/{total}", flush=True)


def main():
    if not os.path.exists(PLAN_PATH):
        build_plan()

    with open(PLAN_PATH, encoding="utf-8") as f:
        plan = list(csv.DictReader(f))

    done = set()
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            done = {row["key"] for row in csv.DictReader(f)}

    new_file = not os.path.exists(MANIFEST_PATH)
    manifest = open(MANIFEST_PATH, "a", newline="", encoding="utf-8")
    writer = csv.writer(manifest)
    if new_file:
        writer.writerow(["key", "timestamp", "status", "bytes", "file", "original"])

    todo = [p for p in plan if p["key"] not in done]
    print(f"{len(done)} already done, {len(todo)} to go", flush=True)
    checkpoint(len(done), len(plan))
    last_checkpoint = time.time()

    for i, p in enumerate(todo, 1):
        if out_of_time():
            print("time budget reached, stopping for this run", flush=True)
            break
        url = f"https://web.archive.org/web/{p['timestamp']}id_/{p['original']}"
        status, body = http_get(url, raw=True)
        rel = ""
        if status == 200 and body:
            rel = local_path(p["key"], p["mimetype"])
            os.makedirs(os.path.dirname(rel), exist_ok=True)
            with open(rel, "wb") as out:
                out.write(body)
        if status is not None:  # network failures are retried on the next run
            writer.writerow([p["key"], p["timestamp"], status, len(body), rel, p["original"]])
            manifest.flush()
        if i % 100 == 0:
            print(f"{i}/{len(todo)}", flush=True)
        if time.time() - last_checkpoint > CHECKPOINT_MIN * 60:
            checkpoint(len(done) + i, len(plan))
            last_checkpoint = time.time()
        time.sleep(DELAY)

    manifest.close()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        finished = sum(1 for _ in f) - 1
    complete = finished >= len(plan)
    print(f"progress: {finished}/{len(plan)} complete={complete}", flush=True)
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as gh:
        gh.write(f"complete={'true' if complete else 'false'}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
