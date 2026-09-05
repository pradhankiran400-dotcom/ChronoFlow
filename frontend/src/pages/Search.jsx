import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function Search() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("keyword"); // 'keyword' | 'semantic'
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.topics().then(setTopics).catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    const trimmed = query.trim();
    if (!trimmed) {
      setResults([]);
      return;
    }

    setLoading(true);
    setError("");

    const fetcher = mode === "semantic"
      ? api.aiSearch(trimmed, selectedTopic)
      : api.search(trimmed, selectedTopic);

    fetcher
      .then((data) => {
        setResults(data.results || []);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [query, mode, selectedTopic]);

  return (
    <section className="max-w-4xl">
      <div className="border-b border-black/10 pb-6">
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-moss">Knowledge Search</span>
        <h1 className="mt-2 font-display text-4xl font-semibold">Search Articles & Events</h1>
        <p className="mt-2 text-ink/70">
          Find events by exact keyword matching or explore semantically relevant concepts using AI embedding vectors.
        </p>
      </div>

      {/* Mode & Topic Controls */}
      <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
        {/* Toggle Mode */}
        <div className="inline-flex rounded-xl bg-black/5 p-1">
          <button
            onClick={() => setMode("keyword")}
            className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
              mode === "keyword"
                ? "bg-white text-ink shadow-sm"
                : "text-ink/60 hover:text-ink"
            }`}
          >
            🔍 Keyword Search
          </button>
          <button
            onClick={() => setMode("semantic")}
            className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
              mode === "semantic"
                ? "bg-ink text-parchment shadow-sm"
                : "text-ink/60 hover:text-ink"
            }`}
          >
            ✨ AI Semantic Search
          </button>
        </div>

        {/* Topic Filter */}
        <select
          className="rounded-xl border border-black/15 bg-white px-4 py-2 text-sm text-ink font-medium focus:border-moss focus:outline-none"
          value={selectedTopic}
          onChange={(e) => setSelectedTopic(e.target.value)}
        >
          <option value="">All Topics</option>
          {topics.map((topic) => (
            <option key={topic.id} value={topic.id}>
              {topic.name}
            </option>
          ))}
        </select>
      </div>

      {/* Input */}
      <div className="mt-4 relative">
        <input
          className="w-full rounded-2xl border border-black/15 bg-white px-5 py-4 text-base transition placeholder:text-ink/40 focus:border-moss focus:outline-none focus:ring-2 focus:ring-moss/20"
          placeholder={
            mode === "semantic"
              ? "Ask a concept, e.g., 'generative models adoption in 2023' or 'space telescope findings'…"
              : "Type keyword, title, or summary…"
          }
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            className="absolute right-4 top-4 text-sm text-ink/40 hover:text-ink"
          >
            Clear
          </button>
        )}
      </div>

      {error && <p className="mt-4 rounded-xl bg-red-100 p-4 text-sm text-red-800">{error}</p>}

      {/* Results */}
      {loading ? (
        <div className="mt-8 space-y-4">
          <div className="h-24 animate-pulse rounded-2xl bg-black/5" />
          <div className="h-24 animate-pulse rounded-2xl bg-black/5" />
        </div>
      ) : (
        <ul className="mt-8 space-y-4">
          {results.map((article) => {
            const similarityPercent = article.similarity_score
              ? Math.round(article.similarity_score * 100)
              : null;

            return (
              <li
                key={article.id}
                className="rounded-2xl border border-black/10 bg-white p-6 shadow-sm transition hover:border-moss/40 hover:shadow-md"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="font-mono text-sm font-semibold text-brass">
                    📅 {article.event_date}
                  </span>
                  {similarityPercent !== null && (
                    <span className="rounded-full bg-brass/10 px-3 py-1 text-xs font-semibold text-brass">
                      {similarityPercent}% Match Score
                    </span>
                  )}
                </div>

                <Link
                  to={`/articles/${article.id}`}
                  className="mt-2 block font-display text-2xl font-semibold text-ink hover:text-moss"
                >
                  {article.title}
                </Link>

                {article.summary && (
                  <p className="mt-2 text-ink/70 leading-relaxed">{article.summary}</p>
                )}

                <div className="mt-4 flex items-center justify-between text-xs text-ink/50">
                  <span>Topic #{article.topic_id}</span>
                  <Link
                    to={`/articles/${article.id}`}
                    className="font-semibold text-moss hover:underline"
                  >
                    View Article Details →
                  </Link>
                </div>
              </li>
            );
          })}
        </ul>
      )}

      {!loading && query.trim() && results.length === 0 && !error && (
        <p className="mt-10 text-center text-ink/60">
          No articles found for "{query}". Try adjusting search terms or mode.
        </p>
      )}
    </section>
  );
}

