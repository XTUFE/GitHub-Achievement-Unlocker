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

<!-- achievement-run:47756288-ba2e-4d1f-bbb6-103ad2d55473 | 2026-11-19T19:21:58.122620+00:00 -->

<!-- achievement-run:42910937-6bd8-4c7f-9f16-bdeb0297878e | 2026-11-19T19:22:08.393791+00:00 -->

<!-- achievement-run:4af6ed7c-6a4b-4fde-bf67-3e1f35186afd | 2026-11-19T19:22:20.951592+00:00 -->

<!-- achievement-run:d0836cc1-eb5f-4253-a0c9-323c2ffd423a | 2026-11-19T19:22:32.320503+00:00 -->

<!-- achievement-run:a129f326-e7f1-4375-9880-bd7d153ba9cd | 2026-11-19T19:22:43.037295+00:00 -->

<!-- achievement-run:57512d85-bd7e-4ea5-a484-cea955643dd0 | 2026-11-19T19:22:53.306053+00:00 -->

<!-- achievement-run:3dfe036c-d879-4182-8d7a-874ddeed66f6 | 2026-11-19T19:23:04.021130+00:00 -->

<!-- achievement-run:20faac3b-dd4e-4cbb-9ed8-ef6eb92def83 | 2026-11-19T19:23:14.637409+00:00 -->

<!-- achievement-run:b7f82097-4e18-4d4b-9658-42189a05ecf8 | 2026-11-19T19:25:55.599338+00:00 -->

<!-- achievement-run:d50f7c07-2f82-4733-9c52-9b58416382bc | 2026-11-19T19:55:50.561209+00:00 -->

<!-- achievement-run:b1796d7a-0b9d-4df9-80d9-49e0984d8e3f | 2026-11-19T19:56:06.776770+00:00 -->

<!-- achievement-run:24611655-e745-4163-926e-c712a86f9a9d | 2026-11-19T19:56:22.463257+00:00 -->

<!-- achievement-run:dd48ba28-ea5c-4a10-a056-23e7cb48c718 | 2026-11-19T19:56:39.259901+00:00 -->

<!-- achievement-run:23a440d1-c351-4edf-966a-4822e960217d | 2026-11-19T19:56:55.028018+00:00 -->

<!-- achievement-run:25542cf9-6f4f-4d92-ad35-8bd10a4a4c2a | 2026-11-19T19:57:11.615890+00:00 -->

<!-- achievement-run:58c573e5-b791-4754-a2d1-fb024c54ece2 | 2026-11-19T19:57:27.152006+00:00 -->

<!-- achievement-run:4c6d5d85-7696-4e17-a1bc-774460415dcb | 2026-11-19T19:57:43.019690+00:00 -->

<!-- achievement-run:234f57d9-d545-4e05-a877-be246f77e689 | 2026-11-19T19:57:58.932453+00:00 -->

<!-- achievement-run:67f6a1cd-4a47-4900-83ef-51ce9c31c9a9 | 2026-11-19T20:03:57.327131+00:00 -->

<!-- achievement-run:1a210d26-50d5-4fa4-a746-9ce03dd31b6a | 2026-11-19T20:04:19.398472+00:00 -->

<!-- achievement-run:10c3d82b-1d11-48fc-9fb5-9a40e6515cf3 | 2026-11-19T20:04:41.823289+00:00 -->

<!-- achievement-run:dc6e2dfa-144e-4b8e-ae96-80f035936c07 | 2026-11-19T20:04:57.287592+00:00 -->

<!-- achievement-run:ba697846-1465-4cfd-863d-1d7ca380e6bd | 2026-11-19T20:05:13.095188+00:00 -->

<!-- achievement-run:17b0577f-a0ee-4a4c-9771-d5f0137b6c92 | 2026-11-19T20:05:29.725151+00:00 -->
