---
name: orchestrated-build
description: Executes a written implementation plan by fanning out one Opus 5 low subagent per vertical slice, each supervising a Codex gpt-5.6-sol run inside tmux, with 10-minute check-ins, one review phase, and one end-to-end phase. Use when the user asks to execute or ship a plan, orchestrate agents, delegate slices to subagents, run codex exec in tmux, parallelize a build, or babysit long autonomous runs.
---

# Orchestrated Build

You are the orchestrator. Do not write feature code yourself.

## 1. Preflight: tools

Before any work, check the tools needed for orchestration, end-to-end testing, and every external system the plan touches (DB, cloud, payment, auth, CI).

- Check with `command -v <tool>`. Required baseline: `codex`, `tmux`, `git`.
- Prefer CLIs. If a connected MCP already covers the job, use it and skip the CLI.
- If something is missing, print the exact install command for the user to run. Never use computer-use to install.
- For auth, offer to open the browser at the right page; the user approves and pastes the device code back.
- Do not start phase work until every gap is closed or the user waives it.

## 2. Preflight: orchestrator model

Confirm the current session model. If it is not Opus 5 at high effort or Fable at high effort, recommend switching first. In a Codex-only environment, gpt-5.6-sol orchestrates instead.

## 3. Read the plan

Read the plan in `docs/plans/`. One `## Phase N:` = one slice; its `### Task N:` items are that slice's steps. Take verification commands from `## Validation Commands` and models from `## Models`; fall back to the defaults above only when the plan names none. Note which slices depend on which. If the plan has no vertical slices, stop and ask for a plan from `ralphex-plan-writer`.

## 4. Fan out one subagent per slice

Launch subagents in parallel wherever slices are independent. One subagent = one slice = Opus 5 **low**. Its only job is to launch and supervise a Codex run.

Give each parallel slice its own `git worktree add /tmp/ob/$SLICE/wt <branch>` and point `-C` at it. Merge into the main branch as each slice lands. Run a dependent slice only after its dependency merges.

Give each subagent this literal shape:

```sh
SLICE=slice-01
mkdir -p /tmp/ob/$SLICE
# brief goes in a file
cat > /tmp/ob/$SLICE/prompt.md <<'EOF'
<slice brief: goal, files, acceptance test, verification command>
EOF

tmux new-session -d -s "$SLICE" \
  "codex exec -m gpt-5.6-sol -c model_reasoning_effort=\"medium\" \
     --sandbox workspace-write -C /tmp/ob/$SLICE/wt \
     -o /tmp/ob/$SLICE/last.md \
     - < /tmp/ob/$SLICE/prompt.md 2>&1 | tee /tmp/ob/$SLICE/run.log"
```

Keep stdout on the pane through `tee`. Redirecting all three fds kills the pane at once, and every slice then reports done instantly.

Poll, never block:

```sh
tmux has-session -t "$SLICE" 2>/dev/null   # exit 0 = still running
tail -n 40 /tmp/ob/$SLICE/run.log
cat /tmp/ob/$SLICE/last.md                 # final message, once the session ends
tmux kill-session -t "$SLICE"              # to stop a runaway
```

Subagent rules:
- Report status as: running / blocked / done + last meaningful action.
- Test-driven, but deliberately few tests. One test per acceptance criterion.
- If you loop, or write more code than the task needs, stop and reflect. Pass this rule down to Codex in every slice brief.

## 5. Check in every 10 minutes

For each running session, read the tail of its log and look for:
- a stuck loop (same file, same error, or same command repeating)
- drift off the slice brief
- features nobody asked for
- code that is more complex or more verbose than the task needs
- tests being added in bulk instead of per acceptance criterion

On a hit: kill the session, correct the brief, relaunch. Report to the user what you cut and why.

On `blocked`: relaunch once with the blocker in the brief. Still blocked, stop that slice and ask the user. Stop any slice that runs 90 minutes without a verified step.

Tick the plan's `- [ ]` items as each slice verifies.

## 6. Review phase (once, after ALL slices)

Run this pass yourself, one pass across everything, not per slice. Remove code that is bad, not best practice, or was never asked for. Focus hardest on tests: are the tests correct, not are there many. Delete redundant tests.

## 7. End-to-end phase (once, last)

Run this yourself: one end-to-end run of the whole product against the real interfaces the plan named. Fix only what it breaks.

## 8. Docs

Ensure `docs/` contains `PLANNING.md`, `EXECUTION.md`, `REVIEW.md`, `TESTING.md`, plus `DESIGN.md` when the work is design work. If there is no `docs/` folder, propose creating one. Write `EXECUTION.md` from the slice logs and `REVIEW.md` from phase 6. Link all of them from `AGENTS.md`. If a CI pipeline exists, add a check that flags a new UPPERCASE `.md` file in `docs/` that is not linked from `AGENTS.md`.
