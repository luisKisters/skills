---
name: pr-insights-automation
description: Makes a PR Insights style review pipeline fully automatic - a report on every pull request, published to a stable URL, and an architecture graph that refreshes itself on merge - without letting pull request code run next to secrets or a write token. Use when the user asks to automate PR reports, publish CI artifacts to GitHub Pages, stop hand-running refresh-docs, auto-update an architecture graph, fix a label-gated report workflow, or turn on a CI analyzer safely.
---

# PR Insights Automation

Turns a half-manual PR review pipeline into an automatic one. Assumes the repo already has a PR Insights style tool: a deterministic report generator plus a committed architecture graph. If it does not, stop and say so.

## The security model, which no step may regress

This is the constraint every decision below is shaped by:

- **Pull request code never runs in a job that has secrets or write permissions.**
- Jobs that need a write token or a secret run **base branch or default branch code only**, and never check out the pull request.
- Exactly one job may execute pull request code. It gets `contents: read`, no secrets, and it is skipped for forks.

If a step you are about to take would break this, do not take it. Say what it would expose.

## 1. Audit first

Read the repo and report which of these apply before changing anything. Do not assume; check.

| Finding | How to confirm |
| --- | --- |
| The committed graph never updates from a PR | `refresh-docs` is called with `--output-dir` in CI, and no job commits. The graph only moves in occasional manual commits |
| There is no browsable HTML | The report exists only as an artifact zip. The PR comment links a run page, not a URL |
| The workflow does not run on normal PR activity | The only trigger is a label applied by a local script |
| The analyzer is effectively off | The analyze step has no `env:` block, so the API key is never in scope and every run falls back to deterministic analysis |
| Docs drift | Infrastructure docs describe runners or outputs that no longer match the workflow |

Report which findings are real, then follow the migration order in section 8. Do not do all of it in one pull request.

## 2. The key design decision

**Do not commit the graph from the pull request run.** That run is either untrusted (fork) or a moving target (a new push invalidates it). Update the graph once, on the default branch, after the merge.

The pull request keeps the **overlay** view, which is the useful view during review anyway: same page, same renderer, plus an injected script marking added, changed and removed nodes against the base copy of the graph.

## 3. Publish to a stable URL

Publish each report into its own path on a `gh-pages` branch so reports coexist:

```
gh-pages/
  pr/123/index.html architecture.html summary.md ui/ agent-docs/
  main/            ← optional: the current graph, always fresh
```

```yaml
- uses: actions/download-artifact@v4
  with:
    name: pr-insights-${{ env.PR_NUMBER }}
    run-id: ${{ github.event.workflow_run.id }}
    github-token: ${{ github.token }}
    path: pr-report

- name: Publish to gh-pages
  uses: peaceiris/actions-gh-pages@v4
  with:
    github_token: ${{ github.token }}
    publish_dir: ./pr-report
    destination_dir: pr/${{ env.PR_NUMBER }}
    keep_files: true          # do not wipe other PRs
    commit_message: "docs(pr-insights): report for PR #${{ env.PR_NUMBER }}"
```

**Do not use `actions/deploy-pages` here.** It replaces the whole site on every deploy, which deletes every other PR report. Enable Pages with source "Deploy from a branch, gh-pages, root".

Then link the real page from the comment, keeping the existing marker-based upsert so the comment is edited rather than repeated:

```
https://<owner>.github.io/<repo>/pr/<number>/
https://<owner>.github.io/<repo>/pr/<number>/architecture.html
```

**Private repo fallback.** Pages for private repos needs a paid plan. If that blocks it, render one self-contained `report.html` with inline CSS and JS and images as data URIs, and attach it as its own artifact. One click, one file, no unzip. The graph overlay already works offline, so only image inlining is new work.

## 4. Report on every pull request

Replace the label trigger. Split the work across two workflows by trust.

Untrusted build. `pull_request` checks out the merge ref, has no secrets, and cannot write:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  workflow_dispatch:
    inputs:
      pr_number: { required: true, type: string }

concurrency:
  group: pr-insights-${{ github.event.pull_request.number || inputs.pr_number }}
  cancel-in-progress: true

permissions:
  contents: read
```

Keep the existing `resolve_pr` job. It still computes whether the head is same-repo, which now gates both the job that runs pull request code and the publish step.

Trusted publish. `workflow_run` always runs the **default branch** copy of the workflow file, with a write token, and never checks out pull request code:

```yaml
on:
  workflow_run:
    workflows: ["PR Insights"]
    types: [completed]

permissions:
  contents: write        # push to gh-pages
  pull-requests: write   # upsert the comment
```

Everything this workflow consumes is the artifact from the first one. **Treat it as data.** Read the PR number out of the index JSON; never `eval` anything from it, never pass it unquoted into a shell.

## 5. Refresh the graph on merge

A third, small workflow. Trusted code, default branch, one commit:

```yaml
name: Architecture graph
on:
  push:
    branches: [main]
    paths-ignore: ['docs/architecture-graph.html']
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: architecture-graph          # serialize; no cancel, or commits are lost
  cancel-in-progress: false

jobs:
  refresh:
    if: github.actor != 'github-actions[bot]'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v4
        with: { node-version: 22 }

      - name: Index the merged range
        env:
          BEFORE: ${{ github.event.before }}
          AFTER: ${{ github.sha }}
        run: |
          if ! git rev-parse --verify "$BEFORE^{commit}" >/dev/null 2>&1; then
            BEFORE="${AFTER}^"
          fi
          mkdir -p report-data
          node Tools/pr-insights.mjs index --base "$BEFORE" --head "$AFTER" \
            --output report-data/index.json

      - name: Analyze
        env:
          ANALYZER_API_KEY: ${{ secrets.ANALYZER_API_KEY }}   # safe: trusted code
        run: |
          node Tools/pr-insights.mjs analyze --index report-data/index.json \
            --output report-data/analysis.json

      # No --output-dir: this branch writes the graph and generated doc sections in place.
      - name: Refresh graph and generated doc sections
        run: |
          node Tools/pr-insights.mjs refresh-docs \
            --index report-data/index.json \
            --analysis report-data/analysis.json

      - name: Commit when something changed
        run: |
          if git diff --quiet -- docs/; then
            echo "graph already current"; exit 0
          fi
          git config user.name  'github-actions[bot]'
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git add docs/
          git commit -m 'chore(docs): refresh architecture graph [skip ci]'
          git push || (git pull --rebase && git push)
```

Four details that decide whether this works in practice:

1. **Loop guard.** The job's own commit triggers `push`. `paths-ignore`, the `github.actor` check, and `[skip ci]` together stop it. Test this first; a graph loop burns minutes fast.
2. **`github.event.before`.** On a merge this is the previous default-branch tip, so the diff is exactly the merged pull request. On a force-push it can be all zeroes, which is what the `rev-parse --verify` fallback above handles.
3. **Serialize.** Two merges in a row must not both push a graph. Use a non-cancelling concurrency group and retry the push once after a rebase.
4. **Branch protection.** If the default branch requires pull requests, a bot push is rejected. Either give the workflow a PAT or GitHub App token with bypass, or have it open a small `chore/graph-refresh` pull request instead. The pull request variant is slower but needs no privileged token. Ask the user which they want.

## 6. Turn the analyzer on, in trusted jobs only

- **Allowed:** the graph refresh workflow on the default branch, and `workflow_dispatch` runs.
- **Not allowed:** any `pull_request` job, because a fork pull request would see the secret. Also not the job that runs pull request code.

For per-pull-request reports from same-repo branches, keep `analyze` in the untrusted job **without** the key so it falls back to deterministic analysis, and let the prose come from the graph, whose summaries the default-branch run already filled in. If AI prose is genuinely wanted per pull request, move the analyze step into the trusted publish workflow, reading the index and diff JSON out of the artifact.

**Secrets rule.** The API key goes into 1Password first, then into a GitHub Actions secret. It must never appear in a log, a report, a commit, or a chat message. Never write it to a plaintext file in the repo.

## 7. Clean up

- A workflow on `pull_request: [closed]` that deletes `pr/<number>/` from `gh-pages`.
- A scheduled job that drops directories for pull requests closed more than 30 days ago.

## 8. Migration order

Do these as separate pull requests, in this order, verifying each before moving on.

1. Enable Pages on `gh-pages`. Add the publish workflow. **Keep the existing trigger for now.** Verify a real URL appears in the pull request comment.
2. Switch the trigger to `pull_request`. Confirm a fork pull request produces a report with no privileged job and no secret in scope.
3. Add the graph refresh workflow on a branch. Run it with `workflow_dispatch` first and **read the diff before enabling the push step.**
4. Set the analyzer secret and enable it for the trusted jobs only.
5. Add the pull-request-closed cleanup and the scheduled sweep.
6. Fix the drifted docs so they describe the runners and outputs that actually exist.

## 9. Report back

State which findings were real, which steps you completed, the published URL, and anything still requiring a human decision, in particular the branch-protection choice in section 5 and whether the repo can use Pages at all.
