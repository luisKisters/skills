# Ralphex Plan Writer

This skill creates verification-first Markdown implementation plans for [Ralphex](https://github.com/umputun/ralphex) and [executr](https://github.com/luiskisters/executr). An agent triggers it when a user asks to convert a PRD or brainstorming note into autonomous implementation tasks or requests a Ralphex-compatible plan.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill ralphex-plan-writer
```

If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R ralphex-plan-writer ~/.codex/skills/ralphex-plan-writer`.
