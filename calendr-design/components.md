# Components and patterns
Each spec uses the tokens and styles in `foundations.md`. Sizes are in points.
## Segmented control
One control for Day/Week/Month, Going? and the settings switches. Swift: one `Segmented` in `Components.swift`.
| Part | Spec |
|---|---|
| Frame | field material: no fill, 1 px inset `hair2`, padding 2, radius 8 |
| Segment | height 22, padding 0 10, radius 6, `label-11.5`, `fg2` |
| Selected | `thumb` fill, `fg`, strong |
| Hover (not selected) | `hover` fill, `fg` |
## Button
| Variant | Fill | Text | Note |
|---|---|---|---|
| Default | `bg2` | `label-12.5`, `fg` | Hover 12 % brighter |
| Primary | `act` | `label-12.5` strong, `onAct` | Hover 8 % brighter |
| Ghost | none | `fg2` | Hover: `hover` fill, `fg` |
| Destructive | danger `#D9645A` | strong, white | |
| Split (Send) | `act` | strong, `onAct` | Chevron part 32 wide, 1 px divider `onAct` 25 % |
| Join | `act` | strong, `onAct` | Full width, content centred |

- Size: height 32, padding 0 12, radius 8. Small: height 28, padding 0 10, `label-11.5`.
- Icon button: 26 with a 16 icon, or 22 with a 14 icon. Radius 6. Icon `fg3`. Hover: `hover` fill, `fg`.
## Field
| Part | Spec |
|---|---|
| Field, search | height 32, field material, padding 0 12 (search: icon, gap 8) |
| Inline field (panel) | radius 6, padding 3 8, margin −3 −8, so it bleeds 8 px |
| Hover | `hover` fill |
| Focus | `bg` fill, 1.5 px inset `fg3` |
| Placeholder | `fg3`. Empty fields always show, with a placeholder. |
| Switch (All day) | track 26 × 15, radius 8, `bg3`; on `act`. Knob 11, `fg2`; on `onAct` |
## Row
| Kind | Height | Spec |
|---|---|---|
| List, menu, sidebar | 28 | Radius 6, `hover` on hover and for the selected row |
| Panel | min 32 | Icon `fg3` in the icon column, text on the text column, gap 12 |
| Later (right column) | 28 | Time 40 wide `label-11.5` `fg2`, bar 3 × 14 radius 2, title `label-12.5` with an ellipsis, gap 8 |
| Sidebar calendar | 28 | Checkbox 14 radius 4, gap 10, `label-11.5` |
## Menu and dialog
| Part | Spec |
|---|---|
| Menu | menu material, padding 6 |
| Item | min height 28, padding 4 10, gap 10, radius 6, check column 14. Hover `hover`. |
| Section label | `label-11.5-strong`, padding 8 10 4 |
| Separator | 1 px `hair`, margin 6 4 |
| Danger item | text `#E5776C` |
| Dialog | modal material, width 520. Title `heading-18`. Text `copy-12.5` `fg2`. Buttons at the right, gap 8. |
| Calendar menu | width 224, account name without the domain, swatches in 6 columns of 20, radius 6 |
## Event block
| Part | Spec |
|---|---|
| Box | radius 6, padding 4 7 4 10 |
| Bar | 3 wide, inset 3 from left, top and bottom, radius 2 |
| Text | title `event-11.5`, time `label-11.5` tabular |
| Position | left = lane + 2 + indent; width = lane − 5 − indent; top + 1; height = duration − 2, min 18 |
| On top of another (cut) | 1.5 px `bg` ring |
| Selected | 1.5 px `bg` ring, then 3 px `fg` |
| Hover | 12 % brighter |

Text rules:
- The title always starts at the top. Only a one-line block under 22 is centred.
- Height under 30: one line, title then start time.
- Height under 52: the title has 1 line, so the time shows. Else 2 lines.
- Width under 56: one line with an ellipsis. A narrow one-line block hides the time.
- Show the range "14:00–16:00" only if width − 17 ≥ 62. Else show the start time.
- Hyphenate long words at syllables. Never break inside a word.

All-day item: height 18, radius 6, padding 0 7 0 10, the same bar. Two rows, then "+N more". Expanded: a fixed height that scrolls.
Reminders and 0-min items: a small block, not a pill.
## Reply states
`fill` = mix(bg, cc, .34).
| State | Fill | Bar | Title | Time | Extra |
|---|---|---|---|---|---|
| Going | `fill` | `cc` | `fg` | `fg2` | |
| Past | `fillPast` | `barPast` | `fg2` | `fg3` | |
| Not answered | `bg` | `cc` | `fg` | `fg2` | 1 px solid `outline` |
| Maybe | stripes 135°: 6 px `fill`, 6 px mix(fill, bg, .45) | `cc` | `fg` | `fg2` | |
| Declined | mix(bg, fill, .38), solid | `cc` at 45 % | `fg3`, struck | `fg3`, struck | Never see-through |
## Overlap layout
Smart cascade with 2 lanes. Source: `layoutDay()` in `index.html`.
1. Sort by start, then the longer event first.
2. An event that starts 30 min or more after the group under it cascades: one level up, 14 px more indent, the rest of the width.
3. Events that start within 30 min of each other share the width equally.
4. At most 2 events are side by side at one time. The next one goes into "+N".
5. Declined and not-answered events take the right half, on top. Accepted events keep the left half. If they start within 30 min, the accepted event narrows to the left half.
6. Two unaccepted events at the same time: the later one goes into "+N".
7. A short item (task, 0 min) takes the right half. In the first 30 min of a block it takes the right third, and the block narrows to two thirds.

"+N" chip: height 16, min width 22, padding 0 5, radius 8, `bg3`, `fg`, `label-11.5` strong, 3 from the right, 1.5 px `bg` ring. Hover or open: `fg` fill, `bg` text.

Stack panel ("+N" opens it):
- menu material, padding 4, gap 3. Over the day at the busy time. Width = 2 day columns − 8. Left edge 2 inside the day. It flips left at the window edge.
- One full-width row per event of the busy time, in time order.
- Row: columns 76 / 1fr / auto, gap 8, min height 28, padding 4 8 4 12, radius 6, event fill and bar (inset 4 top and bottom).
- Row text: time `label-11.5`, title `event-11.5` with an ellipsis, reply "maybe", "no reply" or "declined" in `fg3`. The reply states apply.
## Participant row
One line per person: reply mark, name, role in grey. No pictures.
| Part | Spec |
|---|---|
| Row | min height 28, padding 2 0 2 8, margin left −8, gap 8, radius 6 |
| Reply mark | 14 × 14: going check 12 `#3FA45B`, maybe question 12 `#D9A33A`, declined x 11 `#E5776C`, no reply clock 12 `fg3` |
| Name | `label-12.5` `fg`, ellipsis |
| Role | `label-11.5` `fg3`: "organizer", "you", "optional", joined with " · " |
| Not sent yet | 7 px `fg2` dot at the end. Removed: name struck, `fg3`. |
| Hover | Row actions at the end: 22 icon buttons, 14 icons |
| My row, expanded | `Segmented`: Going · Maybe · Decline |

Bare addresses get names from Apple Contacts, then Google contacts. Without access, show "N without a name · Allow Contacts".
## Alignment
- Event panel: padding 12 14 16 20. Icon column 20–36 (16 icon). Text column at 48. Line box 20; secondary lines 16.
- Fields, inputs and hover boxes bleed 8 px. Text stays on the text column.
- Reply marks start on the text column. Text after a 14 px mark starts after an 8 px gap.
- Right column: box edge 8, content edge 20, for search, cards, rows and shortcuts.
- Sidebar: leading glyphs at 16, text at 40, trailing buttons end at 220. Row icons 14.
- Week grid: gutter 58, so a day column is 118 and hairlines fall on whole pixels. Hour labels end 8 from the gutter edge.
- Day labels and all-day text start on the event text line: 12 inside the day column.
- Menus from the right column end 8 left of it. Menus under a field start their text on the field text.
- Calendar menu headers and swatches start at the colour dot.
## Do and avoid
| Do | Avoid |
|---|---|
| Use a token or a style name | A hex, font size or radius number in a view |
| Instrument Sans for `heading-18` only | Instrument Sans for small text |
| A reply mark before the name | Avatars or pictures in participant rows |
| Solid, muted declined events | See-through declined events |
| 2 lanes, then "+N" | 3 or more events side by side |
| Sentence-case labels, grey key hints | Capitals, key boxes, panel separators, a Today frame |
| `live` red for now only | `live` red for errors or emphasis |
| One `Segmented` type | A second segmented or tab control |
