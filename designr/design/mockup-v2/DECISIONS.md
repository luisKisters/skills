# designr v2 decisions
Mockup: `design/mockup-v2/index.html`. It is the final designr picker (`templates/mockup.html`) on a sample Tasks app. The Tasks decisions in it are demo data.
## Locked in round 1 (mockup-v1)
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
## Round 3 (final)
Feedback: "das jump to fehlt, ich mag das man vorherige descisions die locked sind so haben kann. und wo is jz agentation? und ich will das man das an und aus machen kann [...] das ? fehlt auch, alignment guides fehlt auch, und ich will das es auch automatisch den tasteskill v2 nutzt um dinge zu designen. mach finale version"
- One picker only. The nested demo designr of mockup-v1 is gone. The final picker has Jump to, the ? help, alignment guides (G), the counter and the Locked block with "Unlock to compare".
- Agentation: a toggle "Notes on elements (Agentation)", on by default. Turning it on opens the toolbar. The toolbar sits at the bottom right of the app, not over the picker. A status line says if it is on, off or did not load.
- Tasteskill v2: designr loads `design-taste-frontend` in the brief and for each option. Its design read shows in the picker (`READ`).
## Fixed without a decision
Round 3:
- Leaving a hover preview that jumped to another scene now goes back to the scene you were on.
- In mockup-v1 the Agentation button sat on the picks text at the bottom right. Nobody could find it.
- A keydown handler failed on events sent to `document`. It now checks the target.
- "ich will nich das der weiße space da is so": the app now grows to fill the stage, with no empty space under it or beside it. Shots keep the exact window size.
## Alignment check
G in Inbox, Settings and Design system: 0 red boxes (`window.__guides` is empty in all three).
