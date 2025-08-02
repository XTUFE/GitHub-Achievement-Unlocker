# GitHub Achievement Unlocker
🏅 A Python bot that helps you automatically unlock all GitHub contribution achievements — including Pull Shark, Pair Extraordinaire, and more. Easily simulate commits, PRs, co-authoring, and collaboration with full automation.

⭐ Please star this repo if you find it helpful!
I'm building unlockers for all GitHub achievements, and soon also for other platforms and apps. Stay tuned and show your support! 🙌


🦈 Pull Shark Achievement Unlocker

Unlock GitHub’s Pull Shark achievement automatically by creating and merging pull requests on a loop.

This Python bot simulates pull request activity by continuously creating branches, updating the README.md file, opening pull requests, and merging them — helping you earn the Pull Shark contribution badge on GitHub.
🚀 Features

    Creates new branches for every update

    Modifies README.md by appending a character

    Opens and merges a PR each cycle

    Helps you unlock the Pull Shark GitHub achievement

    Fully automated loop with adjustable speed

⚙️ Setup Instructions
1. Create a Public GitHub Repository

    Name it test or anything you like.

2. Generate a Fine-Grained Personal Access Token (PAT)

    Go to GitHub → Developer Settings → Tokens

    Create a new Fine-grained token

    Set Repository access to your chosen repo

    Under Permissions, enable:

        All Permissions  → Read and Write

3. Edit the Bot Script

Replace the placeholder values at the top of the script:

TOKEN = "YOUR GITHUB TOKEN"
OWNER = "YOUR GITHUB USERNAME"
REPO = "YOUR REPO NAME"
FILENAME = "README.md"

4. Install Requirements

pip install requests

5. Run the Bot

python bot.py

The bot will:

    Create a branch

    Update README.md

    Open and merge a pull request

    Repeat continuously

🧠 Why Use This?

This bot is ideal for:

    Unlocking the Pull Shark achievement automatically

    Testing GitHub Actions, PR workflows, or CI/CD pipelines

    Simulating user activity in your GitHub projects

⚠️ Notes

    Runs infinitely; press Ctrl + C to stop

    Default interval is 10 seconds between each iteration to prevent GitHub API abuse

    Requires a main branch in your repo

    Use responsibly to avoid hitting GitHub rate limits or triggering anti-abuse mechanisms

----------------------------------------

🤝 Pair Extraordinaire Achievement Bot

Automate GitHub contributions with a co-author to unlock the Pair Extraordinaire achievement.

This Python bot simulates co-authoring by continuously:

    Creating a new branch

    Appending to README.md

    Committing changes with a co-author signature

    Opening a pull request

    Merging the PR

    Repeating the process every few seconds

🌟 What It Does

    🔁 Auto-generates pull requests with co-authored commits

    🤝 Helps you and a friend (or alt account) unlock the Pair Extraordinaire badge

    🧪 Useful for testing co-authoring setups and GitHub workflows

    ⏱️ Sleeps between requests to avoid API abuse

⚙️ Setup Instructions
✅ 1. Create a Public GitHub Repository

    Name it test or any name you want.

    Ensure it has a main branch.

🤝 2. Add a Collaborator

    Invite your friend or secondary GitHub account to the repo.

    They must accept the invitation before running the bot.

🔑 3. Generate a Fine-Grained Personal Access Token

    Go to GitHub → Developer Settings → Tokens

    Click "Generate new token"

    Set Repository access to your test repo

    Set Permissions:

        All Permissions  → Read and Write

🛠️ 4. Configure the Script

Replace the following values in the script:

TOKEN = "YOUR GITHUB TOKEN"               # your fine-grained token
OWNER = "YOUR GITHUB USERNAME"            # your GitHub username
REPO = "YOUR TEST REPO"                   # your test repo name
FILENAME = "README.md"                    # file to modify

COAUTHOR_NAME = "YOUR FRIEND'S USERNAME"  
COAUTHOR_EMAIL = "FRIEND EMAIL ON COMMITS"  # must match verified email on GitHub

📦 5. Install Requirements

pip install requests

▶️ 6. Run the Bot

python bot.py

🧠 How It Works

    Uses the GitHub REST API to automate branch creation, file edits, PRs, and merges.

    Commits include the standard co-author signature:

    Co-authored-by: username <email>

    Each cycle appends a letter to README.md, creates a PR, and merges it.

💤 Delay and Retry Logic

    Sleep Time Between Cycles: 10 seconds (you can adjust it in time.sleep(10))

    On Failure: Waits 60 seconds and retries

🛑 Notes

    The co-author must have a GitHub-verified email that matches the one in the commit.

    This bot runs indefinitely — use Ctrl+C to stop it.

    Do not abuse the GitHub API; respect their rate limits.

🏅 Achievement: Pair Extraordinaire

Once you and your co-author make enough merged co-authored PRs, GitHub will award you the Pair Extraordinaire badge on your profile.


📄 License

MIT License. Use freely and modify as you like.
