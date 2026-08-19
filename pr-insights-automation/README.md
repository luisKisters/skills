# PR Insights Automation

This skill makes a PR Insights style review pipeline automatic: a report on every pull request, published to a stable URL instead of a downloadable artifact, and an architecture graph that refreshes itself when a pull request merges. An agent triggers it when a user asks to automate PR reports, publish CI artifacts to GitHub Pages, stop hand-running `refresh-docs`, auto-update an architecture graph, replace a label-gated report workflow, or turn on a CI analyzer safely.

The security model is the constraint the whole design follows: pull request code never runs in a job that has secrets or write permissions. The skill audits the repo first, then works through a fixed migration order, one pull request per step.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill pr-insights-automation
```

If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R pr-insights-automation ~/.codex/skills/pr-insights-automation`.
