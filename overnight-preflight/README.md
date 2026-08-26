# overnight-preflight

Proves a repository can run unattended before you walk away, and tells you only the
things you genuinely have to decide first.

## What it does

Probes every external dependency once, for real: the toolchain, a real build, one
real round trip to every model or API with the credential the code actually uses,
OS permissions, disk, sleep settings and push access. It never prompts, never uses
`sudo`, and puts a timeout on every command.

Each result is OK, DEGRADED (broken but worked around) or BLOCKED (a human must
act). It ends with a short list of decisions only the owner can make — credentials,
money, taste, and steps that need a person present. It deliberately does not ask
about speculative risks.

## When it triggers

When you are about to leave an agent running overnight or for hours, say you are
going to sleep, ask whether anything will interrupt a long autonomous run, worry
about password prompts or expired tokens, ask for a readiness check, or hand a long
task to subagents.

## Install

```
npx skills add github.com/luisKisters/skills --skill overnight-preflight
```
