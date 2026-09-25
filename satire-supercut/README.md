# Satire Supercut

This skill makes a short, clearly labeled parody video (a YTP or sentence-mix supercut) in which a creator "says" a new script built only from their real words. It triggers when a user asks for a YTP, YouTube Poop, supercut, sentence-mix, or "make <creator> say <thing>" edit. It indexes auto-captions, downloads only the needed clip sections, finds clean cut points with ASR word timings and an audio energy profile, burns in captions and a `parody` tag, and verifies the final cut by transcribing it.

This is for satire. Every video carries a parody tag, the jokes must be obviously absurd, and the skill refuses believable fake statements.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill satire-supercut
```

If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R satire-supercut ~/.codex/skills/satire-supercut`.

Needs `uv`, `ffmpeg`, `node`, and a word-timing ASR (the scripts use `spokenly`).
