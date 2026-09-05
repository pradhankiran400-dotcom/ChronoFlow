import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function Home() {
  const [topics, setTopics] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .topics()
      .then(setTopics)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <section className="space-y-12">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-3xl border border-black/10 bg-gradient-to-br from-ink via-ink/95 to-moss p-8 md:p-12 text-parchment shadow-lg">
        <span className="text-xs font-semibold uppercase tracking-[0.25em] text-brass">
          AI-Powered Knowledge & Timeline Explorer
        </span>
        <h1 className="mt-4 max-w-3xl font-display text-4xl md:text-6xl font-semibold leading-tight tracking-tight">
          Explore How Ideas & Events Evolve Over Time.
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-parchment/80 leading-relaxed font-light">
          ChronoFlow organizes historical milestones into interactive timelines, semantic vector search indexes, and RAG-driven AI answer synthesis.
        </p>

        <div className="mt-8 flex flex-wrap gap-4">
          <Link
            to="/timeline"
            className="rounded-xl bg-brass px-6 py-3 font-semibold text-ink transition hover:bg-brass/90 shadow-md"
          >
            Explore All Timelines →
          </Link>
          <Link
            to="/ask"
            className="rounded-xl border border-parchment/30 bg-parchment/10 px-6 py-3 font-semibold text-parchment transition hover:bg-parchment/20 backdrop-blur"
          >
            ✨ Ask AI Companion
          </Link>
        </div>
      </div>

      {error && (
        <div className="rounded-2xl bg-red-100 p-5 text-sm text-red-800 border border-red-200">
          <span className="font-semibold">Backend Connection Issue:</span> Unable to communicate with the ChronoFlow API ({error}). Please ensure the FastAPI backend is running on port 8000.
        </div>
      )}

      {/* Topics Grid */}
      <div>
        <div className="flex items-center justify-between border-b border-black/10 pb-4">
          <div>
            <span className="text-xs font-semibold uppercase tracking-[0.2em] text-moss">Knowledge Domains</span>
            <h2 className="font-display text-3xl font-semibold text-ink">Browse Topics</h2>
          </div>
          <Link to="/manage" className="text-xs font-semibold text-moss hover:underline">
            + Manage Topics
          </Link>
        </div>

        {loading ? (
          <div className="mt-6 grid gap-5 md:grid-cols-3">
            <div className="h-36 animate-pulse rounded-2xl bg-black/5" />
            <div className="h-36 animate-pulse rounded-2xl bg-black/5" />
            <div className="h-36 animate-pulse rounded-2xl bg-black/5" />
          </div>
        ) : (
          <div className="mt-6 grid gap-6 md:grid-cols-3">
            {topics.map((topic) => (
              <Link
                key={topic.id}
                to={`/timeline/${topic.id}`}
                className="group rounded-2xl border border-black/10 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:border-moss hover:shadow-md"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-display text-2xl font-semibold text-ink group-hover:text-moss">
                    {topic.name}
                  </h3>
                  <span className="text-sm font-bold text-brass transition group-hover:translate-x-1">
                    →
                  </span>
                </div>
                <p className="mt-3 text-sm text-ink/70 leading-relaxed">
                  {topic.description || "Explore milestones in this topic."}
                </p>
              </Link>
            ))}

            {topics.length === 0 && !error && (
              <div className="col-span-full rounded-2xl border border-dashed border-black/20 p-8 text-center text-ink/60">
                No topics configured yet. <Link to="/manage" className="text-moss font-semibold underline">Add your first topic</Link> in Manage.
              </div>
            )}
          </div>
        )}
      </div>

      {/* Feature Highlights Grid */}
      <div className="grid gap-6 md:grid-cols-3">
        <div className="rounded-2xl border border-black/10 bg-white p-6">
          <div className="text-2xl">⏳</div>
          <h3 className="mt-3 font-display text-xl font-semibold">Interactive Timelines</h3>
          <p className="mt-2 text-sm text-ink/70">
            Filter events by date ranges, topics, search terms, and multi-tag categorizations.
          </p>
        </div>

        <div className="rounded-2xl border border-black/10 bg-white p-6">
          <div className="text-2xl">🔍</div>
          <h3 className="mt-3 font-display text-xl font-semibold">Hybrid Search</h3>
          <p className="mt-2 text-sm text-ink/70">
            Toggle between fast exact keyword search and Sentence Transformer vector similarity search.
          </p>
        </div>

        <div className="rounded-2xl border border-black/10 bg-white p-6">
          <div className="text-2xl">🤖</div>
          <h3 className="mt-3 font-display text-xl font-semibold">RAG AI Companion</h3>
          <p className="mt-2 text-sm text-ink/70">
            Get accurate answers synthesized with LLM reasoning and linked source citations.
          </p>
        </div>
      </div>
    </section>
  );
}

