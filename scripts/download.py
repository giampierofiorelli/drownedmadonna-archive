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
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

from urlkeys import normalize

DOMAIN = os.environ.get("ARCHIVE_DOMAIN", "drownedmadonna.com")
ERA = os.environ["ERA_LABEL"]
YEAR_FROM = os.environ["CAPTURE_FROM"]
YEAR_TO = os.environ["CAPTURE_TO"]
# "files" (default): newest capture of each URL. "listings": every distinct
# capture of front pages and news listings, to recover stories never archived alone.
MODE = os.environ.get("ERA_MODE", "files") or "files"
# Optional "first-last" story ids: download only those PHP-Nuke articles, from any capture year.
SID_RANGE = os.environ.get("ERA_SID_RANGE", "")
TIME_BUDGET_MIN = float(os.environ.get("TIME_BUDGET_MIN", "320"))
# Pause between requests to stay well clear of archive.org rate limiting.
DELAY = float(os.environ.get("REQUEST_DELAY", "2.0"))
CHECKPOINT_MIN = float(os.environ.get("CHECKPOINT_MIN", "10"))
WORKERS = int(os.environ.get("WORKERS", "4"))
PUBLISH_EVERY_MIN = float(os.environ.get("PUBLISH_EVERY_MIN", "30"))
LAST_PUBLISH = 0.0

ROOT = os.path.join("mirror", ERA)
PLAN_PATH = os.path.join(ROOT, "_plan.csv")
MANIFEST_PATH = os.path.join(ROOT, "_manifest.csv")
RETRIES_PATH = os.path.join(ROOT, "_retries.json")
MAX_RUN_FAILURES = int(os.environ.get("MAX_RUN_FAILURES", "3"))
CDX = "https://web.archive.org/cdx/search/cdx"
USER_AGENT = "drownedmadonna-archive-downloader/1.0 (owner recovering own site)"
START = time.time()
STATS = {}  # retry reasons this run, reported in _status.md


def out_of_time():
    return (time.time() - START) / 60 > TIME_BUDGET_MIN


def http_get(url, attempts=6, raw=False):
    """GET with retries; backs off hard on 429/5xx to respect archive.org."""
    empty = b"" if raw else ""
    # Archived URLs can contain spaces, accents or other non-ASCII characters;
    # percent-encode them while leaving already-valid URL syntax untouched.
    url = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")
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
        except (UnicodeError, ValueError) as exc:
            # Not a network problem: retrying cannot help, so record it as failed.
            STATS[type(exc).__name__] = STATS.get(type(exc).__name__, 0) + 1
            return 0, empty
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


def in_sid_range(url):
    """PHP-Nuke article whose story id falls in SID_RANGE ("first-last")."""
    q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url.replace("&amp;", "&")).query))
    if q.get("file") != "article" or not q.get("sid", "").isdigit():
        return False
    first, last = (int(x) for x in SID_RANGE.split("-"))
    return first <= int(q["sid"]) <= last


def is_forum_page(url, mimetype):
    """phpBB topic and forum index pages: the posts themselves, not profiles or forms."""
    if "html" not in mimetype:
        return False
    q = {k.lower(): v for k, v in urllib.parse.parse_qsl(urllib.parse.urlsplit(url.replace("&amp;", "&")).query)}
    return q.get("name") == "Forums" and q.get("file") in ("viewtopic", "viewforum")


def is_listing_page(url):
    """Front pages and news listings, whose successive captures each show different stories."""
    parts = urllib.parse.urlsplit(url.replace("&amp;", "&"))
    path = (parts.path or "/").lower()
    if path in ("", "/", "/index.php", "/index.html", "/index.htm"):
        return True
    if not path.endswith("modules.php"):
        return False
    q = {k.lower(): v for k, v in urllib.parse.parse_qsl(parts.query)}
    if "sid" in q or q.get("file") in ("article", "print", "friend", "comments"):
        return False
    return q.get("name", "News") in ("News", "") and not q.get("d_op") and not q.get("op", "").startswith("modload")


def build_listing_plan():
    """Every distinct capture of the listing pages: each one may hold stories lost elsewhere."""
    by_digest = {}
    for r in list_captures():
        if "html" not in r.get("mimetype", "") or not is_listing_page(r["original"]):
            continue
        by_digest.setdefault(r["digest"], r)  # identical captures are kept once
    plan = []
    for r in by_digest.values():
        rest = normalize(r["original"]).split("/", 1)[1] if "/" in normalize(r["original"]) else ""
        plan.append((f"drownedmadonna.com/_snapshots/{r['timestamp']}/{rest}", r))
    plan.sort(key=lambda kv: kv[1]["timestamp"])
    os.makedirs(ROOT, exist_ok=True)
    with open(PLAN_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "timestamp", "mimetype", "digest", "length", "original"])
        for key, r in plan:
            w.writerow([key, r["timestamp"], r["mimetype"], r["digest"], r["length"], r["original"]])
    print(f"listing plan: {len(plan)} distinct captures of front and listing pages", flush=True)


def build_plan():
    """Pick the newest capture per URL key, then drop identical content."""
    if MODE == "listings":
        return build_listing_plan()
    latest = {}
    for r in list_captures():
        if SID_RANGE and not in_sid_range(r["original"]):
            continue
        if MODE == "forum" and not is_forum_page(r["original"], r.get("mimetype", "")):
            continue
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
    cmds = [
        ["git", "add", "mirror/"],
        ["git", "commit", "-q", "-m", f"Wayback download: {ERA} checkpoint {done_count}/{total}"],
        ["git", "pull", "--rebase", "-q"],
        ["git", "push", "-q"],
    ]
    for cmd in cmds:
        if subprocess.run(cmd).returncode != 0 and cmd[1] != "commit":
            print(f"  checkpoint step failed: {' '.join(cmd)}", flush=True)
            return
    print(f"checkpoint pushed: {done_count}/{total}", flush=True)

    # Pushes made with the Actions token do not trigger other workflows, so the
    # Pages site is republished explicitly, at most every PUBLISH_EVERY_MIN.
    global LAST_PUBLISH
    if time.time() - LAST_PUBLISH >= PUBLISH_EVERY_MIN * 60:
        if subprocess.run(["gh", "workflow", "run", "pages.yml", "--ref", "main"]).returncode == 0:
            LAST_PUBLISH = time.time()
            print("site republish requested", flush=True)


MANIFEST_HEADER = "key,timestamp,status,bytes,file,original"


def repair_manifest_header(path):
    """Restore the header row if an earlier run lost it (rows appended to a 0-byte file)."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith(MANIFEST_HEADER):
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(MANIFEST_HEADER + "\r\n" + text)
        print("manifest header restored", flush=True)


def main():
    if not os.path.exists(PLAN_PATH):
        build_plan()

    with open(PLAN_PATH, encoding="utf-8") as f:
        plan = list(csv.DictReader(f))

    repair_manifest_header(MANIFEST_PATH)
    done = set()
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            done = {row["key"] for row in csv.DictReader(f)}

    def append_row(row):
        # Open and close on every row: a checkpoint's `git pull --rebase` can
        # replace the manifest file, and a handle kept open would then write
        # into the old, unlinked copy and lose every later row.
        new_file = not os.path.exists(MANIFEST_PATH) or os.path.getsize(MANIFEST_PATH) == 0
        with open(MANIFEST_PATH, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new_file:
                w.writerow(["key", "timestamp", "status", "bytes", "file", "original"])
            w.writerow(row)

    # Files already in the repository but missing from the manifest (lost rows
    # from an earlier run) count as downloaded.
    recovered = 0
    for p in plan:
        if p["key"] in done:
            continue
        rel = local_path(p["key"], p["mimetype"])
        if os.path.exists(rel) and os.path.getsize(rel) > 0:
            append_row([p["key"], p["timestamp"], 200, os.path.getsize(rel), rel, p["original"]])
            done.add(p["key"])
            recovered += 1
    if recovered:
        print(f"recovered {recovered} files already downloaded", flush=True)

    retries = {}
    if os.path.exists(RETRIES_PATH):
        with open(RETRIES_PATH, encoding="utf-8") as f:
            retries = json.load(f)

    todo = [p for p in plan if p["key"] not in done]
    print(f"{len(done)} already done, {len(todo)} to go", flush=True)
    checkpoint(len(done), len(plan))
    last_checkpoint = time.time()

    def fetch_one(p):
        """Download one capture; runs in a worker thread."""
        url = f"https://web.archive.org/web/{p['timestamp']}id_/{p['original']}"
        status, body = http_get(url, raw=True)
        rel = ""
        if status == 200 and body:
            rel = local_path(p["key"], p["mimetype"])
            os.makedirs(os.path.dirname(rel), exist_ok=True)
            with open(rel, "wb") as out:
                out.write(body)
        time.sleep(DELAY)  # per-worker pause keeps the overall rate modest
        return p, status, len(body), rel

    # Archive responses are slow (~15s each), so a few parallel workers multiply
    # throughput while the request rate stays low. The manifest is written only
    # from this thread.
    processed = 0
    queue = iter(todo)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        running = set()
        while True:
            while len(running) < WORKERS and not out_of_time():
                p = next(queue, None)
                if p is None:
                    break
                running.add(pool.submit(fetch_one, p))
            if not running:
                break
            finished, running = wait(running, return_when=FIRST_COMPLETED)
            for fut in finished:
                p, status, size, rel = fut.result()
                processed += 1
                if status is None:
                    # Network failure: retry on later runs, but give up after
                    # MAX_RUN_FAILURES so an era can still complete.
                    retries[p["key"]] = retries.get(p["key"], 0) + 1
                    if retries[p["key"]] >= MAX_RUN_FAILURES:
                        status = "failed"
                if status is not None:
                    append_row([p["key"], p["timestamp"], status, size, rel, p["original"]])
                if processed % 100 == 0:
                    print(f"{processed}/{len(todo)}", flush=True)
            if time.time() - last_checkpoint > CHECKPOINT_MIN * 60:
                checkpoint(len(done) + processed, len(plan))
                last_checkpoint = time.time()
    if out_of_time():
        print("time budget reached, stopping for this run", flush=True)

    with open(RETRIES_PATH, "w", encoding="utf-8") as f:
        json.dump(retries, f, indent=0, sort_keys=True)
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        finished = sum(1 for _ in f) - 1
    complete = finished >= len(plan)
    print(f"progress: {finished}/{len(plan)} complete={complete}", flush=True)
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as gh:
        gh.write(f"complete={'true' if complete else 'false'}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
