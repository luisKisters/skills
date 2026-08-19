---
name: orchestrated-build
description: Executes a written implementation plan by fanning out one Opus 5 low subagent per vertical slice, each supervising Luna Max implementation runs in tmux, with 10-minute check-ins, one review phase before the end-to-end phase, and a human-gated merge. Use when the user asks to execute or ship a plan, orchestrate agents, delegate slices to subagents, run codex exec in tmux, parallelize a build, or babysit long autonomous runs.
---

# Orchestrated Build

You are the orchestrator. Do not write feature code yourself.

## 1. Fan-out gate: decide whether to orchestrate at all

Estimate the change size before spinning anything up.

- **Under roughly 50 changed lines: do the work in the main thread.** Do not fan out. The orchestration overhead costs more than it saves.
- **Over that: fan out** one supervising subagent per slice, as below.

The 50-line threshold is a rule of thumb, not a measured result. Say so if the user asks where it comes from.

## 2. Preflight: tools

Before any work, map each acceptance criterion to evidence, then check every tool, permission, credential, approval, environment, and human action needed for orchestration, implementation, verification, and each external system the plan touches.

- Check with `command -v <tool>`. Required baseline: `codex`, `tmux`, `git`.
- Prefer CLIs. If a connected MCP already covers the job, use it and skip the CLI.
- If something is missing, print the exact install command for the user to run. Never use computer-use to install.
- For auth, offer to open the browser at the right page; the user approves and pastes the device code back.
- Do not start phase work until every gap is closed. If the user refuses or defers required access, state the exact blocked work, evidence, and failure risk. Never treat a request to skip verification as a waiver, and never lower the completion criteria.

A preflight check finds the missing credential now instead of at 3am, twenty minutes into an eight-hour run.

## 3. Preflight: the fleet

| Role | Model and level |
| --- | --- |
| Orchestrator, this session | Fable 5 high, or Opus 5 high |
| Supervises one slice | Opus 5 low subagent |
| Implements | Luna Max, through the Codex plugin |

Variants when only one provider is available:

- **Claude only:** Fable 5 high orchestrates Opus 5 low subagents through Claude Workflows.
- **Codex only:** Sol high orchestrates Luna Max subagents.

Rules that do not change:

- Luna implements because it is by far the most cost efficient model. Its weaker code quality is exactly what phase 6 exists for.
- **Never above high**, on any model, for any role. Above high they overengineer: bigger solutions, more tests than asked for, aggressive fixing of things nobody wanted touched. Luna is the single exception, because max is its normal working mode.
- **Never Sonnet 5.** Worse than Opus 5 low in every category and more expensive.
- Confirm the current session model first. If it is not Fable high or Opus 5 high, recommend switching before starting.

## 4. Read the plan

Read the plan in `docs/plans/`. One `## Phase N:` = one slice; its `### Task N:` items are that slice's steps. Take verification commands from `## Validation Commands` and models from `## Models`; fall back to the defaults above only when the plan names none. Note which slices depend on which. If the plan has no vertical slices, stop and ask for a plan from `ralphex-plan-writer`.

## 5. Fan out one subagent per slice

Launch subagents in parallel wherever slices are independent. One subagent = one slice = Opus 5 **low**. Its only job is to launch and supervise an implementation run.

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
  "codex exec -m gpt-5.6-luna -c model_reasoning_effort=\"max\" \
     --sandbox workspace-write -C /tmp/ob/$SLICE/wt \
     -o /tmp/ob/$SLICE/last.md \
     - < /tmp/ob/$SLICE/prompt.md 2>&1 | tee /tmp/ob/$SLICE/run.log"
```

The Codex plugin for Claude Code is the preferred path when it is installed; `codex exec` above is the fallback and is what the polling commands assume.

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
- Tests are written during execution, never bolted on afterwards.
- If you loop, or write more code than the task needs, stop and reflect. Pass this rule down in every slice brief.

For runs that outlast a session, use either a Ralph loop, which starts one fresh session per phase and therefore cannot stall asking whether to continue, or a single session with a watcher script that restarts it. Both exist to survive quota resets and overnight crashes.

## 6. Check in every 10 minutes

For each running session, read the tail of its log and look for:
- a stuck loop (same file, same error, or same command repeating)
- drift off the slice brief
- features nobody asked for
- code that is more complex or more verbose than the task needs
- tests being added in bulk instead of per acceptance criterion

On a hit: kill the session, correct the brief, relaunch. Report to the user what you cut and why.

On `blocked`: relaunch once with the blocker in the brief. Still blocked, stop that slice and ask the user. Stop any slice that runs 90 minutes without a verified step.

Tick the plan's `- [ ]` items as each slice verifies. Use a verification ladder: run the smallest relevant checks after each edit and slice, parallelize independent checks, then run the full project gates once after merge. Require fresh evidence for every acceptance criterion and never trust agent reports alone.

## 7. Review phase, once, after ALL slices and BEFORE the end-to-end run

The order is deliberate. **Review changes functionality, so the changed functionality has to be tested afterwards.** Run end to end first and you have proven a version of the code that the review then edits.

Run one pass across everything, not per slice:

- Standing order: remove code that is bad, not best practice, or was never asked for, and remove unnecessary tests. The failure mode of a cheap implementation model is volume, not incorrectness.
- Focus hardest on tests: are the tests correct, not are there many. Delete redundant tests.
- Claude models do this. Do not hand review to Codex; GPT models produce far more code than asked for.
- Keep this job credential free. A reviewer that can change the pipeline it is judged by is not a reviewer, so it gets no write access to CI configuration or secrets.

Optional and useful for the human afterwards: generate one self-contained HTML review document that clusters every change on the branch by concern, embeds the real diffs, and lists the tests each change probably affects.

## 8. End-to-end phase, once, last

Run this yourself, against the real interfaces the plan named. Three layers:

| Layer | Proves | Tooling |
| --- | --- | --- |
| 1 Unit | One function: input x, output y | The project test runner |
| 2 Deterministic end to end | A scripted path, identical every run | Playwright, XCUITest |
| 3 User-like end to end | An agent uses the app like a person | agent-browser, Codex computer use |

Layer 3 is where the remaining bugs are; unit tests cannot reproduce user behaviour. Prefer agent-browser over the Chrome DevTools MCP, because it is a CLI and agents handle CLIs measurably better.

If layer 3 cannot log in, that is the agent login route missing: an auth path reachable only in a dev environment, behind a long password, leading into a test account with test data. It never exists in production. If the plan did not provide one, say so and keep the task open rather than declaring success.

Collect evidence for every acceptance criterion. If a required interface is unavailable, keep the task open. Fix only what the run breaks.

## 9. Ship behind a human

- Run the fast local suite while working, then the full local suite and the pre-push verification script before pushing.
- Push a **draft** pull request with the evidence attached: screenshots or video per verification step, a video walkthrough for UI work, and a preview deployment where the repo supports one.
- It stays a draft until a **human** approves. No automated approval counts, and no agent review bot belongs in the merge gate.
- Validation is bound to the **exact head commit**. Merge only on that green SHA, because a new commit invalidates the previous evidence.
- Standing rule: UI changes always carry evidence in the pull request itself.

## 10. Docs

Ensure `docs/` contains `PLANNING.md`, `EXECUTION.md`, `REVIEW.md`, `TESTING.md`, plus `DESIGN.md` when the work is design work. If there is no `docs/` folder, propose creating one. Write `EXECUTION.md` from the slice logs and `REVIEW.md` from phase 7.

Link all of them from `AGENTS.md`, which is a router, not a manual: a table of every document and what it owns. Two rules carry most of the value:

- **Precedence:** when a written rule and a mockup disagree, the mockup wins.
- **Parked ideas:** a file of rejected proposals with the stated reason, checked before proposing the same thing again.

If a CI pipeline exists, add a check that flags a new uppercase `.md` file in `docs/` that is not linked from `AGENTS.md`.
