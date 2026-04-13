#!/usr/bin/env python3
"""
Add `updated` field to each adapter entry in adapters.yaml.
The date is sourced from the GitLab API `created_at` field for each adapter repo.

Usage:
    GITLAB_TOKEN=<token> python3 scripts/add_updated_dates.py
"""

import os
import sys
import time
import urllib.request
import urllib.error
import json
import re

ADAPTERS_FILE = "adapters.yaml"
GITLAB_API = "https://gitlab.com/api/v4/projects/itentialopensource%2Fadapters%2F{name}"
DELAY = 0.1  # seconds between requests (no token = 500/hr; with token = 2000/min)

token = os.environ.get("GITLAB_TOKEN")


def fetch_created_at(name: str) -> str | None:
    url = GITLAB_API.format(name=urllib.parse.quote(name, safe=""))
    req = urllib.request.Request(url)
    if token:
        req.add_header("PRIVATE-TOKEN", token)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("created_at", "")[:10]  # YYYY-MM-DD
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  [WARN] 404 for {name}", file=sys.stderr)
        else:
            print(f"  [WARN] HTTP {e.code} for {name}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [WARN] Error for {name}: {e}", file=sys.stderr)
        return None


import urllib.parse  # noqa: E402 (import after use in function for readability)


def main():
    with open(ADAPTERS_FILE, "r") as f:
        lines = f.readlines()

    out = []
    current_name = None
    name_pattern = re.compile(r"^  - name:\s+(.+)$")
    icon_pattern = re.compile(r"^    icon:\s+.+$")

    for line in lines:
        # Track current adapter name
        m = name_pattern.match(line.rstrip("\n"))
        if m:
            current_name = m.group(1).strip()

        out.append(line)

        # After each icon line, inject updated:
        if icon_pattern.match(line.rstrip("\n")) and current_name:
            print(f"Fetching: {current_name}")
            date = fetch_created_at(current_name)
            if date:
                out.append(f'    updated: "{date}"\n')
                print(f"  -> {date}")
            else:
                out.append('    updated: ""\n')
            time.sleep(DELAY)

    with open(ADAPTERS_FILE, "w") as f:
        f.writelines(out)

    print("Done.")


if __name__ == "__main__":
    main()
