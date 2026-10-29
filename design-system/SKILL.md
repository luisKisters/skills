---
name: design-system
description: Use when you build, change or review UI in a project that has a design system, or when the user asks to apply, follow, check, create or extract a design system, design tokens, a style guide or a mockup's visual rules. Works with any stack (SwiftUI, web, other). It finds the active design system (the project's, else the personal default in this skill), builds screens only from its tokens and component specs, and checks the result. It also creates a new design system in a Geist-style format (foundations, materials, components, patterns) from templates.
---

# Design system
This skill does not hold one design system. It holds the format and the workflow. You put your own design system in.
## The format
A design system is one folder with three files. The form follows the Vercel Geist docs: every value has a name and a role.
| File | Contents |
|---|---|
| `README.md` | Name, sources of truth, principles, project checks |
| `foundations.md` | Colours by role, text styles, materials, layout, code mapping |
| `components.md` | One spec per component, patterns, alignment, do and avoid |

Empty templates: [templates/](templates/). A filled example: [examples/calendr/](examples/calendr/).
## Find the active design system
Use the first one that exists:
1. The path that the project's `AGENTS.md` or `CLAUDE.md` names.
2. `design-system/` in the project root.
3. `system/` in this skill directory: the personal default.

If none exists, tell the user. Offer to create one (see "Create a design system"). Do not invent values to fill the gap.
## Build or change UI
1. Read the active `README.md`, `foundations.md` and `components.md`.
2. Read the view and the theme code before you change them.
3. Take every value from a token, a text style or a material. Take every component from its spec.
4. If the code has no token for a value yet, add it in the theme file. Never put a literal in a view.
5. If the design system has no answer, ask the user. Do not invent a value.
6. Run the checks in the active `README.md`. Compare the result with the source (mockup, screenshot).
## Create a design system
1. Copy `templates/` to the target: the project's `design-system/`, or `system/` in this skill for a personal default.
2. Collect the sources: mockup, CSS, decision log, screenshots, existing theme code. Write them in `README.md`, in order of authority.
3. Fill `foundations.md` from the sources. Take exact values. Give each value one role.
4. Fill `components.md` with the components the product uses. Use one spec format for all of them.
5. Delete empty rows and sections. Do not add a value without a source.
6. Write principles that a reviewer can check. Write a check list.
## Rules
- The design system wins over taste and over defaults of the framework.
- One value per job. Two tokens with the same value and the same role are one token.
- Name values by role (`fg2`, `label-12.5`, `menu`), not by look (`grey`, `small`).
- Keep each file short and scannable: tables and lists, no prose blocks.
## Check list before done
- [ ] Every colour, text style, radius, height and spacing is a token from `foundations.md`.
- [ ] Every component matches its spec in `components.md`.
- [ ] No literal value in a view outside the theme code.
- [ ] The checks in the active `README.md` pass.
- [ ] The result matches the source scene or screenshot.
