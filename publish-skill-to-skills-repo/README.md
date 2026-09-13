# Publish Skill to Skills Repo

This skill adds or updates a skill in Luis's personal agent-skills repository at
`github.com/luisKisters/skills`. It triggers when an agent is asked to publish a
skill, add a workflow to the skills repo, or update a skill there. It enforces
the repo's directory layout and frontmatter conventions, writes the short
README and optional OpenAI/Codex metadata, lists the skill in the root README,
validates the result, and commits and pushes on the correct branch.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill publish-skill-to-skills-repo
```

If the CLI is unavailable, clone or download the repository and copy the skill
directory into the agent's skills directory, for example
`cp -R publish-skill-to-skills-repo ~/.codex/skills/publish-skill-to-skills-repo`.
