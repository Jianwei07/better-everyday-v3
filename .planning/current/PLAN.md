# Current Plan: Workspace Shell Pivot

## Goal

Revive Better Everyday by replacing the stale chat-first product shape with a minimal personal source workspace shell.

## Scope

First slice only. Static/web shell. No backend wiring.

## Must Haves

- Homepage presents Better Everyday as a personal source workspace.
- Sources, ingest, notes, and chat are visible as first-class surfaces.
- Paste/transcript ingestion placeholder exists.
- Domains are visible: health, self-help, AI.
- Chat is clearly grounded/future-facing, not the whole product.
- No active first-slice UI path posts to `http://127.0.0.1:8000/chat`.

## Tasks For Execution Later

### Task 1: Confirm existing uncommitted UI baseline

Files:

- `app/page.tsx`
- `app/layout.tsx`

Action:

- Review existing uncommitted changes.
- Keep them if they already satisfy the workspace shell requirements.
- Otherwise replace with the smallest static shell that does.

Verify:

- `app/page.tsx` does not import `Chatbot` or `Proxy`.
- Page copy mentions sources/ingest/notes/chat.

### Task 2: Sideline stale first-slice blockers

Files:

- `app/components/Chatbot.tsx`
- `app/components/Proxy.tsx`
- `app/api/chat.ts`

Action:

- Delete or clearly sideline files that make the first slice look like the old chatbot path.
- Prefer deletion if not imported.
- Do not add a new backend API in this slice.

Verify:

```bash
rg "127.0.0.1:8000|your-aws-lambda-url|Chatbot|Proxy" app
```

Expected:

- No active page import or first-slice route relies on those legacy paths.

### Task 3: Run available checks

Commands:

```bash
npm run build
npm run lint
```

Expected:

- Build passes, or exact blocker is recorded.
- Lint passes, or stale `next lint` blocker is recorded.

### Task 4: Record verification

File:

- `.planning/current/VERIFY.md`

Action:

- Record commands, results, known blockers, and manual acceptance notes.

## Non-Goals

- No Supabase/Postgres/vector migration.
- No auth.
- No YouTube ingestion automation.
- No production RAG.
- No copied skills harness.
- No design system expansion.

## Done Criteria

- App opens to workspace-first shell.
- Legacy chatbot no longer controls first screen.
- First-slice UI is backend-independent.
- Verification artifact exists.
