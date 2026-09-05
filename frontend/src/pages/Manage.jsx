import { useEffect, useState } from "react";
import { api } from "../api";
import { useAuth } from "../context/AuthContext.jsx";

const emptyArticle = {
  title: "",
  summary: "",
  content: "",
  source_url: "",
  event_date: "",
  topic_id: "",
  tag_ids: [],
};

export default function Manage() {
  const { user, setShowLoginModal } = useAuth();
  const [topics, setTopics] = useState([]);
  const [tags, setTags] = useState([]);
  const [articles, setArticles] = useState([]);
  const [topicForm, setTopicForm] = useState({ name: "", description: "" });
  const [tagName, setTagName] = useState("");
  const [articleForm, setArticleForm] = useState(emptyArticle);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");


  function reload() {
    return Promise.all([api.topics(), api.tags(), api.articles()]).then(([topicList, tagList, articleList]) => {
      setTopics(topicList);
      setTags(tagList);
      setArticles(articleList);
    });
  }

  useEffect(() => {
    reload().catch((err) => setError(err.message));
  }, []);

  async function handle(action) {
    setError("");
    setMessage("");
    try {
      await action();
      await reload();
    } catch (err) {
      setError(err.message);
    }
  }

  function toggleTag(tagId) {
    setArticleForm((prev) => {
      const exists = prev.tag_ids.includes(tagId);
      const nextTags = exists
        ? prev.tag_ids.filter((id) => id !== tagId)
        : [...prev.tag_ids, tagId];
      return { ...prev, tag_ids: nextTags };
    });
  }

  const [syncTopicId, setSyncTopicId] = useState("");
  const [syncQuery, setSyncQuery] = useState("");
  const [syncing, setSyncing] = useState(false);

  return (
    <section className="grid gap-8 lg:grid-cols-2 max-w-6xl">
      <div className="lg:col-span-2 border-b border-black/10 pb-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <span className="text-xs font-semibold uppercase tracking-[0.2em] text-moss">Content Admin</span>
          <h1 className="mt-1 font-display text-4xl font-semibold">Manage Content & Real-Time Feeds</h1>
        </div>
      </div>

      {!user && (
        <div className="lg:col-span-2 rounded-2xl bg-amber-500/10 border border-amber-500/30 p-4 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-xl">🔒</span>
            <div>
              <p className="text-sm font-semibold text-ink">Admin Session Required</p>
              <p className="text-xs text-ink/70">Sign in with your Gmail account to manage topics, create articles, and execute live news syncs.</p>
            </div>
          </div>
          <button
            onClick={() => setShowLoginModal(true)}
            className="rounded-xl bg-ink px-4 py-2 text-xs font-semibold text-parchment hover:bg-ink/90 transition shadow-sm"
          >
            Sign in with Gmail
          </button>
        </div>
      )}


      {/* Live News Sync Card */}
      <form
        className="space-y-4 rounded-2xl border border-brass/30 bg-gradient-to-br from-white to-brass/5 p-6 shadow-sm lg:col-span-2"
        onSubmit={(event) => {
          event.preventDefault();
          if (!syncTopicId) {
            setError("Please select a target topic for the live sync.");
            return;
          }
          setSyncing(true);
          handle(async () => {
            const res = await api.syncLiveArticles(syncTopicId, syncQuery);
            setMessage(`Successfully fetched and ingested ${res.length} live articles!`);
            setSyncQuery("");
          }).finally(() => setSyncing(false));
        }}
      >
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-brass">
          <span>⚡ Real-Time External News Fetcher</span>
        </div>
        <h2 className="font-display text-2xl font-semibold text-ink">Fetch Live Articles</h2>
        <p className="text-sm text-ink/70">
          Query external APIs (NewsAPI, GNews, HackerNews, Wikipedia) to automatically ingest real-time news events into your timeline.
        </p>

        <div className="grid gap-4 md:grid-cols-3">
          <select
            className="rounded-xl border border-black/15 bg-white px-4 py-2.5 text-sm"
            value={syncTopicId}
            onChange={(e) => setSyncTopicId(e.target.value)}
            required
          >
            <option value="">Select Target Topic</option>
            {topics.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>

          <input
            className="rounded-xl border border-black/15 bg-white px-4 py-2.5 text-sm md:col-span-2"
            placeholder="Custom Search Keywords (e.g. 'GPT-5' or 'Moon mission')"
            value={syncQuery}
            onChange={(e) => setSyncQuery(e.target.value)}
          />
        </div>

        <button
          disabled={syncing}
          className="inline-flex items-center gap-2 rounded-xl bg-brass px-6 py-3 text-sm font-semibold text-ink transition hover:bg-brass/90 disabled:opacity-50"
        >
          {syncing ? "Fetching Real-Time Articles…" : "⚡ Fetch Live Articles Now"}
        </button>
      </form>


      {error && <p className="rounded-xl bg-red-100 p-4 text-sm text-red-800 lg:col-span-2">{error}</p>}
      {message && <p className="rounded-xl bg-green-100 p-4 text-sm text-green-900 lg:col-span-2">{message}</p>}

      {/* New Topic */}
      <form
        className="space-y-4 rounded-2xl border border-black/10 bg-white p-6 shadow-sm"
        onSubmit={(event) => {
          event.preventDefault();
          handle(async () => {
            await api.createTopic(topicForm);
            setTopicForm({ name: "", description: "" });
            setMessage("Topic created successfully.");
          });
        }}
      >
        <h2 className="font-display text-2xl font-semibold">New Topic</h2>
        <input
          className="w-full rounded-xl border border-black/15 px-4 py-2.5 text-sm"
          placeholder="Topic Title (e.g. Artificial Intelligence)"
          value={topicForm.name}
          onChange={(event) => setTopicForm({ ...topicForm, name: event.target.value })}
          required
        />
        <textarea
          className="w-full rounded-xl border border-black/15 px-4 py-2.5 text-sm"
          placeholder="Topic Description"
          value={topicForm.description}
          onChange={(event) => setTopicForm({ ...topicForm, description: event.target.value })}
        />
        <button className="rounded-xl bg-ink px-5 py-2.5 text-sm font-semibold text-parchment transition hover:bg-moss">
          Create Topic
        </button>

        <div className="mt-4 pt-4 border-t border-black/10">
          <p className="text-xs font-semibold uppercase text-moss mb-2">Existing Topics ({topics.length})</p>
          <div className="space-y-2">
            {topics.map((t) => (
              <div key={t.id} className="flex items-center justify-between text-sm bg-black/5 p-2 rounded-lg">
                <span className="font-medium">{t.name}</span>
                <button
                  type="button"
                  onClick={() => handle(() => api.deleteTopic(t.id))}
                  className="text-xs text-red-600 hover:underline"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        </div>
      </form>

      {/* New Tag */}
      <form
        className="space-y-4 rounded-2xl border border-black/10 bg-white p-6 shadow-sm"
        onSubmit={(event) => {
          event.preventDefault();
          handle(async () => {
            await api.createTag({ name: tagName });
            setTagName("");
            setMessage("Tag created successfully.");
          });
        }}
      >
        <h2 className="font-display text-2xl font-semibold">New Tag</h2>
        <input
          className="w-full rounded-xl border border-black/15 px-4 py-2.5 text-sm"
          placeholder="Tag Name (e.g. LLM)"
          value={tagName}
          onChange={(event) => setTagName(event.target.value)}
          required
        />
        <button className="rounded-xl bg-ink px-5 py-2.5 text-sm font-semibold text-parchment transition hover:bg-moss">
          Create Tag
        </button>

        <div className="mt-4 pt-4 border-t border-black/10">
          <p className="text-xs font-semibold uppercase text-moss mb-2">Existing Tags ({tags.length})</p>
          <div className="flex flex-wrap gap-2">
            {tags.map((t) => (
              <span key={t.id} className="inline-flex items-center gap-1.5 rounded-full bg-moss/10 px-3 py-1 text-xs font-medium text-moss">
                #{t.name}
                <button
                  type="button"
                  onClick={() => handle(() => api.deleteTag(t.id))}
                  className="ml-1 text-red-600 hover:text-red-800"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>
      </form>

      {/* New Article Form */}
      <form
        className="space-y-4 rounded-2xl border border-black/10 bg-white p-6 shadow-sm lg:col-span-2"
        onSubmit={(event) => {
          event.preventDefault();
          handle(async () => {
            await api.createArticle({
              ...articleForm,
              topic_id: Number(articleForm.topic_id),
              source_url: articleForm.source_url || null,
            });
            setArticleForm(emptyArticle);
            setMessage("Article created successfully.");
          });
        }}
      >
        <h2 className="font-display text-2xl font-semibold">New Article</h2>

        <div className="grid gap-4 md:grid-cols-2">
          <input
            className="rounded-xl border border-black/15 px-4 py-2.5 text-sm"
            placeholder="Article Title"
            value={articleForm.title}
            onChange={(event) => setArticleForm({ ...articleForm, title: event.target.value })}
            required
          />
          <input
            type="date"
            className="rounded-xl border border-black/15 px-4 py-2.5 text-sm"
            value={articleForm.event_date}
            onChange={(event) => setArticleForm({ ...articleForm, event_date: event.target.value })}
            required
          />
          <select
            className="rounded-xl border border-black/15 px-4 py-2.5 text-sm"
            value={articleForm.topic_id}
            onChange={(event) => setArticleForm({ ...articleForm, topic_id: event.target.value })}
            required
          >
            <option value="">Select Topic</option>
            {topics.map((topic) => (
              <option key={topic.id} value={topic.id}>
                {topic.name}
              </option>
            ))}
          </select>
          <input
            className="rounded-xl border border-black/15 px-4 py-2.5 text-sm"
            placeholder="Source URL (Optional)"
            value={articleForm.source_url}
            onChange={(event) => setArticleForm({ ...articleForm, source_url: event.target.value })}
          />
        </div>

        {/* Multi-Tag Selector */}
        {tags.length > 0 && (
          <div>
            <label className="block text-xs font-semibold uppercase text-moss mb-1.5">Assign Tags:</label>
            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => {
                const checked = articleForm.tag_ids.includes(tag.id);
                return (
                  <button
                    key={tag.id}
                    type="button"
                    onClick={() => toggleTag(tag.id)}
                    className={`rounded-full px-3 py-1 text-xs font-semibold transition ${
                      checked
                        ? "bg-moss text-white shadow-sm"
                        : "bg-black/5 text-ink/70 hover:bg-black/10"
                    }`}
                  >
                    {checked ? "✓ " : "+ "}#{tag.name}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        <input
          className="w-full rounded-xl border border-black/15 px-4 py-2.5 text-sm"
          placeholder="Brief Summary"
          value={articleForm.summary}
          onChange={(event) => setArticleForm({ ...articleForm, summary: event.target.value })}
        />

        <textarea
          className="h-32 w-full rounded-xl border border-black/15 px-4 py-2.5 text-sm leading-relaxed"
          placeholder="Full Article Content"
          value={articleForm.content}
          onChange={(event) => setArticleForm({ ...articleForm, content: event.target.value })}
          required
        />

        <button className="rounded-xl bg-ink px-6 py-3 text-sm font-semibold text-parchment transition hover:bg-moss">
          Create Article
        </button>
      </form>

      {/* Articles Management Table */}
      <div className="rounded-2xl border border-black/10 bg-white p-6 shadow-sm lg:col-span-2">
        <h2 className="font-display text-2xl font-semibold mb-4">Existing Articles ({articles.length})</h2>
        <div className="divide-y divide-black/10">
          {articles.map((art) => (
            <div key={art.id} className="py-3 flex flex-wrap items-center justify-between gap-2">
              <div>
                <span className="font-mono text-xs text-brass mr-3">{art.event_date}</span>
                <span className="font-semibold text-ink">{art.title}</span>
                {art.tags?.length > 0 && (
                  <span className="ml-2 text-xs text-moss">
                    ({art.tags.map((t) => `#${t.name}`).join(" ")})
                  </span>
                )}
              </div>
              <button
                type="button"
                onClick={() => handle(() => api.deleteArticle(art.id))}
                className="text-xs font-semibold text-red-600 hover:underline"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

