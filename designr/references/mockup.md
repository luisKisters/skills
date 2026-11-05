# The round mockup
One HTML file per design version: `design/mockup-vN/index.html`. Start from [../templates/mockup.html](../templates/mockup.html). Replace the app part. Keep the picker part.

## File
- One file. Inline CSS and JS. No build, no server. It opens from disk.
- Fonts by relative path to the repo (for example `../../Sources/App/Fonts/`), or system fonts.
- Picks and toggles persist in `localStorage` under one key per version. "Reset demo data" makes the demo data new.
- `#scene` in the URL opens a scene. `#scene&shot` hides the picker at scale 1, for screenshot scripts.

## The app part (left)
- The real window at real size (`DESK`), scaled to fit. The app then grows to fill the stage, so there is no empty space. Shots keep the exact `DESK` size. For a Mac app, add the macOS menu bar if the app uses it. Mark OS chrome with `data-os`, so the counter skips it.
- It works like the app: clicks, menus, fields, keys, empty states. The user tests the flow, not a picture.
- Demo data is invented and realistic: real-length names, long titles, busy days, edge cases.
- Each scene is a start state that shows one problem. Name it by what the user sees ("Busy evening", "Delete with guests").
- Tokens are CSS variables on `.desk`. App CSS uses only tokens. An option changes a class on `.desk` or a branch in `app()`, read with `C(id)`.
- Each area that has its own columns gets `data-area` (sidebar, header, panel, menu, dialog). Centred items get `data-centred`.
- Add a "Design system" scene when the clean-up round starts. It shows every token with its value.

## The picker part (right)
| Part | Rule |
|---|---|
| Title | `Product vN · round N`, then how many decisions are open. |
| How to | 2 to 4 lines: what is clickable, the keys. |
| Before / After (B) | Shows the last round against the change. Values in `BEFORE`. Only when a round changes many things at once. |
| Jump to | One button per scene. |
| Design read | The one-line read and dials from tasteskill, in `READ`. Empty hides it. |
| Preview on hover | On by default. After 90 ms on an option, it applies and its scene opens. Leaving goes back to the pick and to the scene you were on; a click keeps both. The app crossfades in 140 ms and the `hl` elements glow once. The gaps inside one decision keep the preview; leaving the decision restores the pick after 140 ms. Only the app renders again, never the picker, so nothing under the mouse moves. |
| Counter | Text sizes, text colours and weights in view. Use it to argue for a clean-up. |
| Alignment guides (G) | Green: a left edge that 3 or more items share. Blue: a shared right edge. Red box: 1 to 5 px off a line, with the offset. `window.__guides` holds the misses for scripts. |
| Open | One block per open decision: name, "You said: <quote>", where to look, the options. First option tagged "recommended". |
| Locked | A one-line summary per lock. "Unlock to compare" shows the old options again. A changed lock says "changed". |
| Notes on elements (Agentation) | A toggle, on by default ([agentation.com](https://www.agentation.com)). Turning it on opens the toolbar at the bottom right of the app; later ⌘⇧F opens it. Click an element, write a note. The notes go into the picks text under "Notes on elements". It loads from esm.sh; without the network the toggle says so and the mockup works without it. While the toolbar is open, a click on the app makes a note, not an app click. |
| Foot | Copy my picks, Back to locked picks, Reset demo data, and the picks text. |

## A decision
```js
{ g: 'Round 2', id: 'overlap', name: 'Overlapping events',
  fb: 'Slight overlaps look good. Heavy overlaps look weird.',   // the user's words
  note: 'Wednesday 17:00 to 21:30 is the hard case.',             // where to look
  scene: 'overlap', hl: '.day .ev',                               // what opens and what is outlined
  opts: [['smart', 'Smart: cascade; side by side if they start within 30 min', 'Help text for ?'],
         ['columns', 'Side by side only', '...']] }
```
- `lock: true` after the user picks. The value moves into `LOCKED`.
- Labels say the result, not the code: "Right half, on top", not "z-index 4".
- The `?` text says what changes and where, in 1 to 3 sentences.
- Give options that differ in kind, not 3 shades of one idea. Include the current state when it helps ("Round 2, no clean-up").
- Name the round of an older option in its label when you keep it for comparison ("(round 3)").

## Picks text
"Copy my picks" gives the text the user pastes back:
```
# Product v1 round 2 picks
## Open
- List rows: Hairline between rows (not the recommendation)
## Locked
- Accent: Ink
## Notes on elements
- Home · `#desk > .main[data-area="main"] > .row[data-open="1"]` ("Quarterly plan"): the rows feel too tall
## Notes
- less grey
```
Read a note on an element with its scene: open the scene, find the element by the CSS path.
