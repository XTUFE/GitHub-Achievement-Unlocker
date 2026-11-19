# GitHub Achievement Unlocker

Restored from the original [XTUFE/GitHub-Achievement-Unlocker](https://github.com/XTUFE/GitHub-Achievement-Unlocker), with bounded runs, environment-based credentials, unique branches, API error handling and GitHub Actions support.

## Run from GitHub Actions

1. Open **Actions → Achievement Automation**.
2. Click **Run workflow**.
3. Select a mode and cycle count.
4. For Pair Extraordinaire, configure the two co-author secrets described below.

Modes:
- `pull-shark`: create a branch, make a README maintenance commit, open a PR and merge it.
- `pair`: same flow with a real co-author trailer in the commit.
- `quickdraw`: create and close a test issue in the same run.
- `yolo`: create and merge an unreviewed PR (also contributes to Pull Shark activity).
- `all`: run Pull Shark, Pair Extraordinaire and Quickdraw in sequence.

The runner is deliberately bounded: 1–20 cycles, at least 5 seconds between PR cycles. It does not run forever.

## Required repository settings

In **Settings → Actions → General → Workflow permissions**, allow read/write permissions. Also enable **Allow GitHub Actions to create and approve pull requests**.

The workflow uses the built-in `GITHUB_TOKEN`. No PAT is required. The token needs Contents, Pull requests and Issues write access (provided by the workflow permissions).

For Pair Extraordinaire, add these repository Actions secrets:
- `COAUTHOR_NAME`: the actual collaborator's GitHub display/name identity.
- `COAUTHOR_EMAIL`: an email verified and associated with that collaborator's GitHub account.

The co-author must be a real account that has agreed to participate. A fabricated or unrelated co-author email will not credit that account. Pair Extraordinaire is based on co-authored commits in merged PRs; GitHub decides whether the activity qualifies.

## Achievement requirements (current public references)

| Achievement | Requirement | What this project can do |
|---|---|---|
| Pull Shark | Have PRs you opened merged. Commonly reported tiers: 2 / 16 / 128 / 1,024 merged PRs. | Automates PR creation and merge. |
| Pair Extraordinaire | Co-author commits in merged PRs. Commonly reported tiers: 1 / 10 / 24 / 48. | Automates only when a real collaborator and verified email are configured. |
| Quickdraw | Close an issue or PR within 5 minutes of opening it. | Creates and closes a test issue. |
| YOLO | Merge a PR without a review. | The PR runner merges without requesting a review. |
| Starstruck | A repository you created receives stars. Commonly reported tiers: 16 / 128 / 512 / 4,096. | Cannot manufacture genuine stars; other people must star the repository. |
| Galaxy Brain | Have answers accepted in repository Discussions. Commonly reported tiers: 2 / 8 / 16 / 32. | Cannot mark your own answer accepted; another participant or maintainer must accept it. |
| Public Sponsor | Publicly sponsor a developer through GitHub Sponsors. | Requires a real sponsorship/payment; not automated here. |

Tier counts above are community-reported references, not a promise of award. GitHub's own achievement UI is authoritative and may change. The original GitHub Community discussion is [here](https://github.com/orgs/community/discussions/176080); a current criteria index is [here](https://conroy1988.github.io/Achievements/docs/achievement-index.html).

## Not currently unlockable by a normal automation run

- **Arctic Code Vault Contributor** and **Mars 2020 Contributor** are historical/retired.
- **Heart On Your Sleeve** and **Open Sourcerer** have no stable, generally available unlock criteria; don't count them as reliably earnable.
- GitHub awards badges itself. There is no supported API to directly grant achievements, and running a script cannot guarantee that GitHub will award a badge.

## Local usage

```bash
pip install requests
export GITHUB_TOKEN="..."
export GITHUB_OWNER="your-user"
export GITHUB_REPO="your-repo"
python Pull_Shark.py --count 1
```

For Pair Extraordinaire, also set `COAUTHOR_NAME` and `COAUTHOR_EMAIL`, then run `python Pair_Extraordinaire.py --count 1`.

## License

MIT.
