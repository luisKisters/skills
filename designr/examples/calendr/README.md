# Calendr design system (example)
A filled example of the format. Calendr is a native macOS calendar app in SwiftUI. Values come from the Calendr v4 mockup. The style and material names only name locked values.
## Sources
Order of authority. If two sources disagree, the first wins.
1. `design/mockup-v4/DECISIONS.md`: locked decisions and the design system.
2. `design/mockup-v4/index.html`: the `LOCKED` object, the `.ds` CSS, `themeVars()`, `evVars()`, `layoutDay()` and the "Design system" scene.
3. `design/mockup-v4/IMPLEMENTATION-PLAN.md`: phases, files and target Swift names.
## Principles
1. Content first. Events, names and times stand out. Icons, key hints and labels step back to `fg3`.
2. One value per job. 3 text sizes, 2 weights, 3 text colours, 2 row heights, 3 radii, 5 spacing steps.
3. Colour is data. Calendar colours belong to events. `act` is for the primary action and today. `live` is for now.
4. Space before boxes. No box in a box. No panel separators. No capitals in labels.
5. Every edge is on a column. Hover boxes bleed 8 px, so the text does not move.
## Check
- Open `index.html`, select the scene, press G. There are no red boxes.
- Run `scripts/verify.sh` and `scripts/snapshots.sh`. Compare the snapshot with the scene.
- No hex literal, font size or radius number in `Sources/Calendr/Views` outside `Theme.swift`.
