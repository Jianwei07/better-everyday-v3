# Codebase Concerns

**Analysis Date:** 2026-04-21

## Tech Debt

**Runtime and dependency drift:**
- Issue: Python dependency management is split across `requirements.txt` and `api/requirements.txt`, and the manifests do not match. `api/add_data.py` imports `langchain_chroma`, but `langchain-chroma==0.2.4` is only present in `requirements.txt`, not `api/requirements.txt`.
- Files: `requirements.txt`, `api/requirements.txt`, `api/add_data.py`, `README-backend.md`
- Impact: Backend setup becomes environment-dependent. Installing from `api/requirements.txt` leaves the ingestion path broken, while the docs point at a different install flow.
- Fix approach: Collapse Python dependencies into one authoritative manifest and keep `README-backend.md` aligned with that file.

**Committed runtime artifacts:**
- Issue: Generated runtime state is committed in the repo, including `api/__pycache__/*.pyc` and the persistent Chroma database under `chroma_storage/`.
- Files: `api/__pycache__/__init__.cpython-311.pyc`, `api/__pycache__/main.cpython-312.pyc`, `chroma_storage/chroma.sqlite3`, `chroma_storage/3423ba22-e29c-4975-acba-2bd618e56a7e/data_level0.bin`
- Impact: Git history accumulates machine-specific artifacts, local database state, and noisy diffs. Runtime behavior becomes tied to whatever dataset happened to be committed last.
- Fix approach: Remove generated artifacts from version control, extend `.gitignore`, and recreate local vector data through `api/add_data.py`.

**Duplicate chatbot implementation:**
- Issue: `app/components/Proxy.tsx` duplicates the live UI in `app/components/Chatbot.tsx` but has already drifted.
- Files: `app/components/Chatbot.tsx`, `app/components/Proxy.tsx`, `app/page.tsx`
- Impact: Two large components implement the same flow differently, increasing maintenance cost and making future UI changes easy to apply inconsistently.
- Fix approach: Remove `app/components/Proxy.tsx` or convert shared behavior into smaller reused modules.

## Known Bugs

**FastAPI app imports the wrong router symbol:**
- Symptoms: Starting the backend through `uvicorn api.main:app --reload` is brittle because `api/main.py` imports `router` from the package root, but `api/__init__.py` does not export `router`.
- Files: `api/main.py`, `api/__init__.py`, `api/api.py`
- Trigger: Importing `api.main` in a package-aware runtime.
- Workaround: Import `router` from `api.api` directly or re-export it from `api/__init__.py`.

**App Router API file is not a valid Next.js route handler:**
- Symptoms: `app/api/chat.ts` uses `NextApiRequest` / `NextApiResponse` and a default export, which is the Pages Router pattern, not the App Router pattern.
- Files: `app/api/chat.ts`
- Trigger: Hitting `/app/api/chat` in a Next.js 15 App Router deployment.
- Workaround: Replace it with `app/api/chat/route.ts` exporting `POST`, or remove the file if the browser should call another backend path.

**Frontend networking is hardcoded to localhost:**
- Symptoms: The chat UI posts directly to `http://127.0.0.1:8000/chat` even though `next.config.js` defines environment-driven rewrites.
- Files: `app/components/Chatbot.tsx`, `app/components/Proxy.tsx`, `next.config.js`
- Trigger: Opening the deployed frontend anywhere other than the developer machine.
- Workaround: Route requests through the configured Next.js rewrite or a real server-side route handler.

**Legacy Chroma inspection scripts are broken:**
- Symptoms: Maintenance scripts reference collections and config symbols that no longer exist.
- Files: `api/check_data.py`, `api/test.py`, `api/config.py`
- Trigger: Running `python api/check_data.py` or `python api/test.py` against the current topic-per-collection setup.
- Workaround: Update these scripts to use the current collection naming pattern and the current `api/config.py` exports.

## Security Considerations

**Debug data is exposed through the public API surface:**
- Risk: The main chat endpoint returns the cleaned answer plus the raw model output, and `/test_llm` exposes retrieved context directly.
- Files: `api/api.py`
- Current mitigation: None beyond generic FastAPI exception handling.
- Recommendations: Remove the `raw` field from `POST /chat`, gate `POST /test_llm` behind an authenticated admin path, and keep retrieval/debug inspection off the public router.

**No authentication or request throttling on expensive endpoints:**
- Risk: `POST /chat` and `POST /test_llm` are unauthenticated even though they trigger retrieval and model inference. CORS in `api/main.py` restricts browser origins, but it does not protect server-to-server abuse.
- Files: `api/main.py`, `api/api.py`, `api/chat.py`
- Current mitigation: `CORSMiddleware` only allows `http://localhost:3000` and `https://better-everyday-v3.vercel.app`.
- Recommendations: Add auth, rate limiting, and request quotas before exposing the backend outside local development.

## Performance Bottlenecks

**Each chat request can spend two full model timeouts:**
- Problem: The response path performs a primary LLM call and then a self-reflection LLM call, each wrapped with a `120.0` second timeout.
- Files: `api/chat.py`
- Cause: `generate_response_with_context()` always keeps the second generation step in the hot path unless the first answer is detected as generic.
- Improvement path: Make self-reflection optional, reduce default timeout budgets, and add request-level tracing so slow prompts can be identified.

**Retrieval does full-collection metadata scans on every query:**
- Problem: Retrieval fetches `current_collection.count()` records and prints all unique metadata values before running the actual query.
- Files: `api/embedding_search.py`
- Cause: Debug logging calls `current_collection.get(limit=current_collection.count(), include=["metadatas"])` on every request.
- Improvement path: Remove the per-request full scan, keep metadata inspection in offline tooling only, and replace `print` dumping with bounded structured logs.

## Fragile Areas

**Large, stateful chatbot component:**
- Files: `app/components/Chatbot.tsx`
- Why fragile: One 471-line client component owns transport, topic selection, resize behavior, optimistic UI, and rendering. Small changes can easily affect unrelated interactions.
- Safe modification: Extract transport, message state, and topic selection into hooks or child components before extending behavior.
- Test coverage: No frontend tests detected for the component.

**Unused duplicate UI file already contains hard failures:**
- Files: `app/components/Proxy.tsx`
- Why fragile: The file contains `handleKeyDown()` throwing `Function not implemented.`, uses inconsistent image paths, and still posts to localhost. Even if it is currently unused, it is close enough to the real implementation to be mistaken for the supported path.
- Safe modification: Delete the file or rename it clearly as archived code outside the active component tree.
- Test coverage: No tests detected to catch accidental reuse.

## Scaling Limits

**Single-host local retrieval and inference stack:**
- Current capacity: One FastAPI process orchestrates retrieval in `api/chat.py`, one in-process `SentenceTransformer` instance is loaded in `api/embedding_search.py`, and Chroma persists to the local filesystem configured in `api/config.py`.
- Limit: Throughput remains bounded by one host's CPU/GPU, local disk-backed `chroma_storage/`, and repeated model loading per worker/process.
- Scaling path: Move embedding/search and generation behind independently scalable services, externalize vector storage, and avoid process-local model initialization in request-serving modules.

## Dependencies at Risk

**Environment contract for LLM serving is inconsistent:**
- Risk: The documented backend env points `LLM_SERVER_URL` at `http://localhost:8001/v1/completions`, while `api/config.py` defaults to `http://eva-llama-cpp:8001/completion`.
- Impact: A deployment can appear correctly configured while still targeting the wrong path or service shape.
- Migration plan: Define one supported LLM API contract, store it in a single config module, and align `README-backend.md` with `api/config.py`.

## Missing Critical Features

**No production-safe frontend-to-backend bridge:**
- Problem: The active UI calls the backend directly from the browser, while the checked-in Next API file is only a placeholder and is implemented with the wrong routing model.
- Blocks: Reliable deployment of the frontend without local FastAPI access, consistent environment switching, and centralized auth/rate limiting at the web boundary.

## Test Coverage Gaps

**No automated regression suite for chat flows:**
- What's not tested: API response shaping, retrieval fallbacks, router imports, and frontend message submission behavior.
- Files: `package.json`, `api/api.py`, `api/chat.py`, `app/components/Chatbot.tsx`
- Risk: Routing and integration regressions can ship unnoticed because the repo contains no detected `*.test.*` or `*.spec.*` files and `package.json` has no test script.
- Priority: High

**No coverage for ingestion and Chroma maintenance scripts:**
- What's not tested: `--reset_db` behavior, topic-per-collection ingestion, and maintenance utilities that inspect existing vector data.
- Files: `api/add_data.py`, `api/check_data.py`, `api/chroma_db_checker.py`, `api/test.py`
- Risk: Operational scripts silently drift away from the live schema, which is already visible in `api/check_data.py` and `api/test.py`.
- Priority: High

---

*Concerns audit: 2026-04-21*
