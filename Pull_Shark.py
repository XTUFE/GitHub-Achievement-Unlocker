#!/usr/bin/env python3
"""Pull Shark runner based on XTUFE's original branch -> commit -> PR -> merge flow.

Run a bounded number of cycles. Requires GITHUB_TOKEN with Contents and Pull requests
read/write access. GitHub decides whether generated activity qualifies for achievements.
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
    """Recover when the base branch advances while GitHub is processing a merge."""
    merge_path = f"/repos/{OWNER}/{REPO}/pulls/{pr_number}/merge"
    update_path = f"/repos/{OWNER}/{REPO}/pulls/{pr_number}/update-branch"
    last_error = None

    for attempt in range(1, 6):
        try:
            result = api("PUT", merge_path, json={
                "merge_method": "merge", "commit_title": commit_title
            })
            if result.get("merged"):
                return result
            raise RuntimeError(f"PR #{pr_number} was not merged: {result}")
        except GitHubAPIError as exc:
            last_error = exc
            if exc.status_code != 405:
                raise
            print(f"Merge race on PR #{pr_number} (attempt {attempt}/5); updating branch...")
            try:
                api("PUT", update_path, json={})
            except GitHubAPIError as update_error:
                # GitHub can report that the branch is already current; retry the merge.
                if update_error.status_code not in (405, 422):
                    raise
            time.sleep(min(2 * attempt, 10))

    raise RuntimeError(
        f"Could not merge PR #{pr_number} after 5 recovery attempts. "
        f"Last error: {last_error}"
    )


def config():
    if not TOKEN or not OWNER or not REPO:
        raise SystemExit("Set GITHUB_TOKEN, GITHUB_OWNER and GITHUB_REPO.")
    api("GET", f"/repos/{OWNER}/{REPO}")


def run_once(index):
    branch = f"achievement/pull-shark-{int(time.time())}-{uuid.uuid4().hex[:6]}"
    ref = api("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{BASE}")
    api("POST", f"/repos/{OWNER}/{REPO}/git/refs",
        json={"ref": f"refs/heads/{branch}", "sha": ref["object"]["sha"]})

    file_data = api("GET", f"/repos/{OWNER}/{REPO}/contents/{FILENAME}",
                    params={"ref": branch})
    content = base64.b64decode(file_data["content"]).decode("utf-8")
    marker = f"<!-- achievement-run:{uuid.uuid4()} | {datetime.now(timezone.utc).isoformat()} -->"
    updated = content.rstrip() + "\n\n" + marker + "\n"
    message = f"docs: record repository maintenance run {index}"
    api("PUT", f"/repos/{OWNER}/{REPO}/contents/{FILENAME}", json={
        "message": message,
        "content": base64.b64encode(updated.encode()).decode(),
        "sha": file_data["sha"],
        "branch": branch,
    })
    pr = api("POST", f"/repos/{OWNER}/{REPO}/pulls", json={
        "title": message, "head": branch, "base": BASE,
        "body": "Automated repository maintenance record.\n",
    })
    merge_pr_with_retry(pr["number"], message)
    print(f"Merged PR #{pr['number']} ({branch})")


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
