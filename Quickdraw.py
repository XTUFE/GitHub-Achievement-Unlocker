#!/usr/bin/env python3
"""Create and close one issue to exercise the Quickdraw workflow."""
import os
import requests

token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
owner = os.getenv("GITHUB_OWNER")
repo = os.getenv("GITHUB_REPO")
if not all((token, owner, repo)):
    raise SystemExit("Set GITHUB_TOKEN, GITHUB_OWNER and GITHUB_REPO.")

base = f"https://api.github.com/repos/{owner}/{repo}/issues"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
created = requests.post(base, headers=headers, json={
    "title": "Quickdraw workflow verification",
    "body": "Short-lived issue created to verify the repository's issue lifecycle automation.",
}, timeout=30)
created.raise_for_status()
issue = created.json()
closed = requests.patch(f"{base}/{issue['number']}", headers=headers,
                        json={"state": "closed", "state_reason": "not_planned"}, timeout=30)
closed.raise_for_status()
print(f"Created and closed issue #{issue['number']} in one run.")
