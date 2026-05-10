# Concerns

**Updated:** 2026-05-10

## Highest Priority

### Legacy browser-to-localhost chat path

- Files: `app/components/Chatbot.tsx`, `app/components/Proxy.tsx`.
- Problem: browser posts directly to `http://127.0.0.1:8000/chat`.
- Impact: deployed app cannot work reliably and bypasses any future web boundary.
- Fix: remove from first screen; later replace with a deliberate BFF/API adapter.

### Invalid/stale API route

- File: `app/api/chat.ts`.
- Problem: Pages Router handler shape inside App Router tree plus placeholder AWS URL.
- Impact: misleading path; future agent may treat it as real.
- Fix: delete or replace later with `app/api/chat/route.ts` when chat returns.

### Duplicate legacy chat UI

- Files: `app/components/Chatbot.tsx`, `app/components/Proxy.tsx`.
- Problem: duplicate large components have drifted.
- Impact: high maintenance cost and unclear source of truth.
- Fix: sideline/delete duplicate during first slice.

## Repo Hygiene

### Committed generated artifacts

- Files: `api/__pycache__/`, `chroma_storage/`.
- Impact: noisy repo and machine-specific state.
- Fix: defer cleanup unless it blocks build/checks.

### Split backend dependencies

- Files: `requirements.txt`, `api/requirements.txt`.
- Impact: setup ambiguity.
- Fix: defer until backend phase.

## Product Risk

### Rebuilding the old chatbot by accident

- Problem: old code pulls attention toward chat before source trust exists.
- Impact: product remains generic assistant instead of grounded personal workspace.
- Fix: first slice must show sources, ingest, notes, and chat as one workspace.

## Check Gate

First execution should only touch the minimal UI/planning files needed to prove the shell and remove active first-slice blockers.
