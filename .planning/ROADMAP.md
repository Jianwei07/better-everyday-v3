# Roadmap: Better Everyday

## Overview

Better Everyday is a brownfield rebuild from a brittle split chat demo into a trustworthy personal research workspace. The roadmap starts by repairing the current web/API boundary and workspace shell, then moves through reviewable ingestion, evidence-backed chat, daily-use search and notes, narrow ingest assistance, and finally personal memory-driven coaching.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Boundary Repair & Workspace Shell** - Repair brownfield routing and reliability seams while establishing the workspace-first app shell.
- [ ] **Phase 2: Reviewable Source Intake** - Let the user add sources, review ingest results, and manage the source library before retrieval uses new material.
- [ ] **Phase 3: Grounded Chat & Evidence** - Deliver workspace-scoped answers with citations, evidence views, and clear insufficient-evidence behavior.
- [ ] **Phase 4: Search, Notes & Follow-up** - Make the workspace useful for daily recall through search, saved notes, and resurfaced follow-up context.
- [ ] **Phase 5: Ingestion Assistant** - Add narrow, reviewable AI help during source cleanup and organization.
- [ ] **Phase 6: Personal Memory & Coaching** - Layer in goals, trusted sources, and coaching mode after the workspace earns trust.

## Phase Details

### Phase 1: Boundary Repair & Workspace Shell
**Goal**: Users can reliably enter and navigate a workspace-first app through a production-safe web boundary instead of the current brittle localhost-bound shell.
**Depends on**: Nothing (first phase)
**Requirements**: EXP-01, WRK-01
**Success Criteria** (what must be TRUE):
  1. User can open the app and move between dedicated sources, notes, and chat views without broken routes or localhost-only networking assumptions.
  2. User can create or select an explicit topic workspace and see their activity scoped to that workspace.
  3. The rebuilt web flow behaves consistently through the supported app entrypoint rather than exposing duplicate or debug-oriented public paths.
**Plans**: TBD
**UI hint**: yes

### Phase 2: Reviewable Source Intake
**Goal**: Users can add, inspect, and curate sources inside a workspace before those sources affect retrieval.
**Depends on**: Phase 1
**Requirements**: ING-01, ING-02, ING-03, ING-04, WRK-02, KNOW-02
**Success Criteria** (what must be TRUE):
  1. User can add a source to a workspace from either a YouTube URL or pasted transcript or note content.
  2. User can review cleaned metadata, summary, and tags before a new source becomes active.
  3. User can approve or reject ingest results so only accepted sources are used for retrieval.
  4. User can browse the workspace source library and edit source tags and summaries after ingestion.
**Plans**: TBD
**UI hint**: yes

### Phase 3: Grounded Chat & Evidence
**Goal**: Users can ask questions inside a workspace and judge whether answers are trustworthy based on inspectable evidence.
**Depends on**: Phase 2
**Requirements**: CHAT-01, CHAT-02, CHAT-03, CHAT-04
**Success Criteria** (what must be TRUE):
  1. User can ask questions within a workspace and receive answers grounded in that workspace's sources by default.
  2. User can inspect citations linked to the sources used in an answer.
  3. User sees a clear insufficient-evidence response when the workspace does not support an answer.
  4. User can open an evidence view showing the source snippets that support an answer.
**Plans**: TBD
**UI hint**: yes

### Phase 4: Search, Notes & Follow-up
**Goal**: Users can reuse what they have learned by searching the workspace, saving grounded notes, and resurfacing useful prior context.
**Depends on**: Phase 3
**Requirements**: KNOW-01, KNOW-03, AST-02
**Success Criteria** (what must be TRUE):
  1. User can search across sources, summaries, and saved notes from the workspace experience.
  2. User can save a useful chat answer as a reusable note while retaining its source citations.
  3. User can see resurfaced notes or prior threads for follow-up during daily use.
**Plans**: TBD
**UI hint**: yes

### Phase 5: Ingestion Assistant
**Goal**: Users get narrow, reviewable AI help that improves source quality before new material is committed to the workspace.
**Depends on**: Phase 2
**Requirements**: AST-01
**Success Criteria** (what must be TRUE):
  1. User receives ingest-assistant suggestions for cleanup, tags, summaries, or topic placement before saving a source.
  2. User can accept, edit, or ignore suggested ingest improvements instead of having opaque automatic changes applied.
**Plans**: TBD
**UI hint**: yes

### Phase 6: Personal Memory & Coaching
**Goal**: Users can steer the assistant with explicit goals and trusted sources, then switch into a coaching mode that stays grounded in those preferences.
**Depends on**: Phase 3
**Requirements**: MEM-01, MEM-02, MEM-03
**Success Criteria** (what must be TRUE):
  1. User can create and edit explicit goals or priorities that the assistant can reference.
  2. User can mark sources as trusted or preferred for later assistant use.
  3. User can switch into a coaching mode and receive responses tailored using stored goals and trusted sources.
**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Boundary Repair & Workspace Shell | 0/TBD | Not started | - |
| 2. Reviewable Source Intake | 0/TBD | Not started | - |
| 3. Grounded Chat & Evidence | 0/TBD | Not started | - |
| 4. Search, Notes & Follow-up | 0/TBD | Not started | - |
| 5. Ingestion Assistant | 0/TBD | Not started | - |
| 6. Personal Memory & Coaching | 0/TBD | Not started | - |
