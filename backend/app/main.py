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

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session

from app.database.base import Base
from app.database.connection import engine, SessionLocal

from app.models.topic import Topic
from app.models.tag import Tag
from app.models.article import Article
from app.models.user import User
from app.models.article_tag import article_tags

from app.routes import topic, tag, article, timeline, search, ai, auth


def seed_default_data(db: Session):
    """Seed sample data if DB is completely empty."""
    try:
        if db.query(Topic).count() == 0:
            ai_topic = Topic(name="Artificial Intelligence", description="Key breakthroughs in AI, LLMs, and intelligent systems.")
            space_topic = Topic(name="Space Exploration", description="Milestones in space missions, telescopes, and lunar exploration.")
            climate_topic = Topic(name="Climate & Science", description="Developments in climate science, renewable energy, and planet Earth.")
            db.add_all([ai_topic, space_topic, climate_topic])
            db.commit()

            ai_tag = Tag(name="AI")
            space_tag = Tag(name="Space")
            tech_tag = Tag(name="Technology")
            db.add_all([ai_tag, space_tag, tech_tag])
            db.commit()

            from datetime import date
            a1 = Article(
                title="ChatGPT Public Launch",
                summary="OpenAI released ChatGPT, bringing conversational AI to hundreds of millions.",
                content="ChatGPT was released for public access in November 2022, rapidly becoming one of the fastest-growing consumer applications in history.",
                source_url="https://openai.com/blog/chatgpt",
                event_date=date(2022, 11, 30),
                topic_id=ai_topic.id,
                tags=[ai_tag, tech_tag]
            )
            a2 = Article(
                title="James Webb First Deep Field",
                summary="NASA unveiled the first full-color deep space images from the James Webb Space Telescope.",
                content="The James Webb Space Telescope delivered infrared images showing galaxy clusters billions of light-years away in July 2022.",
                source_url="https://nasa.gov/webbfirstimages",
                event_date=date(2022, 7, 12),
                topic_id=space_topic.id,
                tags=[space_tag, tech_tag]
            )
            db.add_all([a1, a2])
            db.commit()
    except Exception as exc:
        print(f"Seed notice: {exc}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and initial data asynchronously on server startup
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            seed_default_data(db)
        finally:
            db.close()
    except Exception as exc:
        print(f"Notice: Database schema creation: {exc}")
    yield


app = FastAPI(
    title="ChronoFlow API",
    description="AI-powered interactive timeline platform",
    version="1.0.0",
    lifespan=lifespan
)

# Normalize request path if Vercel serverless rewrites include script filename
class PathNormalizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.scope.get("path", "")
        if path.startswith("/api/index.py"):
            stripped = path[len("/api/index.py"):] or "/"
            request.scope["path"] = stripped
        elif path.startswith("/index.py"):
            stripped = path[len("/index.py"):] or "/"
            request.scope["path"] = stripped
        return await call_next(request)

app.add_middleware(PathNormalizeMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Static directory resolution (backend/app/static or frontend/dist)
STATIC_DIR = _APP_DIR / "static" if (_APP_DIR / "static").exists() else (_ROOT_DIR / "frontend" / "dist")
assets_dir = STATIC_DIR / "assets"
if assets_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Direct API routes (e.g. /topics, /articles, /auth, etc.)
app.include_router(auth.router)
app.include_router(topic.router)
app.include_router(tag.router)
app.include_router(article.router)
app.include_router(timeline.router)
app.include_router(search.router)
app.include_router(ai.router)

# /api prefixed routes (e.g. /api/topics, /api/articles, /api/health)
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
    return {"message": "Welcome to ChronoFlow API", "status": "online"}


@api_router.get("/health")
def api_health():
    return {"status": "healthy"}


app.include_router(api_router)


import mimetypes

MIME_TYPES = {
    ".js": "application/javascript",
    ".mjs": "application/javascript",
    ".css": "text/css",
    ".html": "text/html",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
}

def get_mime_type(path: Path) -> str:
    ext = path.suffix.lower()
    return MIME_TYPES.get(ext, mimetypes.guess_type(str(path))[0] or "application/octet-stream")


# Serve Frontend React Single Page Application (SPA)
@app.get("/")
def home():
    index_file = STATIC_DIR / "index.html"
    if index_file.is_file():
        return FileResponse(str(index_file), media_type="text/html")
    return {
        "message": "Welcome to ChronoFlow API",
        "status": "online",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/{full_path:path}")
def serve_spa(full_path: str):
    # Pass through API and OpenAPI/Docs endpoints
    if full_path.startswith("api/") or full_path == "api" or full_path.startswith("docs") or full_path.startswith("openapi.json"):
        raise HTTPException(status_code=404, detail="Not Found")
    
    file_path = STATIC_DIR / full_path
    if full_path and file_path.is_file():
        return FileResponse(str(file_path), media_type=get_mime_type(file_path))
    
    index_file = STATIC_DIR / "index.html"
    if index_file.is_file():
        return FileResponse(str(index_file), media_type="text/html")
    
    raise HTTPException(status_code=404, detail="Not Found")