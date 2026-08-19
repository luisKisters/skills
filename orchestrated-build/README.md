# Orchestrated Build

This skill executes a written implementation plan with a fleet of agents: one Opus 5 low subagent per vertical slice, each supervising Luna Max implementation runs inside tmux, checked every 10 minutes, then one review phase and one end-to-end phase. An agent triggers it when a user asks to execute or ship a plan, orchestrate or parallelize agents, or run long autonomous builds without losing them when a turn ends.

Two rules shape the skill. Below roughly 50 changed lines it does not fan out at all, because the orchestration overhead costs more than it saves. And review runs before the end-to-end phase, because review changes functionality and that changed functionality is what has to be tested afterwards.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill orchestrated-build
```

If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R orchestrated-build ~/.codex/skills/orchestrated-build`.
