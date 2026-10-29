# Design System

This skill holds the format and the workflow for a design system, not one fixed design system. You put your own in. The format follows the Vercel Geist docs: `README.md` (sources, principles, checks), `foundations.md` (colours by role, text styles, materials, layout) and `components.md` (component specs, patterns, alignment). The agent uses the project's `design-system/` folder first, then a personal default in the skill's `system/` folder. It triggers when an agent builds, changes or reviews UI, or is asked to apply, check, create or extract a design system. It ships empty templates and a filled example (Calendr, a macOS SwiftUI calendar).

## Install

```sh
npx skills add github.com/luisKisters/skills --skill design-system
```

To set a personal default, copy `templates/` to `system/` in the installed skill and fill it. If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R design-system ~/.claude/skills/design-system`.
