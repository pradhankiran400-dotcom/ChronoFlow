import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

const SUGGESTIONS = [
  "How did Artificial Intelligence evolve during 2023?",
  "What space exploration milestones occurred recently?",
  "Tell me about the release of ChatGPT and GPT-4.",
];

function formatUrlsInText(text) {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const parts = text.split(urlRegex);
  return parts.map((part, i) => {
    if (part.match(urlRegex)) {
      let domain = "External Source";
      try {
        domain = new URL(part).hostname.replace("www.", "");
      } catch (e) {}
      return (
        <a
          key={i}
          href={part}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 mx-1 px-2.5 py-0.5 rounded-lg bg-brass/15 text-brass hover:bg-brass/25 font-semibold text-xs border border-brass/30 transition truncate max-w-[220px]"
        >
          🌐 {domain} ↗
        </a>
      );
    }
    return part;
  });
}

function FormattedAnswer({ text }) {
  if (!text) return null;

  const lines = text.split("\n");
  return (
    <div className="space-y-3 text-ink/90 text-sm leading-relaxed">
      {lines.map((line, idx) => {
        const trimmed = line.trim();
        if (!trimmed) return null;

        if (trimmed.startsWith("### ") || trimmed.startsWith("## ")) {
          return (
            <h3 key={idx} className="font-display text-lg font-semibold text-moss pt-2 border-b border-moss/15 pb-1">
              {trimmed.replace(/^#+\s*/, "")}
            </h3>
          );
        }

        if (trimmed.startsWith("•") || trimmed.startsWith("-") || trimmed.startsWith("*")) {
          const content = trimmed.replace(/^[•\-\*]\s*/, "");
          return (
            <div key={idx} className="flex items-start gap-2.5 bg-moss/5 border border-moss/15 rounded-xl p-3 shadow-xs">
              <span className="text-moss font-bold mt-0.5">✦</span>
              <span className="flex-1">{formatUrlsInText(content)}</span>
            </div>
          );
        }

        return <p key={idx}>{formatUrlsInText(trimmed)}</p>;
      })}
    </div>
  );
}

export default function AskAi() {
  const [question, setQuestion] = useState("");
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.topics().then(setTopics).catch((err) => setError(err.message));
  }, []);

  async function handleAsk(promptText) {
    const q = promptText || question;
    if (!q.trim()) return;

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const data = await api.askAi(q, selectedTopic);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function onSubmit(event) {
    event.preventDefault();
    handleAsk(question);
  }

  return (
    <section className="max-w-3xl">
      <div className="border-b border-black/10 pb-6">
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-moss">RAG Question Answering</span>
        <h1 className="mt-2 font-display text-4xl font-semibold">Ask ChronoFlow AI</h1>
        <p className="mt-2 text-ink/70">
          Ask questions about historical events and evolution. Answers are generated using Retrieval-Augmented Generation (RAG) strictly backed by verified stored articles.
        </p>
      </div>

      <form className="mt-6" onSubmit={onSubmit}>
        <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
          <label className="text-sm font-semibold text-ink">Topic Context (Optional):</label>
          <select
            className="rounded-xl border border-black/15 bg-white px-3 py-1.5 text-sm text-ink font-medium focus:border-moss focus:outline-none shadow-xs"
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
          >
            <option value="">All Knowledge Bases</option>
            {topics.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>
        </div>

        <textarea
          className="h-32 w-full rounded-2xl border border-black/15 bg-white px-4 py-3 text-base shadow-sm transition placeholder:text-ink/40 focus:border-moss focus:outline-none focus:ring-2 focus:ring-moss/20"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="e.g. How did Artificial Intelligence evolve in 2023?"
          required
        />

        {/* Suggestion Chips */}
        <div className="mt-3 flex flex-wrap gap-2">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              type="button"
              onClick={() => {
                setQuestion(s);
                handleAsk(s);
              }}
              className="rounded-full border border-black/10 bg-white px-3 py-1 text-xs text-ink/70 transition hover:border-moss hover:bg-moss/10 hover:text-moss shadow-2xs"
            >
              💡 {s}
            </button>
          ))}
        </div>

        <button
          type="submit"
          className="mt-5 inline-flex items-center gap-2 rounded-xl bg-ink px-6 py-3 font-semibold text-parchment shadow-md transition hover:bg-moss disabled:opacity-50"
          disabled={loading || !question.trim()}
        >
          {loading ? (
            <>
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-parchment border-t-transparent" />
              Thinking…
            </>
          ) : (
            "Ask ChronoFlow AI"
          )}
        </button>
      </form>

      {error && <p className="mt-6 rounded-xl bg-red-100 p-4 text-sm text-red-800">{error}</p>}

      {result && (
        <div className="mt-8 rounded-2xl border border-black/15 bg-gradient-to-br from-white to-moss/5 p-6 shadow-xl space-y-4">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-moss">
            <span>✨ AI Answer</span>
          </div>

          <FormattedAnswer text={result.answer} />

          {result.sources?.length > 0 && (
            <div className="mt-6 border-t border-black/10 pt-4">
              <h2 className="text-xs font-semibold uppercase tracking-[0.2em] text-brass mb-3">
                📚 Cited Sources ({result.sources.length})
              </h2>
              <div className="grid gap-2 md:grid-cols-2">
                {result.sources.map((source) => {
                  const id = source.id || source.article_id;
                  return (
                    <Link
                      key={id}
                      to={`/articles/${id}`}
                      className="group flex items-center justify-between rounded-xl border border-black/10 bg-white/80 p-3 text-sm font-semibold text-moss transition hover:border-moss hover:bg-white shadow-xs"
                    >
                      <span className="truncate">{source.title}</span>
                      <span className="text-xs transition group-hover:translate-x-1">→</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
