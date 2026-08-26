---
name: overnight-preflight
description: Proves a repository can run unattended before the user walks away, and surfaces only the decisions a human genuinely must make. Use when the user is about to leave an agent running overnight or for hours, says they are going to sleep, asks whether anything will block or interrupt a long autonomous run, worries about password prompts, expired tokens, missing credentials, permission dialogs or a hung tool, asks for a preflight or readiness check before a long run, or starts an unattended build, migration, batch or loop. Also use before handing a long-running task to subagents.
---

# Overnight Preflight

Run this before any session where nobody will be at the keyboard. It answers one
question: **can this repository run for hours, alone, without stopping?**

The failure it prevents is not a crash. It is a run that spends six hours failing
the same way because a token expired, a model id was rejected, or a dialog nobody
saw was waiting for a click.

## The rule that makes it useful

**Probe the real thing once. Never trust configuration.**

A key that is present is not a key that works. A CLI that is installed is not a
CLI that is logged in. A model named in a config file is not a model the account
may use. One real round trip per external dependency costs seconds and is the only
evidence worth having.

This is not hypothetical. A preflight that only checked "is the CLI installed"
would have passed a repository where every single model call returned
`400 … not supported when using this account`, because the config named a model
the subscription could not use. The round trip caught it in six seconds.

## Hard rules for the check script

1. **Never prompt.** No `sudo`, no interactive tool, no GUI, no dialog. If a
   credential needs an interactive unlock, try it, accept failure, move on.
2. **Time out every command.** macOS has no `timeout`; use the background+kill
   helper in `scripts/preflight-template.sh`. A hung tool must not swallow the
   night.
3. **Never write a secret to the repository, a log, or stdout.** Check that a
   credential *works*, print nothing but the verdict.
4. **Prefer a workaround to a stop.** If the configured model is rejected, find one
   that is not and report the override. If a permission is missing, report which
   opt-in tests will skip and let the rest of the run proceed.
5. **Exit non-zero only for a real stop.** A degraded run that still does useful
   work is a success.

## Classify every result

| Class | Meaning | Effect |
|---|---|---|
| **OK** | Probed, works | Silent |
| **DEGRADED** | Broken, but worked around | Listed, run continues |
| **BLOCKED** | A human must act | Listed, exit 1 |

Plus one separate list: **decisions only the owner can make.**

## What counts as a decision — and what does not

This is the part agents get wrong. Do **not** ask about anything speculative.
"This might fail" is not a decision. Ask only when one of these is true:

- **A credential or permission only a human can grant.** An API key, an OS
  permission dialog, a login.
- **Money or an irreversible, outward-facing action.** Spending, publishing,
  pushing, deleting, sending.
- **Taste the agent is not allowed to judge.** Approving a visual baseline,
  choosing a product direction.
- **A step that structurally requires the human's presence.** "Use the app for 20
  minutes", "record real samples from your own work."

Do **not** ask about:

- Anything with a sane default the agent can pick and state.
- Risks the agent invented while imagining what could go wrong.
- Choices already implied by what the user asked for.
- Anything the agent can simply probe and find out.

One line per decision, phrased as the action the user takes, not as a worry.

## What to check

Adapt to the repository; these are the ones that actually stop runs.

- **Toolchain** — the exact compiler/SDK the scripts assume, not just "a compiler".
- **A real build** — before anything else, because nothing else matters if it fails.
- **Every external model or API** — one real round trip, with the credential the
  code will actually use, through the same code path.
- **Credentials** — where the code reads them from, in that order. Report the
  source that won.
- **`sudo`** — confirm nothing in the run needs it.
- **Disk** — a run that fills the disk at 3am leaves a broken tree.
- **Sleep** — is the machine allowed to sleep? Name the `caffeinate` wrapper.
- **Push access** — can the agent reach the remote non-interactively?
- **OS permissions** — accessibility, screen recording, automation. Missing ones
  are usually DEGRADED, not BLOCKED: the opt-in tests skip.
- **Tests that take over the screen or input** — say so explicitly. The user
  decides whether that is acceptable tonight.

## How to run it

1. Read the repository's own scripts first. Reuse its gate helper, its environment
   setup and its naming instead of inventing a parallel system.
2. Write `scripts/preflight.sh` from `scripts/preflight-template.sh` in this skill,
   keeping the classification and the timeout helper.
3. Run it. Fix what is fixable in code, then re-run until it is OK or knowingly
   DEGRADED.
4. Report to the user: what you fixed, what is degraded with its workaround, and
   the short list of decisions. Nothing else.
5. Commit the script. A preflight that lives only in a chat log is not a gate.

## Reporting back

Lead with the blocker if there is one. Then the decisions. Keep it to what changes
what the user does in the next two minutes — they are trying to go to sleep.
