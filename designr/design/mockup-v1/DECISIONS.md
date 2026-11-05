# designr v1 decisions
Superseded by `design/mockup-v2/` (round 3, the final version). Kept as the record of rounds 1 and 2.
Mockup: `design/mockup-v1/index.html`. The picker shows the same state.
## Locked in round 1
| Element | Pick |
| --- | --- |
| How hovering an option shows it | Short pause, then show; stays while you move inside a decision |
| When the option is on another screen | Jump to that screen while hovering |
| How the change appears | Short crossfade (140 ms) |
| How it marks what changes | A short glow, then nothing |
| Where the picker sits | Sidebar on the right |
| How options look | Radio list |
| How you go through the decisions | All open decisions in one list |
| How you give feedback | Copy my picks, write notes in the chat |
## Added in round 2
- Agentation (agentation.com) in the mockup: ⌘⇧F, click an element, write a note. The user asked for it ("hau noch agentation rein").
- Its notes go into "Copy my picks" under "Notes on elements", with the scene, the CSS path and the element text.
- It loads from esm.sh. Without the network the mockup works, without Agentation.
## Ported to the template
`templates/mockup.html` now has the round 1 picks and Agentation:
- Hover intent: 90 ms in, 140 ms out, the gaps inside one decision keep the preview.
- A hover preview renders only the app, never the picker.
- A 140 ms crossfade on hover previews, and a short glow on the `hl` elements.
