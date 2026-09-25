---
name: satire-supercut
description: Use when the user asks for a YTP, YouTube Poop, supercut, sentence-mix, parody edit, or "make <creator> say <thing>" video built only from a creator's real footage. Builds a short, dry, clearly labeled satire video where every word is really spoken by the creator: it indexes their auto-captions, finds exact phrases, downloads only the needed clip sections, finds clean cut points with ASR word timings plus an audio energy profile, burns in captions and a "parody" tag, and verifies the final cut by transcribing it. Also use when the user wants to fix leaked or dropped words at splice points in such an edit.
---

# Satire Supercut

Make a short parody video in which a creator "says" a new script. Every word comes
from their own footage. The result is satire and must look like satire.

## Rules

- **Satire, clearly labeled.** Every frame carries a `parody` tag (build.py adds it).
  The post that shares it says it is a parody/YTP. Never produce a cut that a viewer
  could mistake for a real statement.
- **Absurd, not believable.** The joke must be obviously false (for example "I'm paid
  by China", "today's sponsor is Jira"). Do not fabricate plausible accusations,
  crimes, slurs, health claims, or anything that could hurt the person if clipped
  out of context. If the user asks for that, say no and offer a sillier line.
- **Only real words.** Every caption word must exist in the audio. No TTS, no voice
  cloning, no pitch or speed tricks.
- **Dry style by default.** Hard cuts, captions, the creator's own audio. No cards,
  freeze frames, zooms, drones, or sound effects unless the user asks.
- **Natural pauses only.** A beat is a real silent moment from their footage
  (`silences.py`), never a frozen frame or inserted silence.
- **Pacing.** Do not repeat the punchline word twice in a row. Let the setup breathe
  and put the pause right before the reveal.
- Keep downloads small: auto-captions first, then only the clip sections you use.

## Tools

Needs: `uv`/`uvx`, `ffmpeg`, `node` (yt-dlp JS runtime), and a word-timing ASR.
The scripts use `spokenly transcribe file X --format json`; swap in any ASR that
outputs `segments: [{text,start,end}]` per word. Scripts live in `scripts/`; run them
from one working directory.

| Script | Purpose |
|---|---|
| `fetch.sh subs <channel-url> [n]` | Auto-captions of the last n uploads into `subs/` |
| `index.py` | Build `words.json` (video, start, end, word) |
| `find.py "phrase" ...` | Exact phrase hits with timestamps |
| `context.py "phrase"` | Hits with surrounding words (check meaning and speaker) |
| `fetch.sh clip <id> <s> <e>` | Download a section to `raw/<id>_<s>.mp4` + word timings |
| `words.py <clip>` | Print ASR word timings of a clip |
| `energy.py <clip>,<s>,<e>` | RMS every 40 ms; cut inside valleys |
| `silences.py` | Silences >= 0.5 s in all clips (natural pauses) |
| `check.py "clip,s,e;clip,s,e"` | Splice and transcribe to verify a line |
| `build.py cuts.txt out.mp4` | Render with captions + parody tag, hard cuts |

`examples/theo-cuts.txt` is a finished 28-line cut to copy the style from.

## Steps

1. **Get the premise.** One plot in 4-6 beats, with a twist near the end (for
   example: paid shill for A -> B pays more -> someone calls it out -> sponsor list of
   things they hate -> secret love). Done when the user approves the beats.
2. **Index the words.** `fetch.sh subs` for the creator's channel (and podcasts or
   second channels they appear on; check the speaker there), then `index.py`.
   Done when `words.json` exists.
3. **Write the script from real phrases.** For each line, use `find.py` for long
   exact phrases first, then splice shorter ones. Prefer whole natural phrases over
   single-word splices: they sound better and are funnier. Write `script.md` with
   one caption line per numbered row and show it to the user before rendering.
   Done when every word has a hit and the user agrees.
4. **Download sections.** `fetch.sh clip` with ~3 s padding around each hit.
5. **Find exact cut points.** `words.py` gives rough times (often 0.1-0.3 s off).
   Confirm with `energy.py`: start and end inside a low-energy valley. Check every
   line with `check.py`. Fix leaks ("that Anthropic") by moving the start later and
   dropped syllables ("thropic") by moving it earlier, in 0.05-0.1 s steps. Done
   when `check.py` prints exactly the caption for every line.
6. **Add pauses.** Pick a real silent moment from `silences.py` (face on screen,
   mouth closed) and append it to the setup line before a reveal.
7. **Render.** Write `cuts.txt` (`caption | clip,s,e ; clip,s,e`) and run
   `uv run scripts/build.py cuts.txt out.mp4`.
8. **Verify the whole video.** Transcribe `out.mp4` and compare it with
   `script.md` line by line. Make a contact sheet
   (`ffmpeg -i out.mp4 -vf "fps=1/2,scale=320:-1,tile=5x5" sheet.png`) and check
   that the creator's face is visible and captions are readable. Done when the
   transcript matches, except for known ASR quirks you list for the user.
9. **Share.** Hand over the file path. If the user wants a post, write it in their
   voice and make the parody label explicit (for example "ytp", "satire", "every
   word is real, the context is not").

## Do not

- Do not remove the parody tag or strip the label from the post.
- Do not upload or post anywhere without the user's explicit go.
- Do not keep a line whose speaker you cannot confirm (co-hosts, guests).
