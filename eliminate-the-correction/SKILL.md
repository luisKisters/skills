---
name: eliminate-the-correction
description: Turn a correction of the agent into a permanent fix, using the value ladder architecture, then lint rule or test, then skill or rule file, then human review as the last resort. Use when the user corrects the agent, says "I told you this before", "you keep doing that", "stop doing X", "don't do that again", "make sure this never happens again", or asks to prevent a mistake from recurring, to make a fix permanent, to add a guardrail, or to write a rule, hook, lint rule, or regression test after a mistake.
---

# Eliminate the Correction

Every human correction of an agent is a defect in the environment, not only in the output. Fix the output, then remove the class of mistake so nobody has to catch it again.

Order of value:

1. Categorically eliminate the problem through better architecture or data structures.
2. Turn it into a lint rule or test, so CI catches it.
3. Turn it into a skill or rule.
4. Have humans review the code to catch it. This one fails at scale.

Always climb from rung 1 down. Take the highest rung that really works. Do not stop at rung 3 because it is easy.

## 1. Fix what the user asked for first

Apply the correction itself. The prevention work never delays the fix the user wanted.

## 2. Name the class

State the class in one sentence: what the agent did, and what it should do instead. Do this before choosing a rung.

Then check the class is real:

- Has this, or something like it, happened before? Search the repository and past rules for existing partial guards.
- Is it a rule, or a taste call for one file? A one-off preference gets no guardrail. Say so and stop.
- Would the guard fire on correct code? A guard with false positives gets disabled and protects nothing.

## 3. Rung 1: make the mistake impossible

Ask whether the code can be shaped so the mistake cannot be expressed.

- Illegal state that a type or schema can forbid.
- A branded or newtype value instead of a bare string or number, for example `UserId` instead of `string`.
- One chokepoint function or module instead of the same logic copied to each call site.
- A required parameter instead of a defaulted one that is easy to forget.
- Deleting the unsafe path completely, so only the safe path remains.

This rung costs the most and is worth the most. If it fits the change budget, propose it, with the size, and let the user decide.

## 4. Rung 2: make CI catch it

If the mistake stays expressible, make the machine reject it.

- A regression test that fails on the exact mistake. It must fail before the fix and pass after it. Prove both.
- A lint rule: an existing ESLint, Ruff, or Clippy rule turned on, or a small custom rule.
- A type-check, schema-validation, or build step in the pipeline.
- A pre-commit or `PreToolUse` hook when the mistake is a command or an edit, not a code shape.

Wire it into CI. A check that runs only on request is rung 4 with extra steps.

## 5. Rung 3: write the rule down

Only when rungs 1 and 2 cannot cover it, write it for the agent.

- Repeats in this repository: add it to `AGENTS.md` or `CLAUDE.md`, near related rules.
- Repeats everywhere: add it to the global agent instructions.
- A whole workflow, not one line: write a skill.

Keep it short, imperative, and testable: "Use `trash <path>`, never `rm`." Edit the existing rule instead of adding a near-duplicate. Rule files that grow past reading length stop working, so every addition must earn its lines.

## 6. Rung 4: human review

This is the failure case, not a plan. Use it only as a temporary measure while a higher rung is being built, and say when the real guard lands.

## 7. Report

Give the user, in a few lines:

- The class you named.
- The rung you took, and why the rungs above it did not fit.
- The proof: the failing-then-passing test, the lint run, or the file and lines you changed.
- Anything left for the user to do, such as enabling a CI check.

## Anti-patterns

- Adding a rule line for every small correction, until the rule file is unreadable.
- Writing a rule when a type or a test would have settled it.
- Claiming a guardrail without running it.
- A test that passes both before and after the fix.
- Guarding one call site when the same mistake is available at ten others.
