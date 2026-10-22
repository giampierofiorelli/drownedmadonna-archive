#!/usr/bin/env python3
"""
Print the first era in config/download.json that is not fully downloaded,
as GitHub Actions outputs (era, from, to, done). An era is complete when its
manifest has a row for every entry of its plan.
"""

import csv
import json
import os


def rows(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def main():
    with open("config/download.json", encoding="utf-8") as f:
        eras = json.load(f)["eras"]
    pick = None
    for era in eras:
        base = os.path.join("mirror", era["era"])
        planned = rows(os.path.join(base, "_plan.csv"))
        finished = rows(os.path.join(base, "_manifest.csv")) or 0
        if planned is None or finished < planned:
            pick = era
            break
    out = os.environ.get("GITHUB_OUTPUT", os.devnull)
    with open(out, "a", encoding="utf-8") as f:
        if pick:
            f.write(f"era={pick['era']}\nfrom={pick['capture_from']}\nto={pick['capture_to']}\n"
                    f"mode={pick.get('mode', 'files')}\nsids={pick.get('sid_range', '')}\ndone=false\n")
        else:
            f.write("done=true\n")
    print(pick["era"] if pick else "all eras complete")


if __name__ == "__main__":
    main()
