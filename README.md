# Agent Skills

This repository is my personal collection of agent skills. Each skill packages focused instructions and any supporting resources an agent needs to carry out a repeatable workflow.

## ralphex-plan-writer

`ralphex-plan-writer` creates verification-first Markdown implementation plans compatible with Ralphex and executr. An agent should trigger it when asked to turn a PRD or brainstorming note into autonomous implementation tasks, design an executr verification loop, or prepare a Ralphex-compatible plan. It emphasizes minimal, approval-gated architecture, deterministic verification, and validation with its bundled format checker. Install it with `npx skills add github.com/luisKisters/skills --skill ralphex-plan-writer`.

## hyperkey-setup

`hyperkey-setup` installs or configures Karabiner-Elements with a bundled Caps Lock Hyperkey and right Shift launcher mapping. An agent should trigger it when a user asks for this keyboard setup, wants Caps Lock to act as Hyper when held and Cmd+Tab when tapped, or wants right Shift to launch Cmd+Space or Raycast when tapped. It handles installation checks, safely copies the predefined rules, guides or automates setup where possible, and verifies both shortcuts. Install it with `npx skills add github.com/luisKisters/skills --skill hyperkey-setup`.

## concise-comms

`concise-comms` enforces concise, ADHD-friendly responses in ASD-STE100 Simplified Technical English or equivalent controlled German and tolerates likely voice-dictation transcription errors. An agent should trigger it when a user asks for shorter or clearer replies, says they have ADHD, says they dictate by voice, asks for Simplified Technical English, or starts any session with this user. Install it with `npx skills add github.com/luisKisters/skills --skill concise-comms`.

## How to install a skill

Install one skill with `npx skills add <repo> --skill <name>`. For this repository, replace `<repo>` with `github.com/luisKisters/skills` and `<name>` with the skill name shown above.

If the CLI is unavailable, clone or download the repository and manually copy the selected skill directory into your agent's skills directory, for example `cp -R <skill-directory> ~/.codex/skills/<name>`.
