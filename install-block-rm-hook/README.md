# Install Block rm Hook

This skill installs and verifies a global Claude Code `PreToolUse` hook. The hook blocks direct calls to `rm` and tells the agent to use `trash <path>` instead. It permits `git rm` and the `rm` subcommands of npm, yarn, and pnpm.

It triggers when a user asks to block `rm` in Claude Code, add the guard to another machine, repair the hook, or verify that the guard works.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill install-block-rm-hook
```
