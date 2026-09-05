import { useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Timeline from "./pages/Timeline.jsx";
import Article from "./pages/Article.jsx";
import Search from "./pages/Search.jsx";
import AskAi from "./pages/AskAi.jsx";
import Manage from "./pages/Manage.jsx";
import { AuthProvider, useAuth } from "./context/AuthContext.jsx";

const links = [
  ["/", "Topics"],
  ["/timeline", "Timeline"],
  ["/search", "Search"],
  ["/ask", "Ask AI"],
  ["/manage", "Manage"],
];

function HeaderNav() {
  const { user, logout, loginWithGoogle, showLoginModal, setShowLoginModal } = useAuth();
  const [emailInput, setEmailInput] = useState("");
  const [nameInput, setNameInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [authError, setAuthError] = useState("");

  async function handleGmailSubmit(e) {
    e.preventDefault();
    if (!emailInput || !emailInput.includes("@")) {
      setAuthError("Please enter a valid Gmail / Google email address.");
      return;
    }
    setLoading(true);
    setAuthError("");
    try {
      await loginWithGoogle({
        email: emailInput,
        name: nameInput || emailInput.split("@")[0].replace(".", " ").toUpperCase(),
        picture: `https://api.dicebear.com/7.x/avataaars/svg?seed=${emailInput}`,
        google_id: `google_${Date.now()}`
      });
      setEmailInput("");
      setNameInput("");
    } catch (err) {
      setAuthError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <header className="border-b border-black/10 bg-ink text-parchment shadow-md">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-4">
          <NavLink to="/" className="font-display text-2xl tracking-tight text-white flex items-center gap-2">
            <span>⏳</span> ChronoFlow
          </NavLink>

          <div className="flex flex-wrap items-center gap-6">
            <nav className="flex flex-wrap items-center gap-5 text-sm font-medium">
              {links.map(([to, label]) => (
                <NavLink
                  key={to}
                  to={to}
                  end={to === "/"}
                  className={({ isActive }) =>
                    isActive ? "text-brass font-semibold" : "text-parchment/80 hover:text-parchment transition"
                  }
                >
                  {label}
                </NavLink>
              ))}
            </nav>

            {/* Auth Badge & Buttons */}
            {user ? (
              <div className="flex items-center gap-3 bg-white/10 px-3 py-1.5 rounded-xl border border-white/15">
                <img
                  src={user.picture || `https://api.dicebear.com/7.x/bottts/svg?seed=${user.email}`}
                  alt={user.name}
                  className="h-7 w-7 rounded-full bg-brass/30 object-cover border border-brass/50"
                />
                <div className="text-left text-xs">
                  <p className="font-semibold text-white leading-tight">{user.name}</p>
                  <p className="text-[10px] text-parchment/60 leading-tight">{user.email}</p>
                </div>
                <button
                  onClick={logout}
                  className="ml-2 rounded-lg bg-red-500/20 px-2.5 py-1 text-xs font-semibold text-red-300 transition hover:bg-red-500/30 hover:text-red-200"
                >
                  Logout
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowLoginModal(true)}
                className="inline-flex items-center gap-2 rounded-xl bg-white px-3.5 py-1.5 text-xs font-semibold text-ink shadow hover:bg-parchment transition"
              >
                <svg className="h-4 w-4" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                  />
                </svg>
                Sign in with Google
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Gmail / Google Login Modal */}
      {showLoginModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl space-y-5 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between border-b border-black/10 pb-3">
              <div className="flex items-center gap-2">
                <svg className="h-6 w-6" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                  />
                </svg>
                <h3 className="font-display text-xl font-semibold text-ink">Sign in with Gmail</h3>
              </div>
              <button
                onClick={() => setShowLoginModal(false)}
                className="text-ink/50 hover:text-ink text-lg font-bold"
              >
                ✕
              </button>
            </div>

            <p className="text-sm text-ink/70">
              Sign in with your Gmail account to manage content, trigger live news ingestion, and access personalized AI insights.
            </p>

            <form onSubmit={handleGmailSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold uppercase text-ink/70 mb-1">Gmail Address</label>
                <input
                  type="email"
                  required
                  placeholder="alex.developer@gmail.com"
                  className="w-full rounded-xl border border-black/15 px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-moss/30"
                  value={emailInput}
                  onChange={(e) => setEmailInput(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-ink/70 mb-1">Full Name (Optional)</label>
                <input
                  type="text"
                  placeholder="Alex Developer"
                  className="w-full rounded-xl border border-black/15 px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-moss/30"
                  value={nameInput}
                  onChange={(e) => setNameInput(e.target.value)}
                />
              </div>

              {authError && <p className="text-xs text-red-600 font-medium">{authError}</p>}

              <div className="flex items-center gap-3 pt-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 rounded-xl bg-ink py-2.5 text-sm font-semibold text-parchment hover:bg-ink/90 disabled:opacity-50 transition"
                >
                  {loading ? "Authenticating..." : "Continue with Gmail"}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    // Quick Demo Login
                    loginWithGoogle({
                      email: "user.demo@gmail.com",
                      name: "ChronoFlow Demo User",
                      picture: "https://api.dicebear.com/7.x/avataaars/svg?seed=chronoflow_user",
                      google_id: "google_demo_123"
                    });
                  }}
                  className="rounded-xl border border-black/15 bg-slate-100 px-4 py-2.5 text-sm font-semibold text-ink hover:bg-slate-200 transition"
                >
                  Quick Demo Login
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen">
        <HeaderNav />
        <main className="mx-auto max-w-6xl px-6 py-10">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/timeline/:topicId" element={<Timeline />} />
            <Route path="/articles/:articleId" element={<Article />} />
            <Route path="/search" element={<Search />} />
            <Route path="/ask" element={<AskAi />} />
            <Route path="/manage" element={<Manage />} />
          </Routes>
        </main>
      </div>
    </AuthProvider>
  );
}
