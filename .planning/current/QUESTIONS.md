# Questions

## Blocking Execution

None. The first slice can execute after user approval.

## Decision Before Execution

- Keep current uncommitted `app/page.tsx` / `app/layout.tsx` changes as the baseline, or reset and recreate the shell from the plan?

## Later Questions

- First real ingestion input: manual paste, YouTube URL, or file upload?
- First persistence layer: local JSON/SQLite, Supabase, or Postgres?
- When chat returns, should the boundary be Next.js route/BFF first?
