# Designr

Designr is a design workflow for agents. You design UI in rounds, in one interactive HTML mockup: the real app at real size on the left, a picker on the right. The agent makes 2 to 5 working options per decision. You hover to preview, pick, add notes on single elements with [Agentation](https://www.agentation.com), and paste your picks and notes back. The agent locks the picks in a decision log, cleans the result up into a design system (few text sizes, colours, heights, radii), checks the alignment with built-in guides, and hands it off: design system files, a token-to-code map, and a pixel compare of the app against each mockup scene. It works for any stack.

It triggers when you ask an agent to design or redesign an app, screen or style, to show options or variants, to lock a design, to clean up a cluttered UI, to make a design system from a design, or to build or check UI against a locked design.

When tasteskill (`design-taste-frontend`, tasteskill v2) is installed, designr loads it for the design read, the dials and the rules for each option. The user's picks and the locked design system win over it.

Each time the agent makes or changes a mockup, it serves it with a tiny local server (`templates/serve.mjs`, Node, no dependencies, 127.0.0.1 only) and sends you a clickable link to the page and scene, for example `http://127.0.0.1:4600/mockup-v2/index.html#busy`. It reuses a running server for the same folder. The file still opens from disk.

It ships a starter mockup (`templates/mockup.html`), a static server (`templates/serve.mjs`), a decision log template, design system templates, and the Calendr design system as a filled example.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill designr
```

For a personal default design system, copy `templates/design-system/` to `system/` in the installed skill and fill it. If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R designr ~/.claude/skills/designr`.
