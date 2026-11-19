#!/usr/bin/env python3
"""Create one genuine, user-described GitHub issue."""
import os
import re

import requests

token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
owner = os.getenv("GITHUB_OWNER")
repo = os.getenv("GITHUB_REPO")
title = (os.getenv("ISSUE_TITLE") or "").strip()
body = (os.getenv("ISSUE_BODY") or "").strip()

if not all((token, owner, repo)):
    raise SystemExit("Set GITHUB_TOKEN, GITHUB_OWNER and GITHUB_REPO.")

if not title or len(title) < 12:
    raise SystemExit("For Quickdraw, provide a meaningful ISSUE_TITLE (at least 12 characters).")
if len(title) > 200:
    raise SystemExit("ISSUE_TITLE must be 200 characters or fewer.")
if not body or len(body) < 40:
    raise SystemExit("For Quickdraw, provide an ISSUE_BODY describing the real task (at least 40 characters).")

placeholder_patterns = (
    r"quickdraw",
    r"workflow\s*(check|test|run)",
    r"achievement\s*(check|test|run)",
    r"test\s*issue",
)
if any(re.search(pattern, title, re.IGNORECASE) for pattern in placeholder_patterns):
    raise SystemExit("ISSUE_TITLE must describe the actual project task, not an automation or achievement check.")

api = f"https://api.github.com/repos/{owner}/{repo}"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

response = requests.post(
    f"{api}/issues",
    headers=headers,
    json={"title": title, "body": body},
    timeout=30,
)
if not response.ok:
    try:
        detail = response.json()
    except ValueError:
        detail = response.text[:500]
    raise SystemExit(f"GitHub API issue creation failed: {response.status_code} {detail}")

issue = response.json()
print(f"Created project issue #{issue['number']}: {issue['html_url']}")
print("The issue was left open for normal project triage and work.")
