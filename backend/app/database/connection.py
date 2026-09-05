import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
logger = logging.getLogger(__name__)

BACKEND_DIR = Path(__file__).resolve().parents[2]
is_serverless = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

if is_serverless:
    DEFAULT_DB_PATH = Path("/tmp/chronoflow.db")
else:
    DEFAULT_DB_PATH = BACKEND_DIR / "chronoflow.db"

RAW_DB_URL = os.getenv("DATABASE_URL", "").strip()


def get_database_url() -> str:
    if not RAW_DB_URL:
        return f"sqlite:///{DEFAULT_DB_PATH}"

    # In serverless cloud (Vercel), localhost is unreachable
    if is_serverless and ("localhost" in RAW_DB_URL or "127.0.0.1" in RAW_DB_URL):
        logger.info("Serverless environment detected with localhost DB URL; falling back to SQLite.")
        return f"sqlite:///{DEFAULT_DB_PATH}"

    url = RAW_DB_URL
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+pg8000://", 1)
    elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
        url = url.replace("postgresql://", "postgresql+pg8000://", 1)

    return url


DATABASE_URL = get_database_url()

connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args["check_same_thread"] = False

try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
except Exception as exc:
    logger.warning(f"Error creating primary engine ({exc}). Using SQLite fallback.")
    DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Flag to track if DB tables and seed data have been initialized this process/cold start
_db_initialized = False


def _ensure_db():
    """Create tables and seed initial data once per cold start. Safe to call multiple times."""
    global _db_initialized, engine, SessionLocal
    if _db_initialized:
        return
    _db_initialized = True

    # 1. Verify engine connectivity; if unreachable, fallback to SQLite
    try:
        with engine.connect() as conn:
            pass
    except Exception as exc:
        logger.warning(f"Primary DB connection failed ({exc}). Falling back to SQLite: {DEFAULT_DB_PATH}")
        fallback_url = f"sqlite:///{DEFAULT_DB_PATH}"
        engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
        SessionLocal.configure(bind=engine)

    # 2. Import all models so Base.metadata is fully populated with all table schemas
    try:
        from app.database.base import Base
        import app.models.topic
        import app.models.tag
        import app.models.article
        import app.models.user
        import app.models.article_tag

        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        logger.error(f"Error creating database tables: {exc}")

    # 3. Seed default data if database is empty
    try:
        from app.models.topic import Topic
        from app.models.tag import Tag
        from app.models.article import Article
        from datetime import date

        db = SessionLocal()
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
        finally:
            db.close()
    except Exception as exc:
        logger.warning(f"Seed DB notice: {exc}")


def get_db():
    _ensure_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()