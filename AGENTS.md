# Repository Conventions

- Each skill is a top-level directory named after the skill.
- Each skill directory has a `SKILL.md` with YAML frontmatter that contains `name` and a long, trigger-rich `description`.
- An optional `agents/openai.yaml` provides OpenAI and Codex interface metadata: `display_name`, `short_description`, and `default_prompt`.
- Supporting files, such as scripts and JSON configurations, live inside the skill directory.
- Every skill must have a short English `README.md` that states what it does, when it triggers, and how to install it.
- List every new skill in the root `README.md`.
- Use this install command: `npx skills add github.com/luisKisters/skills --skill <name>`.
