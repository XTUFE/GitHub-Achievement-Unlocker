#!/usr/bin/env python3
"""Create and immediately close a GitHub issue for the Quickdraw achievement."""
import os
import time
import uuid

import requests

token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
owner = os.getenv("GITHUB_OWNER")
repo = os.getenv("GITHUB_REPO")
if not all((token, owner, repo)):
    raise SystemExit("Set GITHUB_TOKEN, GITHUB_OWNER and GITHUB_REPO.")

api = f"https://api.github.com/repos/{owner}/{repo}"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
session = requests.Session()
session.headers.update(headers)


def request(method, url, **kwargs):
    response = session.request(method, url, timeout=30, **kwargs)
    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text[:500]
        raise RuntimeError(
            f"GitHub API {method} {url} failed: "
            f"{response.status_code} {detail}"
        )
    return response.json() if response.content else {}


# Quickdraw is based on closing an issue within five minutes of opening it.
# Keep the issue unique so every workflow run is independently auditable.
suffix = f"{int(time.time())}-{uuid.uuid4().hex[:8]}"
issue = request("POST", f"{api}/issues", json={
    "title": f"Quickdraw workflow check {suffix}",
    "body": (
        "Temporary issue created by the GitHub Achievement Unlocker "
        f"Quickdraw workflow. Run marker: {uuid.uuid4()}."
    ),
})

issue_number = issue["number"]
closed = request("PATCH", f"{api}/issues/{issue_number}", json={
    "state": "closed",
})
if closed.get("state") != "closed":
    raise RuntimeError(f"Issue #{issue_number} was not closed successfully.")

print(f"Opened and closed issue #{issue_number} in one run.")
