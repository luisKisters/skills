---
name: ralphex-plan-writer
description: Creates verification-first Ralphex/executr-compatible Markdown implementation plans with minimal, approval-gated architecture. Use when the user asks to make a Ralfex/Ralfax/Ralphex/executr-compatible plan, convert a brainstorming note or PRD into docs/plans tasks, engineer an autonomous-agent verification loop, or prepare a plan for the executr reaper.
---

# Ralphex Plan Writer

Plans written here are executed by the `orchestrated-build` skill. Write for that executor.

## Preflight

Before drafting, confirm the executor has:

- orchestration tools, end-to-end test runner, and a CLI for every external system in scope
- prefer CLIs; if a connected MCP already covers the job, use it instead of asking for a CLI
- missing tool: give the user the exact install command. Never use computer-use to install
- needs auth: offer to open the browser at the right page so the user only approves and pastes back a device code

Do not plan work for a system the agent cannot reach or verify end to end.

## Workflow

1. Read local execution rules before drafting:
   - target repo `AGENTS.md`, `CLAUDE.md`, and relevant project docs
   - target repo `.ralphex/config` and `.ralphex/prompts/task.txt` when present
2. If the target repo requires current docs for CLIs/libraries, obey that rule before relying on memory.
3. Survey unresolved product or architecture decisions briefly when they affect task boundaries.
4. Prefer the minimal implementation that solves the feature and can be verified.
5. Put harness engineering first when autonomous verification is weak: deterministic fixtures, seed/cleanup commands, auth path, browser state isolation, and non-external test seams.
6. Write the plan as executable work, not prose-only strategy.
7. Validate with `python3 <skill-dir>/scripts/check_plan_format.py <plan.md>` before handing it back.

## Plan Shape

```md
# Feature Name

## Overview
Short feature goal and rollout shape.

## Context
Facts from the repo and source note.

## Product Decisions
Locked decisions the executor must not reopen.

## Architecture Decisions
Concrete implementation direction.

## Models
Orchestrator, subagent, and Codex model for this plan.

## Verification Contract
How the agent can prove the work without fake success.

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

## Phases

- One phase = one vertical slice = one feature cut through backend, frontend, and database or external API, independently testable.
- Plan all slice phases first. Then exactly one review phase. Then exactly one end-to-end phase, at the end and nowhere else.
- Review phase: remove code that is bad, not best practice, or never asked for. Scrutinize tests hardest — correct tests, not many.
- Keep `### Task N:` numbering global and sequential across phases.

## Models

Name the models in the plan. Default: Opus 5 high or Fable high orchestrates, Opus 5 low subagents, `codex exec` gpt-5.6-sol at medium. Codex-only environment: gpt-5.6-sol orchestrates.

## Ralphex Rules

- Test-driven, but plan the smallest test set that proves the slice.
- If a task loops or grows more complex than the goal needs, stop and reflect before continuing.
- Store executable plans under `docs/plans/*.md` unless the repo config says otherwise.
- Include `## Validation Commands`.
- Use task headings exactly like `### Task N:` or `### Iteration N:`.
- Number tasks from 1.
- Use `- [ ]` checkboxes only inside task sections.
- Do not put checkboxes in Overview, Context, Success Criteria, or other non-task sections.
- Keep each task self-contained for one fresh agent turn.
- End every implementation task with validation commands and, for UI/user-visible behavior, browser verification.
- Prefer minimal implementations over complex architecture. Do not plan new architectural layers, broad abstractions, major rewrites, or subsystem splits for a feature or fix unless the user has explicitly approved that complexity.
- Prefer deterministic local tests over real external services. If a real smoke test is necessary, make it best-effort and require the executor to record exact blockers instead of pretending success.

## Verification-First Planning

Before feature work, ask what the agent must be able to observe to know it is correct. Add early tasks for missing seams:

- fixture creation and cleanup
- test users or auth shortcuts
- local-only admin/debug routes guarded by secrets or test identity
- server authorization matrix tests
- browser flows that prove both owner and anonymous/public views
- screenshots or accessibility snapshots for responsive UI
- external-provider mocks and one explicit smoke test when appropriate

## Handoff

When presenting a finished plan, summarize:

- where the plan file was written
- the important locked decisions
- the verification harness work
- the exact format check that passed

If the user approves the plan, ask: "Should I push this plan to `main` so executr/Ralphex can pick it up?"
