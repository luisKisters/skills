---
name: calendr-design
description: Use when you add, change or review any SwiftUI view in the Calendr macOS calendar app (Sources/Calendr/Views), for example the week grid, event blocks, all-day row, sidebar, right column, event panel, participants, menus, dialogs, settings or the menu bar. Also use when asked to match the v4 mockup, apply the Calendr design system, fix colours, type, spacing or alignment in Calendr, or check a Calendr screen before done. It is the Calendr design system in the form of Geist (foundations, materials, components, patterns), with every locked v4 value and its SwiftUI mapping.
---

# Calendr design system
Calendr is a native macOS calendar in SwiftUI. This skill is its design system. It follows the form of the Vercel Geist docs: foundations, materials, components and patterns, each with a role for every value.

Every value comes from the v4 mockup. Do not add a value. The style names (for example `label-11.5`) only name locked values.
## Sources
Order of authority. If two sources disagree, the first wins.
1. `design/mockup-v4/DECISIONS.md`: locked decisions, rounds 1 to 5, and the design system.
2. `design/mockup-v4/index.html`: the `LOCKED` object, the `.ds` CSS, `themeVars()`, `evVars()`, `layoutDay()` and the "Design system" scene.
3. `design/mockup-v4/IMPLEMENTATION-PLAN.md`: phases, files and the target Swift names.

Do not use `design/LOCKED.md` (v3) or `design/DESIGN.md` (v2) for new work.
## Files
| File | Contents |
|---|---|
| [foundations.md](foundations.md) | Colours, typography, materials, layout, Swift mapping, files to change |
| [components.md](components.md) | Controls, rows, menus, events, participants, overlap layout, alignment |
## Principles
1. Content first. Events, names and times stand out. Icons, key hints and labels step back to `fg3`.
2. One value per job. 3 text sizes, 2 weights, 3 text colours, 2 row heights, 3 radii, 5 spacing steps.
3. Colour is data. Calendar colours belong to events. `act` is for the primary action and today. `live` is for now. Nothing else has colour.
4. Space before boxes. No box in a box. No panel separators. No capitals in labels.
5. Every edge is on a column. Hover boxes bleed 8 px, so the text does not move.
## Workflow
1. Find the mockup scene for the screen. Open `index.html`, select the scene in the picker, and press G for the alignment guides.
2. Read the view and `Theme.swift` before you change them.
3. Take the tokens from `foundations.md` and the spec from `components.md`.
4. If a Swift token does not exist yet, add it in `Theme.swift`, `Typeface.swift` or `Components.swift`. Never put a literal in a view.
5. Build. Run `scripts/verify.sh`. Render the snapshots with `scripts/snapshots.sh` and compare them with the scene.
6. Complete the check list.
## Check list
- [ ] Every text style is one of the 6 styles in `foundations.md`.
- [ ] Every text colour is `fg`, `fg2` or `fg3`.
- [ ] Surfaces use a material: base, raised, menu or modal.
- [ ] Row heights are 28 or 32. Icon buttons are 26 / 16 or 22 / 14.
- [ ] Radii are 6, 8 or 12. Spacing is 4, 8, 12, 16 or 24.
- [ ] Text is on the columns in `components.md` › Alignment. Fields bleed 8 px.
- [ ] Event reply states match the table. Overlaps use 2 lanes and "+N".
- [ ] No hex literal, font size or radius number in a view.
- [ ] `scripts/verify.sh` passes.
- [ ] The snapshot matches the scene. With G in the mockup, there are no red boxes.
