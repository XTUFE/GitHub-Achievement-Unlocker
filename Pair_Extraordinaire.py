#!/usr/bin/env python3
"""Pair Extraordinaire runner based on XTUFE's original co-authored PR flow.

The co-author must be a real GitHub account/collaborator and the email must be
verified and associated with that account. Never use another person's identity
without their consent. GitHub determines achievement eligibility.
"""
import argparse
import base64
import os
import time
import uuid
from datetime import datetime, timezone

import requests

API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")
BASE = os.getenv("GITHUB_BASE_BRANCH", "main")
FILENAME = os.getenv("GITHUB_TARGET_FILE", "README.md")
COAUTHOR_NAME = os.getenv("COAUTHOR_NAME")
COAUTHOR_EMAIL = os.getenv("COAUTHOR_EMAIL")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


class GitHubAPIError(RuntimeError):
    def __init__(self, method, path, response):
        self.status_code = response.status_code
        self.response_text = response.text[:500]
        super().__init__(f"{method} {path}: {response.status_code} {self.response_text}")


def api(method, path, **kwargs):
    response = SESSION.request(method, f"{API}{path}", timeout=30, **kwargs)
    if not response.ok:
        raise GitHubAPIError(method, path, response)
    return response.json() if response.content else {}


def merge_pr_with_retry(pr_number, commit_title):
    """Refresh a stale PR branch and retry if main advanced during a merge."""
    merge_path = f"/repos/{OWNER}/{REPO}/pulls/{pr_number}/merge"
    update_path = f"/repos/{OWNER}/{REPO}/pulls/{pr_number}/update-branch"

    for attempt in range(1, 6):
        try:
            result = api("PUT", merge_path, json={
                "merge_method": "merge",
                "commit_title": commit_title,
            })
            if result.get("merged"):
                return result
            raise RuntimeError(f"PR #{pr_number} was not merged: {result}")
        except GitHubAPIError as exc:
            if exc.status_code != 405 or "Base branch was modified" not in exc.response_text or attempt == 5:
                raise
            print(f"Base branch advanced during PR #{pr_number}; updating branch ({attempt}/5).")
            api("POST", update_path, json={})
            for _ in range(30):
                current = api("GET", f"/repos/{OWNER}/{REPO}/pulls/{pr_number}")
                if current.get("mergeable") is True:
                    break
                state = current.get("mergeable_state")
                if current.get("mergeable") is False and state not in ("unknown", "unstable"):
                    raise RuntimeError(f"PR #{pr_number} remains unmergeable after update: {state}")
                time.sleep(2)
            else:
                raise RuntimeError(f"PR #{pr_number} did not become mergeable after branch update.")
    raise RuntimeError(f"Could not merge PR #{pr_number} after five attempts.")



def config():
    missing = [key for key, value in {
        "GITHUB_TOKEN": TOKEN, "GITHUB_OWNER": OWNER, "GITHUB_REPO": REPO,
        "COAUTHOR_NAME": COAUTHOR_NAME, "COAUTHOR_EMAIL": COAUTHOR_EMAIL,
    }.items() if not value]
    if missing:
        raise SystemExit("Missing environment variables: " + ", ".join(missing))
    api("GET", f"/repos/{OWNER}/{REPO}")


def run_once(index):
    branch = f"achievement/pair-{int(time.time())}-{uuid.uuid4().hex[:6]}"
    ref = api("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{BASE}")
    api("POST", f"/repos/{OWNER}/{REPO}/git/refs",
        json={"ref": f"refs/heads/{branch}", "sha": ref["object"]["sha"]})

    file_data = api("GET", f"/repos/{OWNER}/{REPO}/contents/{FILENAME}",
                    params={"ref": branch})
    content = base64.b64decode(file_data["content"]).decode("utf-8")
    marker = f"<!-- coauthored-maintenance:{uuid.uuid4()} | {datetime.now(timezone.utc).isoformat()} -->"
    updated = content.rstrip() + "\n\n" + marker + "\n"
    message = (
        f"docs: record collaborative maintenance run {index}\n\n"
        f"Co-authored-by: {COAUTHOR_NAME} <{COAUTHOR_EMAIL}>"
    )
    api("PUT", f"/repos/{OWNER}/{REPO}/contents/{FILENAME}", json={
        "message": message,
        "content": base64.b64encode(updated.encode()).decode(),
        "sha": file_data["sha"],
        "branch": branch,
    })
    pr = api("POST", f"/repos/{OWNER}/{REPO}/pulls", json={
        "title": f"Collaborative maintenance #{index}",
        "head": branch, "base": BASE,
        "body": "Collaborative repository maintenance.\n",
    })
    merge_pr_with_retry(
        pr["number"], f"Merge collaborative maintenance #{index}"
    )
    print(f"Merged co-authored PR #{pr['number']} ({branch})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1, help="Number of PR cycles (1-20).")
    parser.add_argument("--delay", type=int, default=10, help="Seconds between cycles.")
    args = parser.parse_args()
    if not 1 <= args.count <= 20 or args.delay < 5:
        raise SystemExit("--count must be 1..20 and --delay at least 5 seconds.")
    config()
    for index in range(1, args.count + 1):
        run_once(index)
        if index < args.count:
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
