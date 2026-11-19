# GitHub Achievement Activity Checker

A GitHub Actions workflow that reviews **real contribution activity** in this repository.

## Run it

1. Open the repository's **Actions** tab.
2. Select **Achievement Activity Check**.
3. Click **Run workflow**.
4. Choose how many recently updated pull requests to inspect (1–50).

The workflow is read-only. It reports merged pull requests and commits whose messages contain a `Co-authored-by:` trailer. Results appear in the workflow run summary.

## Permissions and security

- Uses the automatically provided `GITHUB_TOKEN`; no personal access token or extra secret is needed.
- Requests only `contents: read` and `pull-requests: read`.
- Does not create branches, commits, pull requests, comments, or merges.
- Does not send tokens or repository data to third-party services.
- Runs only when manually dispatched and has a five-minute timeout.

## Important: achievements

GitHub controls achievement eligibility and does not provide a supported API for granting profile badges. This workflow is an activity checker, **not an achievement unlocker**. Genuine collaboration and qualifying contributions must happen naturally; fabricated activity or automated PR loops may be treated as spam and may not count.

## Legacy scripts

The old infinite-loop scripts have been retired because they generated repetitive commits and pull requests. They now display a notice directing users to this workflow.

## License

MIT.
