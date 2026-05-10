import {
  BookOpen,
  Brain,
  CheckCircle2,
  FileText,
  Library,
  MessageSquareText,
  Plus,
  Search,
  Sparkles,
} from "lucide-react";

const domains = ["Health", "Self-help", "AI"];

const sourceQueue = [
  {
    title: "Huberman Lab sleep protocol",
    type: "Podcast transcript",
    status: "Ready for review",
  },
  {
    title: "AI agent notes",
    type: "Personal note",
    status: "Needs tags",
  },
  {
    title: "Training consistency clips",
    type: "Video transcript",
    status: "Draft",
  },
];

const notes = [
  "Sleep cues work best when tied to fixed wake time.",
  "Agent workflows need checkpoints before execution.",
  "Strength habit: reduce setup friction before adding volume.",
];

const workspaceCards = [
  {
    title: "Sources",
    icon: Library,
    count: "3 drafts",
    copy: "Podcast, video, and note material waiting for review.",
  },
  {
    title: "Ingest",
    icon: Plus,
    count: "Paste first",
    copy: "Drop a transcript or raw note, then clean and tag it before save.",
  },
  {
    title: "Notes",
    icon: FileText,
    count: "3 saved",
    copy: "Distilled takeaways that stay linked to source evidence later.",
  },
  {
    title: "Chat",
    icon: MessageSquareText,
    count: "Grounded",
    copy: "Ask from approved workspace sources, not the open web by default.",
  },
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-[#f7f5ef] text-[#181713]">
      <div className="grid min-h-screen lg:grid-cols-[280px_1fr]">
        <aside className="border-r border-[#ded8c8] bg-[#ede7d8] px-5 py-6">
          <div className="mb-8 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[#1f4d3a] text-white">
              <Brain size={22} />
            </div>
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.18em] text-[#6d5f46]">
                Better Everyday
              </p>
              <h1 className="text-xl font-semibold">Self-improvement lab</h1>
            </div>
          </div>

          <nav className="space-y-1 text-sm">
            {["Workspace", "Sources", "Ingest", "Notes", "Chat"].map(
              (item) => (
                <button
                  key={item}
                  className="flex w-full items-center justify-between rounded-md px-3 py-2 text-left font-medium text-[#3e3729] hover:bg-[#ded8c8]"
                >
                  {item}
                  {item === "Workspace" && (
                    <span className="rounded-full bg-[#1f4d3a] px-2 py-0.5 text-xs text-white">
                      active
                    </span>
                  )}
                </button>
              )
            )}
          </nav>

          <div className="mt-8 rounded-md border border-[#d4cbb7] bg-[#f7f5ef] p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#7a6b50]">
              Domains
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {domains.map((domain) => (
                <span
                  key={domain}
                  className="rounded-full border border-[#c9bda7] px-3 py-1 text-sm"
                >
                  {domain}
                </span>
              ))}
            </div>
          </div>
        </aside>

        <section className="px-5 py-6 sm:px-8 lg:px-10">
          <header className="mb-8 flex flex-col gap-4 border-b border-[#ded8c8] pb-6 xl:flex-row xl:items-end xl:justify-between">
            <div>
              <p className="mb-2 text-sm font-semibold uppercase tracking-[0.18em] text-[#7a6b50]">
                Personal source workspace
              </p>
              <h2 className="max-w-3xl text-4xl font-semibold leading-tight">
                Turn podcasts, videos, and notes into useful recall.
              </h2>
              <p className="mt-3 max-w-2xl text-base leading-7 text-[#5d5444]">
                A simpler Open WebUI-inspired home for health, self-help, and
                AI learning. Ingest first. Review before saving. Chat only when
                sources can support the answer.
              </p>
            </div>

            <div className="flex gap-2">
              <button className="inline-flex items-center gap-2 rounded-md bg-[#1f4d3a] px-4 py-2 text-sm font-semibold text-white hover:bg-[#183c2d]">
                <Plus size={16} />
                New source
              </button>
              <button className="inline-flex items-center gap-2 rounded-md border border-[#b9ab91] px-4 py-2 text-sm font-semibold text-[#3e3729] hover:bg-[#ede7d8]">
                <Search size={16} />
                Search
              </button>
            </div>
          </header>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {workspaceCards.map((card) => {
              const Icon = card.icon;
              return (
                <article
                  key={card.title}
                  className="rounded-md border border-[#ded8c8] bg-white p-5 shadow-sm"
                >
                  <div className="mb-4 flex items-center justify-between">
                    <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[#ede7d8] text-[#1f4d3a]">
                      <Icon size={20} />
                    </div>
                    <span className="text-sm font-medium text-[#7a6b50]">
                      {card.count}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold">{card.title}</h3>
                  <p className="mt-2 text-sm leading-6 text-[#5d5444]">
                    {card.copy}
                  </p>
                </article>
              );
            })}
          </div>

          <div className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
            <section className="rounded-md border border-[#ded8c8] bg-white p-5 shadow-sm">
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.16em] text-[#7a6b50]">
                    Ingestion queue
                  </p>
                  <h3 className="text-2xl font-semibold">Review before save</h3>
                </div>
                <Sparkles className="text-[#bd6b2f]" size={24} />
              </div>

              <div className="space-y-3">
                {sourceQueue.map((source) => (
                  <div
                    key={source.title}
                    className="grid gap-3 rounded-md border border-[#eadfca] bg-[#fbfaf6] p-4 sm:grid-cols-[1fr_auto]"
                  >
                    <div>
                      <h4 className="font-semibold">{source.title}</h4>
                      <p className="text-sm text-[#6d5f46]">{source.type}</p>
                    </div>
                    <span className="h-fit rounded-full bg-[#ede7d8] px-3 py-1 text-sm font-medium text-[#5d5444]">
                      {source.status}
                    </span>
                  </div>
                ))}
              </div>

              <div className="mt-5 rounded-md border border-dashed border-[#b9ab91] bg-[#f7f5ef] p-5">
                <div className="flex items-start gap-3">
                  <BookOpen className="mt-1 text-[#1f4d3a]" size={20} />
                  <div>
                    <h4 className="font-semibold">Paste transcript or note</h4>
                    <p className="mt-1 text-sm leading-6 text-[#5d5444]">
                      First real ingestion path: paste raw material, assign a
                      domain, then review cleaned metadata before it becomes
                      active for retrieval.
                    </p>
                  </div>
                </div>
              </div>
            </section>

            <section className="rounded-md border border-[#ded8c8] bg-white p-5 shadow-sm">
              <p className="text-sm font-semibold uppercase tracking-[0.16em] text-[#7a6b50]">
                Notes and grounded chat
              </p>
              <h3 className="mt-1 text-2xl font-semibold">
                Recall, then act.
              </h3>

              <div className="mt-5 space-y-3">
                {notes.map((note) => (
                  <div
                    key={note}
                    className="flex gap-3 rounded-md border border-[#eadfca] p-3"
                  >
                    <CheckCircle2
                      className="mt-0.5 shrink-0 text-[#1f4d3a]"
                      size={18}
                    />
                    <p className="text-sm leading-6 text-[#4d4537]">{note}</p>
                  </div>
                ))}
              </div>

              <div className="mt-5 rounded-md bg-[#1f4d3a] p-4 text-white">
                <p className="text-sm font-semibold">Chat placeholder</p>
                <p className="mt-2 text-sm leading-6 text-[#e2efe7]">
                  Ask later from approved sources only. No localhost-bound chat
                  call in this first slice.
                </p>
              </div>
            </section>
          </div>
        </section>
      </div>
    </main>
  );
}
