# Agent Skills

This repository is my personal collection of agent skills. Each skill packages focused instructions and any supporting resources an agent needs to carry out a repeatable workflow.

## ralphex-plan-writer

`ralphex-plan-writer` creates verification-first Markdown implementation plans compatible with Ralphex and executr. An agent should trigger it when asked to turn a PRD or brainstorming note into autonomous implementation tasks, plan a UI change, design an executr verification loop, or prepare a Ralphex-compatible plan. It decides how much plan the change earns before writing one, plans UI in HTML mockups with locked decisions before converting to Markdown, writes the verification while the code still does not exist, and validates the result with its bundled format checker. Install it with `npx skills add github.com/luisKisters/skills --skill ralphex-plan-writer`.

## hyperkey-setup

`hyperkey-setup` installs or configures Karabiner-Elements with a bundled Caps Lock Hyperkey and right Shift launcher mapping. An agent should trigger it when a user asks for this keyboard setup, wants Caps Lock to act as Hyper when held and Cmd+Tab when tapped, or wants right Shift to launch Cmd+Space or Raycast when tapped. It handles installation checks, safely copies the predefined rules, guides or automates setup where possible, and verifies both shortcuts. Install it with `npx skills add github.com/luisKisters/skills --skill hyperkey-setup`.

## stop-yapping

`stop-yapping` stops rambling while keeping responses short, clear, self-contained, and complete. An agent should trigger it when a user says the agent is yapping, rambling, too verbose, or unclear, or asks for shorter, direct, ADHD-friendly communication. If invoked alone, it answers the user's previous substantive message with these rules. Install it with `npx skills add github.com/luisKisters/skills --skill stop-yapping`.

## orchestrated-build

`orchestrated-build` executes a written implementation plan with a fleet of agents: one Opus 5 low subagent per vertical slice, each supervising Luna Max implementation runs in tmux, with 10-minute check-ins, one review phase before the end-to-end phase, and a human-gated merge. Below roughly 50 changed lines it deliberately does not fan out at all. An agent should trigger it when a user asks to execute or ship a plan, delegate slices to subagents, parallelize a build, or supervise long autonomous runs. Install it with `npx skills add github.com/luisKisters/skills --skill orchestrated-build`.

## pr-insights-automation

`pr-insights-automation` makes a PR Insights style review pipeline automatic: a report on every pull request, published to a stable URL instead of a downloadable artifact, and an architecture graph that refreshes itself when a pull request merges. An agent should trigger it when a user asks to automate PR reports, publish CI artifacts to GitHub Pages, stop hand-running `refresh-docs`, auto-update an architecture graph, replace a label-gated report workflow, or turn on a CI analyzer safely. It keeps one constraint throughout: pull request code never runs in a job that has secrets or write permissions. Install it with `npx skills add github.com/luisKisters/skills --skill pr-insights-automation`.

## How to install a skill

Install one skill with `npx skills add <repo> --skill <name>`. For this repository, replace `<repo>` with `github.com/luisKisters/skills` and `<name>` with the skill name shown above.

If the CLI is unavailable, clone or download the repository and manually copy the selected skill directory into your agent's skills directory, for example `cp -R <skill-directory> ~/.codex/skills/<name>`.
