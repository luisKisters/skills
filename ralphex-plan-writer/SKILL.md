---
name: ralphex-plan-writer
description: Creates verification-first Ralphex/executr-compatible Markdown implementation plans, planned in HTML first and converted to Markdown for execution. Use when the user asks to make a Ralfex/Ralfax/Ralphex/executr-compatible plan, convert a brainstorming note or PRD into docs/plans tasks, plan a UI change with mockups, engineer an autonomous-agent verification loop, or prepare a plan for the executr reaper.
---

# Ralphex Plan Writer

Plans written here are executed by the `orchestrated-build` skill. Write for that executor.

## 1. Scale gate: decide how much plan the change earns

Do this before writing anything. Getting it wrong in either direction is expensive.

| Change | What it gets |
| --- | --- |
| Bugfix, copy change, anything inside one file | No plan. Say so and stop. |
| New screen or endpoint | Mockups or `/grill-me`, a short plan, one review phase |
| Large feature, migration, shared core | The full plan below |

Size and blast radius decide, not habit. One exception overrides the table: if code quality has to hold, because a team ships production code on top of this, run the full pipeline everywhere including the small things. Ask which case applies when it is not obvious.

If the request is tier 1, tell the user a plan is not worth it and offer to do the change directly instead.

## 2. Preflight

Confirm the executor has:

- orchestration tools, an end-to-end test runner, and a CLI for every external system in scope
- prefer CLIs. If a connected MCP already covers the job, use it instead of asking for a CLI
- missing tool: give the user the exact install command. Never use computer-use to install
- needs auth: offer to open the browser at the right page so the user only approves and pastes back a device code

Do not plan work for a system the agent cannot reach or verify end to end.

## 3. Read local execution rules

1. Target repo `AGENTS.md`, `CLAUDE.md`, and the docs its router table points at.
2. Target repo `.ralphex/config` and `.ralphex/prompts/task.txt` when present.
3. The parked-ideas file, if one exists, so a rejected proposal is not planned again.
4. If the repo requires current docs for CLIs or libraries, obey that rule before relying on memory.

## 4. Plan in HTML, then convert to Markdown

HTML is for anything a person reads. Markdown is what the agent executes and is cheap in context.

**For UI work**, generate the interface before writing the spec:

1. Load a design skill that builds a design system first. Screens without one look individually invented.
2. Ask for 2 to 5 standalone HTML mockups per screen.
3. Collect feedback per element, not per screen, then regenerate.
4. Write the decisions the agent may not revisit into a locked list, explicitly, for example "two action buttons".
5. Repeat per screen until each has a winner.
6. Precedence rule to carry into the plan: when a written rule and a mockup disagree, the mockup wins.

**For everything else**, scope by interrogation with `/grill-me` until the feature is actually defined. This is the cheapest step in the pipeline and the one most often skipped.

**Then** refine an HTML plan document until it is right, and only after that convert it into one clear Markdown plan. Splitting plans into folders is unnecessary until they get very large; the model reads only the relevant part anyway.

## 5. Write the verification before the code exists

Ask what the agent must be able to observe to know it is correct, and add early tasks for the missing seams. Otherwise the tests end up fitting the code instead of the intent.

Plan against three layers:

| Layer | Proves | Typical tooling |
| --- | --- | --- |
| 1 Unit | One function: input x, output y | The project test runner |
| 2 Deterministic end to end | A scripted path, identical every run | Playwright, XCUITest |
| 3 User-like end to end | An agent uses the app like a person | agent-browser, Codex computer use |

Layer 3 is where the remaining bugs are, because unit tests cannot reproduce user behaviour. Prefer agent-browser over the Chrome DevTools MCP: it is a CLI, and agents handle CLIs measurably better.

**The agent login route is usually the first harness task.** agent-browser runs headless, headless is what you want on a server, and Google and Microsoft block headless logins. Plan an auth route reachable only in a dev environment, guarded by a long password, leading into a test account with test data. It never exists in production and real authentication stays untouched. Add a task asserting it returns 404 in production.

Other seams worth their own early task:

- fixture creation and cleanup commands
- server authorization matrix tests
- browser flows proving both owner and anonymous views
- screenshots or accessibility snapshots for responsive UI
- external-provider mocks, plus one explicit smoke test when appropriate

## 6. Plan shape

```md
# Feature Name

## Overview
Short feature goal and rollout shape.

## Context
Facts from the repo and source note.

## Product Decisions
Locked decisions the executor must not reopen. Include the mockup-wins precedence rule.

## Architecture Decisions
Concrete implementation direction.

## Models
Orchestrator, supervising subagent, and implementing subagent for this plan.

## Verification Contract
How the agent can prove the work without fake success. Name the stop points.

## Validation Commands
- `pnpm exec tsc --noEmit`
- `pnpm build`
- `pnpm test`

## Phase 1: Slice Name
### Task 1: First Executable Slice
- [ ] Do one coherent iteration.
- [ ] Add or update tests.
- [ ] Run relevant validation.

## Phase 2: Review
### Task 2: Review Pass
- [ ] Delete code that is bad, not best practice, or never asked for.
- [ ] Cut redundant tests; keep one per acceptance criterion.

## Phase 3: End-to-End
### Task 3: Full Product Run
- [ ] Run the whole product against the real interfaces named above.
- [ ] Fix only what the run breaks.
```

## 7. Phases

- One phase = one vertical slice = one feature cut through backend, frontend, and database or external API, independently testable.
- Plan all slice phases first. Then exactly one review phase. Then exactly one end-to-end phase, at the end and nowhere else.
- **Review comes before the end-to-end phase, and the order is deliberate.** Review changes functionality, so the changed functionality is what has to be tested afterwards. Run end to end first and you have proven a version of the code the review then edits.
- Review phase standing order: remove unnecessary code and unnecessary tests. Scrutinize tests hardest. Correct tests, not many.
- Claude models do the review. GPT models produce far more code than asked for, even when prompted against it. Do not plan Codex for review.
- Keep the reviewer credential free. A reviewer that can change the pipeline it is judged by is not a reviewer.
- Keep `### Task N:` numbering global and sequential across phases.

## 8. Models

Name the models in the plan. Default fleet:

| Role | Model and level |
| --- | --- |
| Plans and decides | Fable 5 high, or Opus 5 high |
| Supervises a slice | Opus 5 low subagent |
| Implements | Luna Max subagents, through the Codex plugin |

- **Fan-out gate: roughly 50 changed lines.** Below it the work stays in the main thread, because the orchestration overhead costs more than it saves. This is a rule of thumb, not a measured result. Say so in the plan.
- Luna implements because it is by far the most cost efficient model. Its weaker code quality is what the review phase exists for.
- Claude-only environment: Fable 5 high orchestrates Opus 5 low subagents through Claude Workflows.
- Codex-only environment: Sol high orchestrates Luna Max subagents.
- Never plan a reasoning level above high. Above high the models overengineer: bigger solutions, more tests than asked for, aggressive fixing of things nobody wanted touched. Luna is the exception, because max is its normal working mode.
- Never plan Sonnet 5. It is worse than Opus 5 low in every category and costs more.

## 9. Shipping expectations the plan must state

- The agent runs the fast local suite while it works, then the full suite and the pre-push verification script before pushing.
- It pushes a draft pull request with the evidence attached: screenshots or video per verification step, a video walkthrough for UI work.
- The pull request stays a draft until a human approves it. No automated approval counts.
- Validation is bound to the exact head commit. A new commit invalidates the previous evidence.
- UI changes always carry evidence in the pull request itself.

## 10. Repository documentation

If the target repo has no router, add a task for it: `AGENTS.md` holds a table of every document and what it owns, with the rule that every new uppercase file under `docs/` belongs in that table. Reads are triggered by events, not loaded by default.

## 11. Ralphex rules

- Test-driven, but plan the smallest test set that proves the slice.
- If a task loops or grows more complex than the goal needs, stop and reflect before continuing.
- Store executable plans under `docs/plans/*.md` unless the repo config says otherwise.
- Include `## Validation Commands`.
- Use task headings exactly like `### Task N:` or `### Iteration N:`. Number from 1.
- Use `- [ ]` checkboxes only inside task sections. Never in Overview, Context, Success Criteria, or any other non-task section.
- Keep each task self-contained for one fresh agent turn.
- End every implementation task with validation commands and, for user-visible behavior, browser verification.
- Prefer minimal implementations. Do not plan new architectural layers, broad abstractions, major rewrites, or subsystem splits unless the user explicitly approved that complexity.
- Prefer deterministic local tests over real external services. If a real smoke test is necessary, make it best-effort and require the executor to record exact blockers instead of pretending success.

## 12. Validate and hand off

Run `python3 <skill-dir>/scripts/check_plan_format.py <plan.md>` before handing the plan back.

When presenting a finished plan, summarize:

- where the plan file was written
- the locked decisions
- the verification harness work, including the agent login route if it was needed
- the exact format check that passed

If the user approves, ask: "Should I push this plan to `main` so executr/Ralphex can pick it up?"
