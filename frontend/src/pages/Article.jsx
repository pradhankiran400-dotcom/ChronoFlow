import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "../api";

function formatContentWithPills(contentStr) {
  if (!contentStr) return null;

  const lines = contentStr.split("\n");
  const urlRegex = /(https?:\/\/[^\s]+)/g;

  return lines.map((line, lineIdx) => {
    const trimmed = line.trim();
    if (!trimmed) return null;

    if (trimmed.startsWith("Full reporting at:") || trimmed.startsWith("http")) {
      const match = trimmed.match(urlRegex);
      if (match) {
        const url = match[0];
        let domain = "External Publisher";
        try {
          domain = new URL(url).hostname.replace("www.", "");
        } catch (e) {}
        return (
          <div key={lineIdx} className="my-3">
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-xl bg-brass/15 px-3.5 py-1.5 text-xs font-semibold text-brass hover:bg-brass/25 border border-brass/30 transition shadow-2xs"
            >
              🌐 Read Full Report on {domain} ↗
            </a>
          </div>
        );
      }
    }

    const parts = line.split(urlRegex);
    return (
      <p key={lineIdx} className="my-2 leading-relaxed text-ink/90">
        {parts.map((part, i) => {
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
                className="inline-flex items-center gap-1 mx-1 px-2.5 py-0.5 rounded-lg bg-moss/10 text-moss hover:bg-moss/20 font-semibold text-xs border border-moss/25 transition truncate max-w-[240px]"
              >
                🔗 {domain} ↗
              </a>
            );
          }
          return part;
        })}
      </p>
    );
  });
}

export default function Article() {
  const { articleId } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .article(articleId)
      .then(setArticle)
      .catch((err) => setError(err.message));
  }, [articleId]);

  if (error) {
    return <p className="rounded-xl bg-red-100 p-4 text-sm text-red-800">{error}</p>;
  }

  if (!article) {
    return <p className="text-ink/60">Loading article details…</p>;
  }

  let sourceDomain = "External Source";
  if (article.source_url) {
    try {
      sourceDomain = new URL(article.source_url).hostname.replace("www.", "");
    } catch (e) {}
  }

  return (
    <article className="max-w-3xl space-y-6">
      <Link
        to={article.topic_id ? `/timeline/${article.topic_id}` : "/timeline"}
        className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-[0.2em] text-moss hover:underline"
      >
        ← Back to Timeline
      </Link>

      <div className="flex flex-wrap items-center gap-3">
        <span className="font-mono text-sm font-semibold tracking-wide text-brass">
          📅 {article.event_date}
        </span>
        {article.topic && (
          <span className="rounded-md bg-black/5 px-2.5 py-0.5 text-xs font-medium text-ink">
            Topic: {article.topic.name}
          </span>
        )}
        {article.tags?.map((tag) => (
          <span key={tag.id} className="rounded-full bg-moss/10 px-2.5 py-0.5 text-xs font-medium text-moss">
            #{tag.name}
          </span>
        ))}
      </div>

      <h1 className="font-display text-4xl font-semibold leading-tight text-ink">
        {article.title}
      </h1>

      {article.summary && (
        <div className="rounded-2xl border-l-4 border-brass bg-brass/5 p-4 text-lg italic text-ink/80 shadow-xs">
          {article.summary}
        </div>
      )}

      <div className="rounded-2xl border border-black/10 bg-white p-6 shadow-sm space-y-3">
        {formatContentWithPills(article.content)}
      </div>

      <div className="flex flex-wrap items-center justify-between gap-4 border-t border-black/10 pt-6">
        {article.source_url ? (
          <a
            className="inline-flex items-center gap-2 rounded-xl bg-moss/10 px-4 py-2 text-xs font-semibold text-moss hover:bg-moss/20 border border-moss/20 transition shadow-xs"
            href={article.source_url}
            target="_blank"
            rel="noreferrer"
          >
            🌐 Original Source ({sourceDomain}) ↗
          </a>
        ) : (
          <span />
        )}

        <Link
          to="/ask"
          className="inline-flex items-center gap-2 rounded-xl bg-ink px-4 py-2.5 text-xs font-semibold text-parchment transition hover:bg-moss shadow-md"
        >
          ✨ Ask AI about this event →
        </Link>
      </div>
    </article>
  );
}
