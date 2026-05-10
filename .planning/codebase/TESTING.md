# Testing And Verification

**Updated:** 2026-05-10

## Automated Tests

No automated test framework is currently established.

Observed:

- No `test` script in `package.json`.
- No detected frontend `*.test.*` / `*.spec.*` files.
- `api/test.py` is a manual Chroma inspection script, not a test suite.
- No pytest config or dedicated backend test directory detected.

## Available Checks

Use these for first-slice verification:

```bash
npm run build
npm run lint
```

Caveat:

- `npm run lint` uses `next lint`, which may be stale with Next 15.
- If lint fails because the command is removed/deprecated, record the blocker instead of expanding scope.

## Static Checks For Phase 1

Search for active blockers:

```bash
rg "127.0.0.1:8000|your-aws-lambda-url|Chatbot|Proxy" app
```

Expected after execution:

- `app/page.tsx` should not import `Chatbot` or `Proxy`.
- No first-slice UI path should post to `http://127.0.0.1:8000/chat`.
- Stale `app/api/chat.ts` should be deleted or clearly sidelined.

## Verification Artifact

After execution, write:

- `.planning/current/VERIFY.md`

Include:

- commands run,
- pass/fail status,
- exact errors,
- accepted known blockers,
- manual review notes.
