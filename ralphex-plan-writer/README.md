# Ralphex Plan Writer

This skill creates verification-first Markdown implementation plans compatible with Ralphex and executr. An agent triggers it when asked to turn a PRD or brainstorming note into autonomous implementation tasks, plan a UI change, design an executr verification loop, or prepare a Ralphex-compatible plan.

It decides how much plan the change earns before writing one, so a bugfix gets no plan at all. UI work is planned in HTML first, through mockups with locked decisions, and only then converted into one Markdown plan the agent executes. Verification is written while the code still does not exist, and it validates the result with the bundled format checker.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill ralphex-plan-writer
```

If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R ralphex-plan-writer ~/.codex/skills/ralphex-plan-writer`.
