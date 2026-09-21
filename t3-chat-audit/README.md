# t3-chat-audit

This skill audits every active T3 Code chat straight from the local
`state.sqlite` database, classifies which chats are safe to archive (junk,
tests, greetings, duplicates, finished one-offs), applies hard safety gates
(no linked pull requests, no pending approvals, inputs, or open plans, not
pinned), and archives only the chats the user approved.

Install: `npx skills add github.com/luisKisters/skills --skill t3-chat-audit`
