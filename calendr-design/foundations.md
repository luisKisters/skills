# Foundations
Theme: OLED black with the ink accent. Only the dark theme is locked. Light mode keeps the current Paper values in `Theme.swift`. Do not invent light values.

`mix(a, b, t)` moves colour `a` the fraction `t` toward `b`. "fg 6.5 %" is `fg` at 6.5 % opacity.

Column "Swift": the current name, and "→" the v4 target. The targets come from Phase 1 of `IMPLEMENTATION-PLAN.md`.
## Colours
Backgrounds
| Token | Value | Use | Swift |
|---|---|---|---|
| `bg` | `#000000` | App, sidebar, right column, unfilled events | `Theme.bg` → `#000000` |
| `bg1` | `#0A0A0A` | Second background. Use it rarely. | `Theme.bg1` |
| `pop` | `#0C0C0C` | Menus, dialogs, toasts, stack panel | → new `Theme.pop` |

Fills
| Token | Value | Use | Swift |
|---|---|---|---|
| `hover` | fg 5.5 % | Hover, selected row | `Theme.hover` |
| `bg2` | `#141414` | Buttons, raised controls | `Theme.bg2` |
| `bg3` | `#1F1F1F` | Switch track, "+N" chip | `Theme.bg3` |
| `thumb` | mix(bg3, fg, .08) = `#303030` | Selected segment | `Theme.thumb` → `#303030` |

Borders
| Token | Value | Use | Swift |
|---|---|---|---|
| `hair` | fg 6.5 % | Grid lines, column edges, separators | `Theme.hair` |
| `hair2` | fg 13 % | Control frames, menu and dialog border | `Theme.hair2` |
| focus | 1.5 px `fg3` | Focused field | `Theme.focus` → `fg3` |
| selection | 1.5 px `bg`, then 3 px `fg` | Selected event | `Theme.ring` → `fg` |

Text and icons
| Token | Value | Use | Swift |
|---|---|---|---|
| `fg` | `#F2F2F2` | Content: titles, names, places, the selected option | `Theme.fg` |
| `fg2` | `#A0A0A0` | Secondary: times, addresses, counts | `Theme.fg2` |
| `fg3` | `#6A6A6A` | Labels, hints, placeholders, icons | `Theme.fg3` |

Accent and state
| Token | Value | Use | Swift |
|---|---|---|---|
| `act` / `onAct` | = `fg` / = `bg` | Primary button, Join, switch on, today pill | `Theme.act`, `Theme.onAct` |
| `live` | `#FF453A` | Now line, now label, countdown. Nothing else. | `Theme.live` |
| `scrim` | black 50 % | Behind dialogs | `Theme.scrim` |
| danger | `#D9645A` fill, `#E5776C` text | Destructive button, danger menu item | → add `Theme.danger*` |
| reply | going `#3FA45B`, maybe `#D9A33A`, declined `#E5776C`, none `fg3` | Reply marks | → add `Theme.reply*` |

Event colours. `cc` is the calendar colour. Code: `Palettes.palette` (`Theme.swift`), `EventPainter` (`EventsCanvas.swift`).
| Token | Formula | `#5B8DEF` gives | Swift |
|---|---|---|---|
| `bar` | `cc` | `#5B8DEF` | `barRGB` |
| `fill` | mix(bg, cc, .34) | `#1F3051` | `fillRGB` (.17) → .34 |
| `fillPast` | mix(bg, cc, .15) | `#0E1524` | `pastFillRGB` (.08) → .15 |
| `barPast` | mix(bg, cc, .32) | `#1D2D4C` | → add |
| `outline` | mix(bg, cc, .75) | `#446AB3` | → add |
| title, time | `fg`, `fg2` (past: `fg2`, `fg3`) | | `titleRGB`, `timeRGB` (tinted) → `fg`, `fg2` |

Calendar swatches, 6 columns: Tomato `#D9443A`, Flamingo `#C9736A`, Tangerine `#F2884B`, Banana `#F2C94C`, Sage `#5FB97E`, Mint `#9BD9C0`, Peacock `#5DADE2`, Blueberry `#5B8DEF`, Lavender `#A9A6F5`, Grape `#9254DE`, Graphite `#B9B9B9`.
## Typography
Text face: SF Pro (system font). Title face: Instrument Sans (`Resources/Fonts/InstrumentSans.ttf`, `Typeface.swift`).
| Style | Face | Size / weight / line | Use | Swift |
|---|---|---|---|---|
| `heading-18` | Instrument Sans | 18 / 600, tracking −0.015 em | Month header, event title, Today, dialog title | `.calTitle` (22) → `Font.ui(18, .semibold)` |
| `label-12.5` | SF Pro | 12.5 / 400 / 20 | Rows, fields, menus, buttons | `.calBody` (13) → `.system(size: 12.5)` |
| `copy-12.5` | SF Pro | 12.5 / 400 / 1.5 | Notes, dialog text | `.system(size: 12.5)` + line spacing |
| `label-11.5` | SF Pro | 11.5 / 400 / 16 | Times, addresses, roles, segments, hour labels | `.calMeta` → `.system(size: 11.5)` |
| `label-11.5-strong` | SF Pro | 11.5 / 600, `fg3` | Section labels, sentence case | `MicroLabel` (10.5 caps) → this |
| `event-11.5` | SF Pro | 11.5 / 500 / 1.25 | Event titles, all-day items | `TextCache` kinds → `.system(size: 11.5, weight: .medium)` |

- Strong: 600 on any style. Use it for the selected segment and the primary button.
- Tabular: every time, date and count. SwiftUI `.monospacedDigit()`. CoreText `NSFont.monospacedDigitSystemFont`.
- Remove the sizes 22, 16, 13 and 10.5.
## Materials
Presets for fill, stroke, radius and shadow.

On the page
| Material | Fill | Stroke | Radius | Use |
|---|---|---|---|---|
| base | `bg` | 1 px `hair` at column edges | 0 | Window, sidebar, right column |
| raised | `bg2` | none | 8 | Buttons |
| field | none | 1 px inset `hair2` | 8 | Fields, search, segmented frame |
| group | none | 1 px `hair2` | 12 | Settings groups |

Above the page
| Material | Fill | Stroke | Radius | Shadow | Use |
|---|---|---|---|---|---|
| menu | `pop` | 1 px `hair2` | 12 | 0 22 60, black 50 % | Menus, popovers, stack panel |
| modal | `pop` | 1 px `hair2` | 12 | 0 30 80, black 55 %, `scrim` | Dialogs |
| toast | `pop` | 1 px `hair2` | 12 | 0 20 60, black 50 % | Toasts |

Today cards in the right column have no fill and no frame. Swift: `popShadow()` in `Theme.swift`; remove `Radius.surface + 2` in `Overlays.swift`.
## Layout
| Group | Values | Swift |
|---|---|---|
| Spacing | 4, 8, 12, 16, 24 | → new `enum Space` |
| Row height | 28: list, menu and sidebar rows, small buttons | → `Dim.row` |
| Control height | 32: panel rows, buttons, fields, search | → `Dim.field` |
| Icon button | 26 with a 16 icon (panel, header); 22 with a 14 icon (sidebar, rows) | `IconButton` → `Dim.iconButton`, `Dim.iconButtonSmall` |
| Radius | 6 rows, events, icon buttons, segments | `Radius.row` 7 → 6, `Radius.event` 6 |
| Radius | 8 buttons, fields, segmented controls | `Radius.control` 7 → 8 |
| Radius | 12 menus, dialogs, groups | `Radius.surface` 12 |
| Chevron | 12 px | |
| Window | sidebar 236, right column 320, header 60, day header 38, hour gutter 58 | `Dim.*` (`hourGutter` 56 → 58) |
## Files to change
| File | What |
|---|---|
| `Views/Theme.swift` | Colours, `pop`, `thumb`, `Dim`, `Radius`, `Space`, `Palettes`, `MicroLabel` |
| `Views/Typeface.swift` | Text styles: SF Pro for text, Instrument Sans for 18 only |
| `Views/Components.swift` | `Segmented`, `IconButton`, `PrimaryButton`, `SecondaryButton`, `Keycap` (no box), `Hairline` |
| `Views/PanelControls.swift` | Remove `PanelRSVP` and `panelThumb`. Use `Segmented`. |
| `Views/CenterView.swift` | `ViewTabs` becomes `Segmented` |
| `Views/Overlays.swift` | Menu and modal materials, settings switches as `Segmented` |
| `Views/EventsCanvas.swift`, `EventViews.swift` | `EventPainter.Ink` from `Theme`, reply states, text rules |
| `Views/DayHeaderView.swift` | `AllDayPainter` items, today pill |
| Other views | Styles, radii, heights, alignment |
