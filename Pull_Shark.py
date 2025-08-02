import requests
import base64
import time

# Replace these with your own values
TOKEN = "YOUR GITHUB TOKEN"
OWNER = "YOUR GITHUB USERNAME"
REPO = "YOUR TEST REPO"
FILENAME = "README.md"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_file_sha_and_content(branch="main"):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILENAME}?ref={branch}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    sha = data["sha"]
    return content, sha


def create_branch(base_branch, new_branch):
    ref_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{base_branch}"
    r = requests.get(ref_url, headers=headers)
    r.raise_for_status()
    sha = r.json()["object"]["sha"]

    create_ref_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs"
    payload = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }
    r = requests.post(create_ref_url, headers=headers, json=payload)
    r.raise_for_status()

def update_file(content, sha, branch):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILENAME}"
    updated_content = content + "A"  # Add a letter
    encoded_content = base64.b64encode(updated_content.encode()).decode()
    data = {
        "message": "bot: update readme",
        "content": encoded_content,
        "branch": branch,
        "sha": sha
    }
    r = requests.put(url, headers=headers, json=data)
    r.raise_for_status()

def create_pull_request(branch):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls"
    data = {
        "title": "bot: update readme",
        "head": branch,
        "base": "main"
    }
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()
    return r.json()["number"]

def merge_pull_request(pr_number):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pr_number}/merge"
    data = {
        "commit_title": "bot: merge readme change"
    }
    r = requests.put(url, headers=headers, json=data)
    r.raise_for_status()

def bot_loop():
    count = 0
    while True:
        print(f"\n--- Iteration {count} ---")
        branch_name = f"bot-update-{int(time.time())}"

        print("Creating branch...")
        create_branch("main", branch_name)

        # Now get file content/SHA from the new branch
        content, sha = get_file_sha_and_content(branch_name)

        print("Updating README...")
        update_file(content, sha, branch_name)

        print("Creating PR...")
        pr_number = create_pull_request(branch_name)

        print("Merging PR...")
        merge_pull_request(pr_number)

        print("Done.")
        count += 1
        time.sleep(10)  # You can reduce this if needed


bot_loop()
