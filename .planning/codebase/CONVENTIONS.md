# Coding Conventions

**Analysis Date:** 2026-04-21

## Naming Patterns

**Files:**
- Use framework-reserved lowercase route files in `app/layout.tsx`, `app/page.tsx`, and `app/api/chat.ts`.
- Use PascalCase for React component files in `app/components/Chatbot.tsx` and `app/components/Proxy.tsx`.
- Use lowercase UI primitive filenames in `src/components/ui/button.tsx`, `src/components/ui/input.tsx`, `src/components/ui/avatar.tsx`, and `src/components/ui/card.tsx`.
- Use snake_case or simple lowercase module names for Python backend modules such as `api/main.py`, `api/chat.py`, `api/config.py`, and `api/embedding_search.py`.

**Functions:**
- Use camelCase for frontend functions and handlers, such as `sendMessage`, `handleTopicSelect`, `handleBackToMenu`, `handleQuickResponse`, and `toggleExpandChat` in `app/components/Chatbot.tsx`.
- Use snake_case for backend Python functions, such as `call_llm_server`, `self_reflect_on_answer`, `is_generic_or_empty`, `fallback_response`, and `generate_response_with_context` in `api/chat.py`.
- Use PascalCase component function names for exported React components like `RootLayout` in `app/layout.tsx` and `Button` in `src/components/ui/button.tsx`.

**Variables:**
- Use camelCase for frontend state and local variables like `chatHistory`, `selectedTopic`, `chatEndRef`, `chatHeight`, and `quickSelectPrompts` in `app/components/Chatbot.tsx`.
- Use UPPER_SNAKE_CASE for backend constants and env-backed settings like `RAG_PROMPT_TEMPLATE`, `DEFAULT_TIMEOUT`, `HF_TOKEN`, `EMBEDDING_MODEL_NAME`, and `LLM_SERVER_URL` in `api/chat.py` and `api/config.py`.

**Types:**
- Use PascalCase for TypeScript types and interfaces such as `ChatMessage` in `app/components/Chatbot.tsx`, `ButtonProps` in `src/components/ui/button.tsx`, and `InputProps` in `src/components/ui/input.tsx`.
- Use PascalCase for Pydantic request models like `ChatRequest` and `TestRequest` in `api/api.py`.

## Code Style

**Formatting:**
- Prettier or Biome config is not detected in the repository root; formatting is governed by existing file-local style rather than a dedicated formatter config.
- Preserve the semicolon-terminated Next.js style used in `app/layout.tsx`, `app/page.tsx`, `app/components/Chatbot.tsx`, `next.config.js`, and `tailwind.config.js`.
- Preserve the no-semicolon shadcn/ui style used in `src/lib/utils.ts`, `src/components/ui/button.tsx`, `src/components/ui/input.tsx`, `src/components/ui/avatar.tsx`, and `src/components/ui/card.tsx`.
- Use double quotes consistently across both frontend and backend-adjacent JS/TS files, as seen in `app/page.tsx`, `app/components/Chatbot.tsx`, and `src/components/ui/button.tsx`.

**Linting:**
- ESLint is configured through `/.eslintrc.json` with `"extends": "next/core-web-vitals"`.
- The only JavaScript/TypeScript lint command exposed in `package.json` is `npm run lint`, which runs `next lint`.
- TypeScript strict mode is enabled in `tsconfig.json` with `"strict": true`; new TS code should remain type-safe instead of relying on `any`.

## Import Organization

**Order:**
1. Import framework or platform packages first, such as `next`, `react`, `fastapi`, `langchain_core`, and `httpx` in `app/layout.tsx`, `app/components/Chatbot.tsx`, `api/api.py`, and `api/chat.py`.
2. Import internal aliases or local modules next, such as `@/components/ui/*` in `app/components/Chatbot.tsx`, `@/lib/utils` in `src/components/ui/button.tsx`, and sibling Python modules like `from chat import generate_response_with_context` in `api/api.py`.
3. Keep styling side effects adjacent to entry files, such as `import "./globals.css";` in `app/layout.tsx`.

**Path Aliases:**
- Use the `@/*` alias from `tsconfig.json` for frontend imports rooted at `src/`.
- Follow the alias map in `components.json`: `@/components`, `@/components/ui`, `@/lib`, and `@/hooks`.
- Prefer `@/components/ui/*` and `@/lib/utils` over long relative traversals in frontend files, as shown in `app/components/Chatbot.tsx` and `src/components/ui/button.tsx`.

## Error Handling

**Patterns:**
- Wrap async network calls in `try/catch` on the frontend and fall back to user-facing chat messages, as done in `sendMessage` inside `app/components/Chatbot.tsx`.
- Wrap backend route handlers in `try/except` and raise `HTTPException` for API failures, as done in `api/api.py`.
- Return fallback strings instead of propagating raw model errors in `api/chat.py`; examples include timeout and generic failure branches in `call_llm_server` and `generate_response_with_context`.
- Coerce unexpected LLM outputs into safe string values before downstream processing in `api/utils.py` via `extract_eva_response`.

## Logging

**Framework:** print-based logging plus minimal stdlib logging.

**Patterns:**
- `api/main.py` initializes `logging.basicConfig(level=logging.INFO)`, but application-level diagnostics primarily use `print(...)` in `api/chat.py`, `api/api.py`, and `api/utils.py`.
- Keep verbose debug prints close to RAG cleanup and inference code when investigating backend issues, following the existing pattern in `api/utils.py` and `api/chat.py`.
- Frontend components are mostly silent; the only explicit browser logging found is `console.error("Error:", error);` in `app/components/Proxy.tsx`.

## Comments

**When to Comment:**
- Use comments for module boundaries and intent, such as `# NOTE: All prompt and RAG logic is in api/chat.py.` in `api/main.py` and `api/api.py`.
- Use inline comments for debugging rationale and defensive fixes in backend code, as seen in the `CRITICAL FIX` comments in `api/chat.py` and the staged cleanup comments in `api/utils.py`.
- Use UI-focused comments in large frontend files to separate state sections and handler groups, as seen in `app/components/Chatbot.tsx`.

**JSDoc/TSDoc:**
- JSDoc/TSDoc is not a standard pattern in the TypeScript files reviewed.
- Python docstrings are used selectively for public or important functions such as `call_llm_server`, `self_reflect_on_answer`, `is_generic_or_empty`, and `generate_response_with_context` in `api/chat.py`.

## Function Design

**Size:**
- Keep generated shadcn/ui utilities small and single-purpose, matching `src/lib/utils.ts` and the wrapper components in `src/components/ui/*.tsx`.
- Frontend feature components currently use large in-file handler groups, with `app/components/Chatbot.tsx` acting as the primary example; additions to that file should follow its local helper-plus-render-section structure.

**Parameters:**
- Prefer typed object props for components, as shown by `ButtonProps` in `src/components/ui/button.tsx` and the inline prop typing for `QuickResponseButton` in `app/components/Chatbot.tsx`.
- Use default parameter values for convenience handlers where it improves call sites, such as `sendMessage(messageToSend = message)` in `app/components/Chatbot.tsx` and `topic: str = "General"` in `generate_response_with_context` inside `api/chat.py`.

**Return Values:**
- React components return JSX and are exported as component functions or `React.forwardRef(...)` wrappers in `app/layout.tsx`, `app/page.tsx`, and `src/components/ui/*.tsx`.
- Backend helpers return plain strings or dict-like objects rather than custom classes, as shown by `call_llm_server` in `api/chat.py` and `extract_eva_response` in `api/utils.py`.
- API endpoints return `JSONResponse` payloads with explicit keys such as `response`, `blocks`, and `raw` in `api/api.py`.

## Module Design

**Exports:**
- Use default exports for route-level React modules such as `app/layout.tsx`, `app/page.tsx`, and `app/components/Chatbot.tsx`.
- Use named exports for shared UI primitives and helpers, such as `Button` and `buttonVariants` in `src/components/ui/button.tsx`, `Avatar` helpers in `src/components/ui/avatar.tsx`, and `cn` in `src/lib/utils.ts`.
- Backend routing modules expose shared router objects and functions directly, such as `router` in `api/api.py` and `handler` in `api/main.py`.

**Barrel Files:**
- Barrel files are not part of the current structure.
- Import shared frontend modules directly from concrete files like `@/components/ui/button` and `@/lib/utils` rather than through index aggregators.

---

*Convention analysis: 2026-04-21*
