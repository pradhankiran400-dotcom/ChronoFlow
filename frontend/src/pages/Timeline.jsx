import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "../api";

export default function Timeline() {
  const { topicId } = useParams();
  const navigate = useNavigate();

  const [topics, setTopics] = useState([]);
  const [tags, setTags] = useState([]);
  const [selectedTag, setSelectedTag] = useState("");
  const [selectedTopicObj, setSelectedTopicObj] = useState(null);
  const [events, setEvents] = useState([]);
  const [query, setQuery] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Load topics & tags list
  useEffect(() => {
    Promise.all([api.topics(), api.tags()])
      .then(([topicList, tagList]) => {
        setTopics(topicList);
        setTags(tagList);
      })
      .catch((err) => setError(err.message));
  }, []);

  // Fetch timeline data whenever filters change
  useEffect(() => {
    setLoading(true);
    setError("");
    api.timeline({
      topic_id: topicId || undefined,
      tag_id: selectedTag || undefined,
      start_date: startDate || undefined,
      end_date: endDate || undefined,
      search: query.trim() || undefined,
    })
      .then((data) => {
        setEvents(data.events || []);
        setSelectedTopicObj(data.topic || null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [topicId, selectedTag, startDate, endDate, query]);

  return (
    <section>
      {/* Header */}
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-black/10 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-moss">
            <span>Interactive Timeline</span>
            {selectedTopicObj && <span className="rounded bg-moss/10 px-2 py-0.5 text-moss">{selectedTopicObj.name}</span>}
          </div>
          <h1 className="mt-2 font-display text-4xl font-semibold text-ink">
            {selectedTopicObj ? selectedTopicObj.name : "Chronological Evolution"}
          </h1>
          {selectedTopicObj?.description && (
            <p className="mt-2 max-w-2xl text-ink/70">{selectedTopicObj.description}</p>
          )}
        </div>

        {/* Topic Selector & Sync Live Button */}
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => {
              if (!topicId && topics.length > 0) {
                alert("Please select a specific topic to sync live news.");
                return;
              }
              const targetTopic = topicId || (topics[0] ? topics[0].id : 1);
              setLoading(true);
              api.syncLiveArticles(targetTopic)
                .then((newArticles) => {
                  alert(`Successfully synced ${newArticles.length} new live articles!`);
                  // Refresh timeline
                  return api.timeline({
                    topic_id: topicId || undefined,
                    tag_id: selectedTag || undefined,
                    start_date: startDate || undefined,
                    end_date: endDate || undefined,
                    search: query.trim() || undefined,
                  });
                })
                .then((data) => {
                  if (data) setEvents(data.events || []);
                })
                .catch((err) => setError(err.message))
                .finally(() => setLoading(false));
            }}
            disabled={loading}
            className="inline-flex items-center gap-1.5 rounded-xl bg-brass px-4 py-2.5 text-sm font-semibold text-ink shadow-sm transition hover:bg-brass/90 disabled:opacity-50"
          >
            ⚡ Sync Live News
          </button>

          <select
            className="rounded-xl border border-black/15 bg-white px-4 py-2.5 text-sm font-medium shadow-sm transition hover:border-moss focus:outline-none focus:ring-2 focus:ring-moss/20"
            value={topicId || ""}
            onChange={(event) => {
              const val = event.target.value;
              navigate(val ? `/timeline/${val}` : "/timeline");
            }}
          >
            <option value="">All Topics</option>
            {topics.map((topic) => (
              <option key={topic.id} value={topic.id}>
                {topic.name}
              </option>
            ))}
          </select>
        </div>
      </div>


      {/* Filter Toolbar */}
      <div className="mt-6 grid gap-4 rounded-2xl border border-black/10 bg-white/60 p-4 backdrop-blur md:grid-cols-4">
        <div className="relative">
          <input
            className="w-full rounded-xl border border-black/15 bg-white px-3.5 py-2.5 text-sm transition placeholder:text-ink/40 focus:border-moss focus:outline-none"
            placeholder="Search keywords…"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="absolute right-3 top-2.5 text-xs text-ink/40 hover:text-ink"
            >
              Clear
            </button>
          )}
        </div>

        {/* Tag Filter */}
        <select
          className="rounded-xl border border-black/15 bg-white px-3.5 py-2.5 text-sm text-ink transition focus:border-moss focus:outline-none"
          value={selectedTag}
          onChange={(event) => setSelectedTag(event.target.value)}
        >
          <option value="">All Tags</option>
          {tags.map((tag) => (
            <option key={tag.id} value={tag.id}>
              #{tag.name}
            </option>
          ))}
        </select>

        {/* Start Date */}
        <input
          type="date"
          className="rounded-xl border border-black/15 bg-white px-3.5 py-2.5 text-sm text-ink transition focus:border-moss focus:outline-none"
          value={startDate}
          onChange={(event) => setStartDate(event.target.value)}
        />

        {/* End Date */}
        <input
          type="date"
          className="rounded-xl border border-black/15 bg-white px-3.5 py-2.5 text-sm text-ink transition focus:border-moss focus:outline-none"
          value={endDate}
          onChange={(event) => setEndDate(event.target.value)}
        />
      </div>

      {/* Reset Filters button if active */}
      {(query || selectedTag || startDate || endDate) && (
        <div className="mt-3 flex justify-end">
          <button
            onClick={() => {
              setQuery("");
              setSelectedTag("");
              setStartDate("");
              setEndDate("");
            }}
            className="text-xs font-semibold text-moss underline hover:text-ink"
          >
            Reset Filters
          </button>
        </div>
      )}

      {error && <p className="mt-6 rounded-xl bg-red-100 p-4 text-sm text-red-800">{error}</p>}

      {/* Timeline Rail */}
      {loading ? (
        <div className="mt-12 space-y-6 pl-8">
          <div className="h-20 animate-pulse rounded-2xl bg-black/5" />
          <div className="h-20 animate-pulse rounded-2xl bg-black/5" />
        </div>
      ) : (
        <ol className="timeline-rail mt-10 space-y-10 pl-8">
          {events.map((event) => (
            <li key={event.id} className="group relative transition hover:-translate-y-0.5">
              {/* Node Marker */}
              <span className="absolute -left-[37px] top-2 h-4 w-4 rounded-full border-2 border-brass bg-parchment transition group-hover:scale-125 group-hover:bg-brass group-hover:shadow-md" />

              <div className="rounded-2xl border border-black/10 bg-white p-6 shadow-sm transition hover:border-moss/40 hover:shadow-md">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="font-mono text-sm font-semibold tracking-wide text-brass">
                    📅 {event.event_date}
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {event.tags?.map((tag) => (
                      <span key={tag.id} className="rounded-full bg-moss/10 px-2.5 py-0.5 text-xs font-medium text-moss">
                        #{tag.name}
                      </span>
                    ))}
                  </div>
                </div>

                <Link
                  to={`/articles/${event.id}`}
                  className="mt-2 block font-display text-2xl font-semibold text-ink hover:text-moss"
                >
                  {event.title}
                </Link>

                {event.summary && <p className="mt-2 text-ink/70 leading-relaxed">{event.summary}</p>}

                <div className="mt-4 flex items-center justify-between text-xs text-ink/50">
                  {event.source_url && (
                    <a
                      href={event.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-moss underline"
                    >
                      Original Source ↗
                    </a>
                  )}
                  <Link to={`/articles/${event.id}`} className="font-semibold text-moss hover:underline">
                    Read Article →
                  </Link>
                </div>
              </div>
            </li>
          ))}
        </ol>
      )}

      {!loading && events.length === 0 && !error && (
        <div className="mt-12 rounded-2xl border border-dashed border-black/20 p-10 text-center text-ink/60">
          <p className="text-lg font-medium">No events found matching your filter criteria.</p>
          <p className="mt-1 text-sm">Try clearing filters or selecting another topic.</p>
        </div>
      )}
    </section>
  );
}

