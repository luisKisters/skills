---
name: designr
description: Use when the user wants to design or redesign UI with an agent - a new app, screen, flow, component or visual style - or says "make it look better", "show me options", "mockup", "variants", "design round", "lock this", "too cluttered", "too many fonts or colours", or wants a design system made from a design, or wants UI built or checked against a locked design. Works for any stack (SwiftUI, web, other). The workflow - one interactive HTML mockup with a picker, rounds of user picks and feedback, a decision log, a clean-up into a design system, an alignment check, then hand-off and a pixel compare against the real app.
---

# Designr
Design in rounds, in one interactive HTML mockup. You make real options. The user picks and writes feedback. You lock the picks. The locked mockup becomes the spec, then the design system, then the app.

## Where to start
| Situation | Step |
|---|---|
| New app, screen, flow or redesign | 1 |
| The user sends picks or feedback on a mockup | 3 |
| The design is cluttered: too many sizes, colours, controls | 4 |
| Build or change UI in a project that has a locked design | 6 |
| Check a built screen against the design | 7 |

## Steps
1. Brief
    - Read the current UI, its theme code and earlier mockups or design docs. Take screenshots of the current app.
    - Ask only what changes the work: platform, window size, the screens, references the user likes.
    - Make a list of decisions: each element that has more than one good answer.
2. Mockup (rules: [references/mockup.md](references/mockup.md), start file: [templates/mockup.html](templates/mockup.html))
    - One self-contained HTML file: `design/mockup-vN/index.html`. The real app at real size on the left, the picker on the right.
    - Every option works in the mockup. A description is not an option.
    - Give 2 to 5 options per decision. The first option is your recommendation.
    - Tell the user how to open it (`open design/mockup-vN/index.html`) and what to look at.
3. Round
    - The user clicks through, picks, and pastes the "Copy my picks" text with notes.
    - Lock the picks: update `LOCKED` and the round section in `DECISIONS.md` ([templates/DECISIONS.md](templates/DECISIONS.md)).
    - Make new decisions only from the feedback. Quote the feedback word for word in the decision.
    - Fix bugs the user found without a decision. Write them under "Fixed without a decision".
    - Commit the round. Repeat until nothing is open.
4. Clean-up into a design system
    - Turn on the counter. It shows the text sizes, colours and weights on screen.
    - Offer a clean-up decision with real options, for example "3 sizes only", "one text size in panels", "two greys".
    - After the lock, write the design system as one block in `DECISIONS.md`: surfaces, text sizes, text colours, one control per job, heights, icon buttons, radii, spacing.
    - Add a "Design system" scene that shows every token. Add a Before / After switch (B) between the last round and the clean-up.
5. Alignment
    - Press G in each scene. Fix every red box (an item 1 to 5 px off a shared edge).
    - Write the result under "Alignment check" in `DECISIONS.md`.
6. Hand-off and build (format: [references/design-system.md](references/design-system.md))
    - Write the design system files: `design-system/README.md`, `foundations.md`, `components.md`. Take values from the mockup CSS and `DECISIONS.md` only.
    - Map each token to the code (theme file, colour, font, padding). Name the files to change.
    - Build from tokens only. If a value is missing, ask. Do not invent it.
7. Verify (details: [references/verify.md](references/verify.md))
    - Render each mockup scene and the same app state with the same demo data. Compare them side by side.
    - Run the project checks in `design-system/README.md`.

## Rules
- The mockup wins. If a text and the mockup disagree, the mockup is right.
- A locked pick stays locked. Reopen it only when the user asks. Keep old options behind "Unlock to compare".
- Each round changes only what the feedback names. Do not redesign locked parts.
- Name a decision by what the user sees ("Events I have not accepted"), not by code.
- Invent all demo data. Use reserved domains (`example.com`, `example.org`). Use no real people or companies.
- A big change of direction gets a new folder `mockup-vN+1`. Mark the old design docs as superseded. Keep them.
- Content first. Chrome steps back: grey icons, sentence-case labels, no box in a box.
- One value per job. Few sizes, few colours, one control per job.

## Project files
| File | Contents |
|---|---|
| `design/mockup-vN/index.html` | The mockup with the picker. `LOCKED`, `DECISIONS`, `SCENES` at the top of the script. |
| `design/mockup-vN/DECISIONS.md` | Every lock by round, replaced picks, fixes, the design system, the alignment result. |
| `design-system/` | `README.md`, `foundations.md`, `components.md` (format in [references/design-system.md](references/design-system.md)). |
| `design/mockup-vN/shots/` | PNG per scene, for the pixel compare. |

## Check list before you hand a round to the user
- [ ] Every open decision has 2 to 5 working options, a quote of the feedback and a scene.
- [ ] Hover on an option shows it and outlines what changes.
- [ ] Every option has a "?" text that says what it does.
- [ ] `LOCKED` and `DECISIONS.md` agree.
- [ ] G shows no red box in the scenes you changed.
- [ ] The file opens from disk with no server and no console error.
- [ ] Your message says the round number, what is open and which scene to look at.
