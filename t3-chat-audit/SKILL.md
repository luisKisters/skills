---
name: t3-chat-audit
description: Audits all active T3 Code chats from the local state database, classifies which are safe to archive, and archives only the chats the user approved. Use when the user asks to look through, tidy, prune, or archive their T3 Code chats or threads, asks which chats are not needed anymore, wants a stale-chat report with reasons, or asks to bulk archive old chats. The audit is read-only; archiving happens only after the user approves an explicit list.
---

# T3 Chat Audit and Archive

## Data source

All thread state lives in one SQLite file: `~/.t3/userdata/state.sqlite`.
Read it with the `sqlite3` CLI. The T3 Code server reads the same tables, so a
precise `UPDATE` on `projection_threads.archived_at` shows up in the app UI.

Relevant tables and columns:

- `projection_projects`: `project_id`, `title`
- `projection_threads`: `thread_id`, `project_id`, `title`,
  `latest_user_message_at`, `updated_at`, `archived_at`, `deleted_at`,
  `pending_approval_count`, `pending_user_input_count`,
  `has_actionable_proposed_plan`, `pinned_at`
- `projection_thread_pull_requests`: `thread_id`, `url`

## Step 1: Run the audit (read-only)

From this skill directory run:

    sqlite3 -header ~/.t3/userdata/state.sqlite < scripts/audit.sql

The query returns one row per active chat with its project, last user message
time, linked pull request count, and the pending-work counters. Use these
columns, not the UI, as the truth.

## Step 2: Classify

Mark as archive candidates:

- Test threads, greetings, and chats that never got real work.
- Throwaway titles that name no concrete task.
- One-off Q&A probes whose answer is already applied or irrelevant.
- Completed one-off chores with no follow-up dependency.
- Duplicates: same or near-same title and project with close timestamps.
  Keep the newest copy. Propose the older copies only when the newest copy
  clearly contains the finished result.

Keep:

- Chats with activity in the last 10 days.
- Ongoing product work: dashboards, benchmarks, migrations, release trains.
- Task handoffs and anything linked to a pull request.
- Chats whose titles are too vague to judge; ask the user instead of guessing.

## Step 3: Apply hard safety gates

Put a chat on the archive list only when every gate holds:

- `deleted_at IS NULL`
- no row in `projection_thread_pull_requests` for that thread
- `pending_approval_count = 0`
- `pending_user_input_count = 0`
- `has_actionable_proposed_plan = 0`
- `pinned_at IS NULL`
- the user explicitly approved this chat after seeing the proposal

When a gate fails or the classification is uncertain, leave the chat out and
say the reason in one line.

## Step 4: Propose before any write

Present a table with chat title, project, date, and one-line reason. The user
must approve the exact list. Archiving without approval is a hard error.

## Step 5: Archive approved chats

1. Back up the database:
   `cp ~/.t3/userdata/state.sqlite ~/.t3/userdata/state.sqlite.bak-archive-<YYYYMMDD>`
2. Build a `VALUES` list of `(project_id, last_user_message_timestamp)` pairs,
   or `thread_id` pairs when already known, for approved chats only.
3. Preview the join with a `SELECT`; it must return exactly the approved
   chats, no more and no fewer.
4. Run the `UPDATE`:

        WITH targets(project_id, ts) AS (VALUES
          ('<project-uuid>','<timestamp>'),
          ('<project-uuid>','<timestamp>')
        )
        UPDATE projection_threads SET archived_at = '<now-utc>'
        WHERE thread_id IN (
          SELECT t.thread_id FROM projection_threads t
          JOIN targets ON targets.project_id = t.project_id
            AND COALESCE(t.latest_user_message_at, t.updated_at) = targets.ts
          WHERE t.deleted_at IS NULL AND t.archived_at IS NULL
        );

5. `SELECT changes();` must equal the approved count.
6. Verify with counts: archived rows equal the approved count, and the
   remaining active-chat count dropped by the same amount.

## Step 6: Rollback

Set `archived_at = NULL` for the affected `thread_id`s. A full restore means
copying the backup file over `state.sqlite` while the T3 Code app is closed.

## Rules

- Never run `DELETE`, never write `deleted_at`, and never write to message,
  activity, or turn tables.
- Never include chat titles, project names, or other database contents in
  commits, reports for other tools, or anything that leaves the machine.
- Assume the T3 Code app is running. Use short statements; never lock the
  database file or pause the server.
