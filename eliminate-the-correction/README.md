# Eliminate the Correction

This skill turns a correction of the agent into a permanent fix. It names the class of mistake, then climbs a value ladder: categorically eliminate it through architecture or data structures, else make CI catch it with a lint rule or regression test, else write it into a skill or rule file, and treat human review as the failure case.

It triggers when a user corrects the agent, says the agent keeps making the same mistake, or asks for a guardrail, rule, hook, lint rule, or regression test so a mistake never happens again.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill eliminate-the-correction
```

If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R eliminate-the-correction ~/.codex/skills/eliminate-the-correction`.
