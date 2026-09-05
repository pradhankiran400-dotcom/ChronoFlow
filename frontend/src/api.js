const API = import.meta.env.VITE_API_BASE_URL || "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const text = await response.text();
      try {
        const body = JSON.parse(text);
        detail = body.detail || text;
      } catch {
        detail = text || detail;
      }
    } catch {
      // ignore
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }


  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function buildQuery(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      query.append(key, value);
    }
  });
  const str = query.toString();
  return str ? `?${str}` : "";
}

export const api = {
  health: () => request("/health"),

  // Topics
  topics: () => request("/topics/"),
  topic: (id) => request(`/topics/${id}`),
  createTopic: (payload) =>
    request("/topics/", { method: "POST", body: JSON.stringify(payload) }),
  updateTopic: (id, payload) =>
    request(`/topics/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteTopic: (id) =>
    request(`/topics/${id}`, { method: "DELETE" }),

  // Tags
  tags: () => request("/tags"),
  createTag: (payload) =>
    request("/tags", { method: "POST", body: JSON.stringify(payload) }),
  updateTag: (id, payload) =>
    request(`/tags/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteTag: (id) =>
    request(`/tags/${id}`, { method: "DELETE" }),

  // Articles
  articles: (topicId) => request(`/articles${buildQuery({ topic_id: topicId })}`),
  article: (id) => request(`/articles/${id}`),
  createArticle: (payload) =>
    request("/articles", { method: "POST", body: JSON.stringify(payload) }),
  updateArticle: (id, payload) =>
    request(`/articles/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteArticle: (id) =>
    request(`/articles/${id}`, { method: "DELETE" }),
  syncLiveArticles: (topicId, query = "", maxResults = 8) =>
    request(`/articles/sync-live${buildQuery({ topic_id: topicId, query, max_results: maxResults })}`, {
      method: "POST",
    }),


  // Timeline & Search
  timeline: (params) => request(`/timeline${buildQuery(params)}`),
  search: (q, topicId) => request(`/search${buildQuery({ q, topic_id: topicId })}`),
  aiSearch: (q, topicId) => request(`/ai/search${buildQuery({ q, topic_id: topicId })}`),

  // AI RAG
  askAi: (question, topicId) =>
    request("/ai/ask", {
      method: "POST",
      body: JSON.stringify({ question, topic_id: topicId ? Number(topicId) : null }),
    }),

  // Auth
  loginGoogle: (payload) =>
    request("/auth/google", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getMe: (userId) => request(`/auth/me/${userId}`),
};


