WITH pr_counts AS (
  SELECT thread_id, COUNT(*) AS prs
  FROM projection_thread_pull_requests
  GROUP BY thread_id
)
SELECT
  p.title AS project,
  t.title AS chat,
  COALESCE(t.latest_user_message_at, t.updated_at) AS last_msg,
  COALESCE(pc.prs, 0) AS linked_prs,
  t.pending_approval_count AS approvals,
  t.pending_user_input_count AS inputs,
  t.has_actionable_proposed_plan AS open_plan,
  t.pinned_at IS NOT NULL AS pinned
FROM projection_threads t
JOIN projection_projects p ON p.project_id = t.project_id
LEFT JOIN pr_counts pc ON pc.thread_id = t.thread_id
WHERE t.archived_at IS NULL
  AND t.deleted_at IS NULL
ORDER BY last_msg DESC;
