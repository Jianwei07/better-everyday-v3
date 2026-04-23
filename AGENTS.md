<!-- GSD:project-start source:PROJECT.md -->
## Project

Better Everyday is a personal web app that turns YouTube transcripts and personal notes into a grounded AI research workspace for daily use.

Core value: grounded recall from personally curated sources so the assistant gives trustworthy answers that are actually useful every day.

Current project direction:
- Rebuild the legacy app instead of lightly patching it
- Stay web-only for v1
- Keep v1 personal-first with no family accounts
- Start agent-style behavior in ingestion workflows
- Improve trust and grounding before broader coaching behavior
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Current brownfield stack:
- Next.js + React + TypeScript frontend
- FastAPI + Python backend
- Chroma-based retrieval and local/model-server generation

Target direction from research:
- Next.js-first browser boundary / BFF
- Supabase Postgres + `pgvector` for durable app state and retrieval
- Drizzle ORM for schema and migrations
- Vercel AI SDK for chat/model abstraction
- Small Python worker for ingestion and offline ML utilities only

Prefer efficient, low-cost, low-ops choices. Favor smaller models plus strong retrieval over heavier always-on local compute.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

- Preserve existing file-local formatting instead of forcing a repo-wide style shift.
- Keep semicolon style in `app/` and config files; keep no-semicolon style in shadcn files under `src/components/ui/` and `src/lib/utils.ts`.
- Use the `@/*` alias for frontend imports rooted at `src/`.
- Keep TypeScript strict and avoid `any` unless there is a concrete need.
- Follow current naming patterns: PascalCase for React components/types, camelCase for frontend variables/functions, snake_case for Python modules/functions, and UPPER_SNAKE_CASE for backend constants.
- Add tests when introducing behavior changes. The current repo has major testing gaps, so new work should improve regression coverage instead of extending the gap.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Current brownfield architecture is a split Next.js frontend and FastAPI backend with retrieval handled through Chroma and model-server calls.

Project-specific architecture guidance:
- Phase 1 is boundary repair first. Do not preserve the current direct browser-to-FastAPI path as the long-term public flow.
- Keep the workspace-first product shape visible in implementation decisions: sources, notes, and chat are all first-class surfaces.
- Treat source knowledge, durable memory, and transient chat context as separate concerns.
- Prefer reviewable ingestion and evidence-backed answers before broader coaching or automation.
- Remove duplicate, legacy, or debug-oriented public paths instead of keeping parallel flows alive.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` file if project-specific capabilities are introduced.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

For this repo specifically:
- Read `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md` before implementation work.
- Treat Phase 1 (`Boundary Repair & Workspace Shell`) as the current focus until planning docs change.
- Do not expand scope into family accounts, native mobile, generic open-web assistant behavior, or broad autonomous agents unless the planning docs are updated.

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` — do not edit manually.
<!-- GSD:profile-end -->
