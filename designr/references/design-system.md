# The design system files
The locked mockup becomes three files. The form follows the Vercel Geist docs: every value has a name and a role.
| File | Contents |
|---|---|
| `README.md` | Name, sources in order of authority, principles, project checks |
| `foundations.md` | Colours by role, text styles, materials (surfaces with fill, border, radius, shadow), layout, code mapping |
| `components.md` | One spec per component, patterns, alignment, do and avoid |

Empty files: [../templates/design-system/](../templates/design-system/). A filled example: [../examples/calendr/](../examples/calendr/).

## Find the active design system
Use the first one that exists:
1. The path that the project's `AGENTS.md` or `CLAUDE.md` names.
2. `design-system/` in the project root.
3. `system/` in this skill directory: the personal default.

If none exists, say so. Offer to make one from the mockup (step 4 to 6), or from the existing UI. Do not invent values.

## Write it
1. Copy `templates/design-system/` to the target.
2. Write the sources in `README.md`, in order of authority. Usually: `DECISIONS.md`, then the mockup (`LOCKED`, the token CSS, the "Design system" scene), then the theme code.
3. Fill `foundations.md` with exact values from the sources. Give each value one role. Add a "Code" column: the theme name in the code (for example `Theme.fg2`, `Font.label`, `Layout.radiusRow`).
4. Fill `components.md` with the components the product uses. Use one spec form for all: use, size, fill and text, hover, selected or focus, states.
5. Write the alignment rules as numbers: text columns, bleed of hover boxes, gutters.
6. Write principles that a reviewer can check, and the project checks.
7. Delete empty rows. Do not add a value without a source.

## Build from it
1. Read the three files, the view and the theme code before you change them.
2. Take every value from a token, every component from its spec.
3. If the theme code has no token for a value, add it in the theme file. Never put a literal in a view.
4. If the design system has no answer, ask the user, or make it the next round's decision.

## Rules
- The design system wins over taste and over framework defaults.
- One value per job. Two tokens with the same value and the same role are one token.
- Name values by role (`fg2`, `label`, `menu`), not by look (`grey`, `small`).
- Light and dark: write only the modes the user locked. Do not invent the other mode.
