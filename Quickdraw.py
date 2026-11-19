#!/usr/bin/env python3
"""Open and immediately close a pull request for the Quickdraw workflow.

This repository has GitHub Issues disabled, so use a short-lived PR instead.
"""
import base64
import os
import time
import uuid

import requests

token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
owner = os.getenv("GITHUB_OWNER")
repo = os.getenv("GITHUB_REPO")
base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
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


# Create a unique branch from the current base.
suffix = f"{int(time.time())}-{uuid.uuid4().hex[:8]}"
branch = f"quickdraw/{suffix}"
base_ref = request("GET", f"{api}/git/ref/heads/{base_branch}")
base_sha = base_ref["object"]["sha"]
request("POST", f"{api}/git/refs", json={
    "ref": f"refs/heads/{branch}",
    "sha": base_sha,
})

# Add a harmless unique README marker so GitHub accepts the PR.
readme = request("GET", f"{api}/contents/README.md?ref={base_branch}")
raw = base64.b64decode(readme["content"]).decode("utf-8")
marker = f"<!-- quickdraw:{uuid.uuid4()} -->"
updated = raw.rstrip() + "\n\n" + marker + "\n"
request("PUT", f"{api}/contents/README.md", json={
    "message": f"chore: quickdraw verification {suffix}",
    "content": base64.b64encode(updated.encode("utf-8")).decode("ascii"),
    "sha": readme["sha"],
    "branch": branch,
})

# Open and close the PR immediately (well within the five-minute window).
pr = request("POST", f"{api}/pulls", json={
    "title": "Quickdraw workflow verification",
    "body": "Short-lived pull request created and closed to verify Quickdraw automation.",
    "head": branch,
    "base": base_branch,
})
closed = request("PATCH", f"{api}/pulls/{pr['number']}", json={
    "state": "closed",
})
if closed.get("state") != "closed":
    raise RuntimeError(f"PR #{pr['number']} was not closed successfully.")
print(f"Opened and closed PR #{pr['number']} in one run.")
