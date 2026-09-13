---
name: publish-skill-to-skills-repo
description: Adds or updates a skill in Luis's personal agent-skills repository (github.com/luisKisters/skills) and verifies it before pushing. Use when the user says to add a skill to their skills repo, publish a skill, save a workflow as a skill for the repo, update a skill in github.com/luisKisters/skills, or "make this a skill" together with a repo. It enforces the repo's layout and frontmatter conventions, writes the short README and optional OpenAI/Codex metadata, lists the skill in the root README, validates the result, and commits and pushes on the correct branch.
---

# Publish a Skill to the Skills Repo

Target repository: `github.com/luisKisters/skills` (public). Install command:
`npx skills add github.com/luisKisters/skills --skill <name>`.

Trigger this skill whenever a reusable workflow must be added to that repo. The
goal is a skill another agent can install and follow without reading this
conversation.

## Repository conventions

Read `AGENTS.md` in the repo root first; it is the source of truth. Current
rules:

- Each skill is a top-level directory named after the skill (lowercase,
  hyphenated).
- The directory contains `SKILL.md` with YAML frontmatter: `name` and a long,
  trigger-rich `description`.
- Optional `agents/openai.yaml` carries OpenAI/Codex metadata.
- Supporting files (scripts, templates, configs) live inside the skill
  directory.
- Every skill has a short English `README.md` stating what it does, when it
  triggers, and how to install it.
- Every new skill is listed in the root `README.md`.

## Frontmatter

```yaml
---
name: skill-name
description: Use when <trigger classes>. <what the skill does, in one or two sentences>.
---
```

The description is what makes the skill get selected, so it must name the
concrete situations that should trigger it, not just what it does.

## Steps

1. **Locate or clone the repo.** Work in an existing clone when one is present;
   otherwise `gh repo clone luisKisters/skills`. Never edit a copy you are not
   going to push.
2. **Check the branch.** Read `git branch --show-current` and `git status`.
   Work on the default branch unless the user asked for a feature branch. Never
   force-push or rewrite history.
3. **Write the skill directory** `./<name>/` with:
   - `SKILL.md` (frontmatter + body; body is imperative, stepwise, with
     completion criteria per step),
   - `README.md` (what / when / install),
   - `agents/openai.yaml` when the skill benefits from Codex metadata:
     ```yaml
     interface:
       display_name: "<Title>"
       short_description: "<one line>"
       default_prompt: "Use $<name> to <action>."
     ```
   - any `scripts/` or `templates/` the skill needs.
4. **List the skill in the root `README.md`.** Add a `## <name>` section with a
   one-paragraph description ending in the exact install command:
   `npx skills add github.com/luisKisters/skills --skill <name>`. Match the
   existing entries' style.
5. **Validate before pushing.** Confirm, from the repo root:
   - `SKILL.md` frontmatter parses and `name` matches the directory;
   - the root `README.md` contains `--skill <name>`;
   - `git status` shows only intended files (no secrets, no editor files).
6. **Commit and push.** One focused commit, message style
   `feat(<name>): <what the skill does>`. Then report the pushed commit hash and
   the install command.

## Completion criteria

- `./<name>/SKILL.md`, `./<name>/README.md` exist; `agents/openai.yaml` if used.
- Root `README.md` lists `<name>` with its install command.
- `git log -1` on the remote contains the new skill.
- The final report gives the skill name, its trigger phrase, and the install
  command.

## Do not

- Do not add a skill to this repo without updating the root README.
- Do not include machine-specific absolute paths, tokens, or personal data.
- Do not push from a detached HEAD or the wrong branch.
- Do not duplicate a skill that already exists under a different name; update it
  instead.
