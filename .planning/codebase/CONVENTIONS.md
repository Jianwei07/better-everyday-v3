# Conventions

**Updated:** 2026-05-10

## Frontend

- Use TypeScript strict mode.
- Use `@/*` alias for imports rooted at `src/`.
- Keep semicolon style in `app/` and config files.
- Keep no-semicolon style in shadcn files under `src/components/ui/` and `src/lib/utils.ts`.
- Use PascalCase for React component types and component exports.
- Use camelCase for frontend variables/functions.
- Keep first-slice UI static and readable; avoid premature component extraction.

## Backend

- Use snake_case for Python modules/functions.
- Use UPPER_SNAKE_CASE for backend constants/env-backed settings.
- Keep backend route handlers thin; put business logic in modules.
- Do not expose raw/debug output in public paths when backend becomes active.

## Planning

- `.planning/` is project-local workflow state.
- Active work lives under `.planning/current/`.
- Codebase map lives under `.planning/codebase/`.
- Pivot rationale lives under `.planning/pivot/`.
- Do not copy `/Users/jayden77/dev/skills` into this repo.

## Product Scope

- Personal-first.
- Web-only for v1.
- Trust and grounding before coaching.
- Reviewable ingestion before automated agents.
- Delete or sideline legacy code when it blocks the workspace shape.
