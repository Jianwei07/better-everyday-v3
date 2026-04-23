# Requirements: Better Everyday

**Defined:** 2026-04-22
**Core Value:** Grounded recall from personally curated sources so the assistant gives trustworthy answers I will actually use every day.

## v1 Requirements

Requirements for the initial rebuild release.

### Experience

- [ ] **EXP-01**: User can use a workspace-first web interface with dedicated views for sources, notes, and chat instead of a single chat-only shell.

### Ingestion

- [ ] **ING-01**: User can import a YouTube video into a workspace from its URL.
- [ ] **ING-02**: User can paste transcript text or personal notes into a workspace.
- [ ] **ING-03**: User can review cleaned source metadata, summary, and tags before a new source becomes active.
- [ ] **ING-04**: User can approve or reject ingest results before the source is used for retrieval.

### Workspace

- [ ] **WRK-01**: User can organize sources and chats into explicit topic workspaces.
- [ ] **WRK-02**: User can view and edit source tags and summaries inside a workspace.

### Chat and Trust

- [ ] **CHAT-01**: User can ask questions within a workspace and receive answers grounded in workspace sources by default.
- [ ] **CHAT-02**: User can inspect citations linked to the sources used in an answer.
- [ ] **CHAT-03**: User sees a clear insufficient-evidence response when the workspace does not support an answer.
- [ ] **CHAT-04**: User can open an evidence view showing the supporting source snippets for an answer.

### Search and Notes

- [ ] **KNOW-01**: User can search across sources, summaries, and saved notes.
- [ ] **KNOW-02**: User can browse the source library outside the chat flow.
- [ ] **KNOW-03**: User can save a useful chat answer as a reusable note while retaining its source citations.

### Personalization

- [ ] **MEM-01**: User can create and edit explicit goals or priorities that the assistant can reference.
- [ ] **MEM-02**: User can mark sources as trusted or preferred.
- [ ] **MEM-03**: User can switch into a coaching mode that tailors responses using stored goals and trusted sources.

### AI Assistance

- [ ] **AST-01**: User can receive ingest-assistant suggestions for cleanup, tags, summaries, or topic placement before saving a source.
- [ ] **AST-02**: User can receive daily resurfaced notes or threads for follow-up.

## v2 Requirements

Deferred to a later release.

### Workspace Controls

- **WRK-03**: User can include or exclude individual sources when asking within a workspace.
- **WRK-04**: User can reopen and browse prior chat sessions inside each workspace.

### Memory

- **MEM-04**: User can retrieve only relevant prior chats as contextual memory instead of using global chat history.
- **MEM-05**: User can apply multiple trust tiers or retrieval weighting across sources.

## Out of Scope

Explicitly excluded from this initialization scope.

| Feature | Reason |
|---------|--------|
| Family accounts / multi-user support | v1 is personal-first and should avoid auth, privacy, and memory-isolation complexity |
| Native mobile app | Web app only for v1 |
| Broad autonomous agent workflows | Start with narrow, reviewable ingestion assistance instead |
| Generic web-scale assistant mode by default | The core value is grounded recall from curated sources, not open-ended general chat |
| Rich artifact generation (podcasts, slide decks, mind maps) | Trust, ingestion, and daily workspace flow matter more than flashy outputs |
| Heavy always-on paid or resource-hungry model hosting | The project should stay efficient and mostly free to operate |

## Traceability

Which phases cover which requirements. Filled during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| EXP-01 | TBD | Pending |
| ING-01 | TBD | Pending |
| ING-02 | TBD | Pending |
| ING-03 | TBD | Pending |
| ING-04 | TBD | Pending |
| WRK-01 | TBD | Pending |
| WRK-02 | TBD | Pending |
| CHAT-01 | TBD | Pending |
| CHAT-02 | TBD | Pending |
| CHAT-03 | TBD | Pending |
| CHAT-04 | TBD | Pending |
| KNOW-01 | TBD | Pending |
| KNOW-02 | TBD | Pending |
| KNOW-03 | TBD | Pending |
| MEM-01 | TBD | Pending |
| MEM-02 | TBD | Pending |
| MEM-03 | TBD | Pending |
| AST-01 | TBD | Pending |
| AST-02 | TBD | Pending |

**Coverage:**
- v1 requirements: 19 total
- Mapped to phases: 0
- Unmapped: 19 ⚠

---
*Requirements defined: 2026-04-22*
*Last updated: 2026-04-22 after initial definition*
