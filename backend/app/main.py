import os
import sys
from pathlib import Path

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

from app.database.base import Base
from app.database.connection import engine

from app.models.topic import Topic
from app.models.tag import Tag
from app.models.article import Article
from app.models.user import User
from app.models.article_tag import article_tags

from app.routes import topic, tag, article, timeline, search, ai, auth

# Auto-create tables (SQLite or PostgreSQL)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChronoFlow API",
    description="AI-powered interactive timeline platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to ChronoFlow API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Direct routes
app.include_router(auth.router)
app.include_router(topic.router)
app.include_router(tag.router)
app.include_router(article.router)
app.include_router(timeline.router)
app.include_router(search.router)
app.include_router(ai.router)

# /api prefixed routes (for Vercel serverless proxy)
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