# Verify the app against the mockup
The mockup is the spec. Prove the app matches it, scene by scene, with the same data.

## Set up once
1. Shots of the mockup: render each scene to `design/mockup-vN/shots/<scene>.png`.
    - Web: Playwright with `file://.../index.html#<scene>&shot`, wait for `document.fonts.ready`, crop to `DESK`.
    - macOS without Node: a small Swift script with `WKWebView` and a non-persistent data store, so `LOCKED` applies.
    - Optional `js` per scene to open a menu before the shot.
2. The same demo data in the app: port the mockup's demo data into a fixture, with a fixed "now". Add a launch flag, for example `--fixture vN`.
3. Snapshots of the app: a flag or test that renders a named state to PNG at the same size, for example `App --snapshot <state> --out <png>`.
4. A map of states: `design/states.json` with `state`, `mockup` (scene), `js`, `fixture`, `size` per entry.
5. A compare script: mockup, app and difference side by side per state, and a mean-difference score in a JSON report. It is a report, not a gate.

## Each change
- Render the changed states. Look at the triptych. Fix what differs.
- Open the scene in the mockup and press G. The app must keep the same edges.
- Check the code: no colour, font size, radius or spacing literal in the views outside the theme file.
- Run the checks in `design-system/README.md`.

## Tests that keep it true
- Every `states.json` entry has a snapshot hook. Every `mockup` entry has a shot file.
- The fixture has the mockup counts (events, rows, items) and the edge cases of each scene.
- Pure layout logic (for example overlap or column layout) gets unit tests with the scene data.
