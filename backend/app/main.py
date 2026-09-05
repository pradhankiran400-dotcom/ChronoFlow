import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Ensure backend, ai_ml, and root paths are always on sys.path for cloud runtimes (Vercel, Render, AWS)
_CURRENT_FILE = Path(__file__).resolve()
_APP_DIR = _CURRENT_FILE.parent
_BACKEND_DIR = _APP_DIR.parent
_ROOT_DIR = _BACKEND_DIR.parent

for _p in [str(_BACKEND_DIR), str(_ROOT_DIR), str(_ROOT_DIR / "ai_ml")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.database.base import Base
from app.database.connection import engine

from app.models.topic import Topic
from app.models.tag import Tag
from app.models.article import Article
from app.models.user import User
from app.models.article_tag import article_tags

from app.routes import topic, tag, article, timeline, search, ai, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables asynchronously on server startup
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        print(f"Notice: Database schema creation: {exc}")
    yield


app = FastAPI(
    title="ChronoFlow API",
    description="AI-powered interactive timeline platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Direct API routes
app.include_router(auth.router)
app.include_router(topic.router)
app.include_router(tag.router)
app.include_router(article.router)
app.include_router(timeline.router)
app.include_router(search.router)
app.include_router(ai.router)

# /api prefixed routes (for frontend and reverse proxies)
api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(topic.router)
api_router.include_router(tag.router)
api_router.include_router(article.router)
api_router.include_router(timeline.router)
api_router.include_router(search.router)
api_router.include_router(ai.router)


@api_router.get("/")
def api_home():
    return {"message": "Welcome to ChronoFlow API"}


@api_router.get("/health")
def api_health():
    return {"status": "healthy"}


app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Serve static frontend SPA build if present
_FRONTEND_DIST = _ROOT_DIR / "frontend" / "dist"
if _FRONTEND_DIST.exists() and (_FRONTEND_DIST / "index.html").exists():
    _ASSETS_DIR = _FRONTEND_DIST / "assets"
    if _ASSETS_DIR.exists():
        app.mount("/assets", StaticFiles(directory=str(_ASSETS_DIR)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi"):
            return JSONResponse(status_code=404, content={"detail": "Not Found"})
        target_file = _FRONTEND_DIST / full_path
        if target_file.is_file():
            return FileResponse(str(target_file))
        return FileResponse(str(_FRONTEND_DIST / "index.html"))
else:
    @app.get("/")
    def root_home():
        return {
            "message": "Welcome to ChronoFlow API",
            "docs": "/docs",
            "health": "/health"
        }