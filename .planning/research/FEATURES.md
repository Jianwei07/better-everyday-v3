# Feature Landscape

**Domain:** Personal AI research workspace and adaptive knowledge coach
**Project:** Better Everyday
**Researched:** 2026-04-22
**Overall confidence:** MEDIUM-HIGH

## Scope for this research

This repo is not trying to become a generic all-purpose chatbot or a broad agent platform. The right comparison set is products like NotebookLM, Claude Projects, Reflect, Readwise Reader, ChatGPT memory, and Notion AI: tools that combine curated sources, persistent context, note workflows, and repeat-use assistance.

For **Better Everyday**, the feature bar should be set by one core promise:

> **Turn trusted personal sources (starting with YouTube transcripts and notes) into a workspace I can rely on every day for grounded recall, synthesis, and eventually coaching.**

That means features that improve **trust, reuse, and source organization** matter more than flashy generation or broad automation.

## Table Stakes

Features users will reasonably expect from a strong personal AI research workspace in this project shape. Missing these makes the app feel like a brittle transcript bot.

| Feature | Why Expected for This Project | Value | Complexity | Timing | Dependencies | Notes |
|---------|-------------------------------|-------|------------|--------|--------------|-------|
| Source ingestion from YouTube URLs and pasted notes/transcripts | This is the app's starting material and explicit product requirement | High | Med | **v1** | Stable ingestion pipeline, source storage | Must treat pasted notes as first-class, not a workaround |
| Source normalization pipeline | High-quality products do not dump raw imports into chat; they clean titles, metadata, chunks, and summaries on arrival | High | Med | **v1** | Ingestion pipeline, metadata schema | For this product, this is table stakes because ingestion quality directly controls trust |
| Topic/workspace organization | Notebook/project-style grouping is standard in NotebookLM and Claude Projects; users need bounded context, not one giant global blob | High | Med | **v1** | Topic model, source metadata | Keep topic scopes simple and explicit |
| Grounded chat with inline citations or quote-level evidence | NotebookLM sets the bar here; this repo's core value is grounded recall from curated sources | Very high | Med | **v1** | Retrieval quality, response shaping | Must let user inspect source evidence quickly |
| Source-scoped retrieval controls | Users need to include/exclude sources or ask within a chosen topic to keep answers trustworthy | High | Med | **v1** | Topic/workspace organization | Prevents cross-topic contamination and generic answers |
| Search and browse across sources, notes, and prior summaries | Research workspaces need both chat and direct retrieval; chat-only shells create re-discovery pain | High | Med | **v1** | Indexing, metadata, source summaries | Search should expose documents and snippets, not only chat answers |
| Save useful outputs as notes | NotebookLM and note tools convert chat into reusable notes; daily-use products preserve insights, not just conversations | High | Low-Med | **v1** | Note model, citation preservation | Saved notes should retain source links/citations |
| Clear answer failure behavior | High-trust products need graceful "not enough evidence" responses instead of confident invention | Very high | Med | **v1** | Retrieval thresholds, response policy | This is essential for daily trust |
| Basic chat history inside each workspace | Users expect continuity within a project/notebook, even before advanced memory | Med-High | Low | **v1** | Workspace model | Keep history scoped; do not blend everything globally |
| Lightweight source summaries and tags | Helps re-find material and makes later coaching usable | High | Low-Med | **v1** | Source normalization pipeline | Initial tags can be AI-assisted but user-editable |

## Differentiators

These are the features that make the product feel like **Better Everyday** instead of "NotebookLM but smaller." Strong differentiators should be layered after the trust foundation is working.

| Feature | Value Proposition | Value | Complexity | Timing | Dependencies | Notes |
|---------|-------------------|-------|------------|--------|--------------|-------|
| Ingestion assistant for cleaning, tagging, summarizing, and organizing | Matches the product direction exactly: narrow agent help where it is most useful and lowest risk | Very high | Med-High | **v1.5 / early later** | Stable ingestion, editable metadata, review UI | Best first agent surface because outputs are inspectable before they affect chat |
| Trusted-source controls and trust tiers | Lets the product weight or privilege sources the user actually trusts, improving grounded coaching later | Very high | Med | **v1.5 / later** | Source metadata, retrieval policy | Example: trusted / neutral / low-priority |
| Workspace-first UI with source pane + notes pane + chat | Moves the product away from generic chatbot shell and toward an actual research desk | High | Med-High | **v1** | Frontend rewrite, source/note models | More important than adding many new AI tricks |
| Evidence-first answer view | Beyond plain citations: show supporting quotes, source cards, and maybe "why this answer" retrieval context | High | Med | **v1.5 / later** | Citation pipeline, retrieval diagnostics | Major trust booster for daily use |
| Goal memory for coaching | Enables guidance tied to user goals rather than only answering about documents | Very high | Med | **later** | Memory model, trusted-source controls, history relevance | Keep explicit and editable |
| Prior-chat memory with relevance filtering | Makes the assistant feel cumulative without becoming creepy or noisy | High | High | **later** | Chat history, memory ranking, controls | Should retrieve only relevant prior chats, not dump full history |
| Coaching mode grounded in trusted sources + goals + prior chats | The long-term differentiator: adaptive coach, not just research assistant | Very high | High | **later** | Goal memory, trusted-source controls, strong grounding | Must never outrun evidence quality |
| Daily resurfacing / review loop | Borrowing from Readwise, this drives repeat use by resurfacing useful insights, notes, or unanswered threads | High | Med | **later** | Notes, memory, scheduling | Best daily-use retention feature once note quality is good |
| Source-to-note conversion workflows | Convert summaries, highlights, and chat outputs into durable personal knowledge assets | High | Med | **v1.5 / later** | Notes, citations, source summaries | Strong bridge between RAG app and knowledge workspace |
| Personalized follow-up suggestions | Suggest next questions, comparisons, or actions based on current workspace and goals | Med-High | Med | **later** | Goals, history, source graph | Helpful if grounded; annoying if generic |

## Anti-Features

Features that would add cost, complexity, or user distrust faster than they add product value.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Generic web-scale assistant mode by default | Breaks the product's trust promise and competes with tools that already do broad chat better | Default to curated-source answers; add explicit opt-in external search later if needed |
| Broad autonomous agents that browse, decide, and mutate data unsupervised | Too much surface area, weak inspectability, and directly out of scope for v1 | Keep agent behavior narrow and reviewable in ingestion workflows |
| Multi-user/family accounts in v1 | Adds auth, privacy, permissions, and memory isolation complexity before single-user value is proven | Stay personal-first; design data model so multi-user can be added later |
| Flashy artifact generation first (podcasts, slide decks, infographics, mind maps) | NotebookLM proves these are nice-to-have, but they do not solve this repo's current trust and workflow gaps | Start with source summaries, notes, and evidence-backed chat |
| Automatic hidden memory writes | Dangerous for a personal coach product; silent memory causes drift and loss of trust | Use explicit, inspectable memory objects like goals, trusted sources, and pinned facts |
| One giant undifferentiated knowledge base | Creates noisy retrieval and makes the workspace feel sloppy | Keep topic/workspace boundaries explicit with source-level controls |
| Heavy local model hosting as a prerequisite | Violates cost/efficiency constraints and slows iteration | Prefer efficient hosted/local-light models plus better retrieval |
| Native mobile app in early phases | Too much UI and sync complexity for uncertain value | Make the web app reliable and usable on desktop first |
| Rich social sharing/collaboration | Not aligned with personal-first scope and privacy goals | Focus on private capture, organization, and reuse |

## Feature Dependencies

```text
YouTube/note ingestion -> source normalization -> topic/workspace organization -> grounded chat
source normalization -> source summaries/tags -> search/browse -> save to notes
grounded chat + citations -> evidence-first answer view
topic/workspace organization + chat history -> prior-chat relevance
source metadata -> trusted-source controls -> coaching mode
goal memory + trusted-source controls + prior-chat relevance -> adaptive coaching
notes + saved outputs -> daily resurfacing/review loop
```

## MVP Recommendation

### v1 should prioritize

1. **Reliable source ingestion for YouTube + pasted notes**
   - Because the product lives or dies on whether new material gets in cleanly.
2. **Source normalization with editable tags/summaries**
   - Because messy inputs create untrustworthy outputs.
3. **Workspace/topic organization with source controls**
   - Because trust requires bounded retrieval.
4. **Grounded chat with inspectable evidence and good failure behavior**
   - Because daily use depends on trust, not just answer fluency.
5. **Search/browse + save-to-notes workflow**
   - Because a workspace must support recall outside chat.
6. **Workspace-first UI**
   - Because the product should feel like a research desk, not a chatbot wrapper.

### Best v1 differentiator

**Human-in-the-loop ingestion assistant**

If there is room for one standout feature beyond the basics, it should be an assistant that proposes:
- title cleanup
- tags
- summary
- topic placement
- maybe chunking hints

...with explicit review before saving. This is safer and more product-specific than autonomous agents or broad coaching.

### Defer to later

- Goal-aware coaching
- Prior-chat memory with retrieval
- Daily resurfacing/review habit loops
- Trust tiers and retrieval weighting across sources
- External web research / deep research
- Audio/video/visual artifact generation
- Multi-user/family support

## Opinionated Build Order

### Phase 1 — Trustworthy workspace foundation
- ingestion
- source cleanup
- topic organization
- grounded chat
- citations/evidence
- search/browse
- save-to-notes

### Phase 2 — Ingestion intelligence
- AI-assisted cleanup
- AI-generated tags/summaries
- source organization suggestions
- review/approve loop

### Phase 3 — Personal memory foundation
- goals
- trusted sources
- editable personal preferences
- relevant prior-chat recall

### Phase 4 — Adaptive coach
- coaching prompts/views
- goal progress check-ins
- source-grounded recommendations
- daily resurfacing and follow-up loops

## Product-Specific Notes

### Features that most improve trust

1. **Inline citations or quote cards tied to exact sources**
2. **Source scoping and easy include/exclude controls**
3. **Visible uncertainty / "not enough evidence" behavior**
4. **Editable summaries/tags instead of opaque AI-only organization**
5. **Explicit memory management for goals and trusted sources**

### Features that most improve daily reuse

1. **Fast re-entry into a workspace with prior context**
2. **Search across sources and notes**
3. **Saving answers into reusable notes**
4. **Source summaries that reduce re-reading cost**
5. **Later: resurfacing useful notes and unfinished threads**

### Features likely to look appealing but underperform early

- mind maps
- audio summaries
- elaborate artifact generators
- open-ended agents
- broad web browsing

These can wait until the core loop is already trusted.

## Sources

- Google NotebookLM Help — Learn about NotebookLM, grounded chat with citations, source import, notes, mind maps, audio overviews:  
  - https://support.google.com/notebooklm/answer/16164461?hl=en **(HIGH)**  
  - https://support.google.com/notebooklm/answer/16179559?hl=en **(HIGH)**  
  - https://support.google.com/notebooklm/answer/16215270?hl=en **(HIGH)**  
  - https://support.google.com/notebooklm/answer/16262519?hl=en **(HIGH)**  
  - https://support.google.com/notebooklm/answer/16212283?hl=en **(HIGH)**  
  - https://support.google.com/notebooklm/answer/16212820?hl=en **(HIGH)**
- Claude Help / Anthropic — project workspaces, project knowledge, instructions, RAG-backed project knowledge:  
  - https://support.claude.com/en/articles/9517075-what-are-projects **(HIGH)**  
  - https://www.anthropic.com/news/projects **(MEDIUM-HIGH)**
- OpenAI Help — memory controls, saved memories vs chat history, explicit user control over what is remembered:  
  - https://help.openai.com/en/articles/8590148-memory-faq **(HIGH)**
- Reflect — networked notes, backlinks, fast search, end-to-end encryption, integrated AI assistant for notes:  
  - https://reflect.app/ **(MEDIUM)**
- Readwise Reader — unified reading inbox, transcript highlighting, annotations, search, daily review/resurfacing, sync to note apps:  
  - https://readwise.io/read **(MEDIUM-HIGH)**
- Notion AI — workspace-native AI, search across connected apps, agents, meeting notes, governance/privacy patterns:  
  - https://www.notion.com/product/ai **(MEDIUM-HIGH)**
- Project context and repo constraints:  
  - `/Users/jayden77/dev/better-everyday-v3/.planning/PROJECT.md` **(HIGH)**  
  - `/Users/jayden77/dev/better-everyday-v3/.planning/codebase/ARCHITECTURE.md` **(HIGH)**  
  - `/Users/jayden77/dev/better-everyday-v3/.planning/codebase/CONCERNS.md` **(HIGH)**
