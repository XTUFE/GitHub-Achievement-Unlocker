import requests
import base64
import time
import random
import string

# === GitHub Config ===
TOKEN = "YOUR GITHUB TOKEN"  # replace with your token
OWNER = "YOUR GITHUB USERNAME"                # your GitHub username
REPO = "YOUR TEST REPO"                  # your repo name
FILENAME = "README.md"         # file to edit

# === Co-author Info ===
COAUTHOR_NAME = "YOUR FRIEND OR OTHER COAUTHOR USERNAME"
COAUTHOR_EMAIL = "YOUR FRIEND OR OTHER COAUTHOR EMAIL"

# === GitHub API Headers ===
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# === Helper Functions ===

def random_branch_name():
    return "bot-branch-" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def get_file_content(branch="main"):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILENAME}?ref={branch}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    data = res.json()
    content = base64.b64decode(data["content"]).decode()
    sha = data["sha"]
    return content, sha

def create_branch(from_branch, new_branch):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{from_branch}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    sha = res.json()["object"]["sha"]

    payload = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }
    res = requests.post(f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs", headers=headers, json=payload)
    res.raise_for_status()

def update_readme(content, sha, branch):
    updated_content = content + "\nA"  # add one letter to README
    encoded = base64.b64encode(updated_content.encode()).decode()

    commit_message = (
        "Update README\n\n"
        f"Co-authored-by: {COAUTHOR_NAME} <{COAUTHOR_EMAIL}>"
    )

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILENAME}"
    payload = {
        "message": commit_message,
        "content": encoded,
        "branch": branch,
        "sha": sha
    }
    res = requests.put(url, headers=headers, json=payload)
    res.raise_for_status()

def create_pull_request(branch):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls"
    payload = {
        "title": "Automated PR with co-author",
        "head": branch,
        "base": "main",
        "body": f"Auto PR for co-author\n\nCo-authored-by: {COAUTHOR_NAME} <{COAUTHOR_EMAIL}>"
    }
    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()
    return res.json()["number"]

def merge_pull_request(pr_number):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pr_number}/merge"
    payload = {
        "commit_title": "Merge co-authored update"
    }
    res = requests.put(url, headers=headers, json=payload)
    res.raise_for_status()

def run_once():
    print("\n🚀 Starting new cycle...")

    branch = random_branch_name()
    print(f"🔧 Creating branch: {branch}")
    create_branch("main", branch)

    content, sha = get_file_content(branch)
    print("✏️ Updating README.md...")
    update_readme(content, sha, branch)

    print("📬 Creating pull request...")
    pr_number = create_pull_request(branch)

    print("✅ Merging pull request...")
    merge_pull_request(pr_number)

    print(f"🎉 PR #{pr_number} merged successfully with co-author '{COAUTHOR_NAME}'.")

# === Main Loop ===

count = 0
while True:
    try:
        run_once()
        count += 1
        print(f"🔁 Total PRs merged: {count}")
        time.sleep(1)  # delay between each run
    except Exception as e:
        print(f"⚠️ Error: {e}")
        print("⏳ Waiting 60 seconds before retrying...")
        time.sleep(60)
