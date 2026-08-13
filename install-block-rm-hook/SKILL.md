---
name: install-block-rm-hook
description: Install, repair, or verify a user-level Claude Code PreToolUse hook that blocks direct rm commands and tells the agent to use trash instead. Use when a user asks to prevent Claude Code from running rm, add an rm safety guard to ~/.claude/settings.json, copy this protection to another machine, or test an existing block-rm hook. The hook permits git rm and npm, yarn, or pnpm rm commands because those do not directly delete files through the rm executable.
---

# Install Block rm Hook

Install the bundled hook with the bundled installer. Do not rewrite the hook or settings entry by hand.

## Install

Resolve `<skill-dir>` to the directory that contains this `SKILL.md`, then run:

```sh
python3 "<skill-dir>/scripts/install.py"
```

The installer must:

- copy `block-rm.sh` to `~/.claude/hooks/block-rm.sh`;
- make the hook executable;
- preserve all unrelated `~/.claude/settings.json` content;
- add one user-level `PreToolUse` entry with the `Bash` matcher;
- remain idempotent when run more than once.

To install for a different home directory, use `--home <path>`. To inspect changes without writing, use `--dry-run`.

## Verify

Run the deterministic test suite:

```sh
python3 "<skill-dir>/scripts/test_block_rm.py" "$HOME/.claude/hooks/block-rm.sh"
```

Then confirm that Claude Code loads the user hook:

1. Create a uniquely named sentinel file in a temporary directory.
2. Ask a new Claude Code process to invoke Bash with `rm -f <sentinel>`.
3. Confirm the tool call is denied and the sentinel still exists.
4. Move the sentinel and its empty temporary directory to the system trash.

Never use `rm` to clean the verification files. If `trash` is unavailable, keep the files and report the exact paths.

## Remote install

Copy the three bundled scripts to a temporary remote directory. Run `install.py` there with `python3`, then run `test_block_rm.py` against the installed hook. Use the same live verification when Claude Code is available and authenticated on the remote host.
