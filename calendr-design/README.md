# Calendr Design

This skill is the design system of Calendr, a native macOS calendar app in SwiftUI. It follows the form of the Vercel Geist docs: foundations (colours, typography, materials, layout), components and patterns. It gives every locked value of the v4 mockup, the SwiftUI name for each token, the event reply states, the overlap layout and the alignment rules. It triggers when an agent adds, changes or reviews a view in `Sources/Calendr/Views`, or is asked to match the v4 mockup or check a Calendr screen.

Files: `SKILL.md` (principles, workflow, check list), `foundations.md`, `components.md`.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill calendr-design
```

If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R calendr-design ~/.claude/skills/calendr-design`.
