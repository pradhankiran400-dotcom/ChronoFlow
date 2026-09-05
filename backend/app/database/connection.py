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

# Eagerly create tables at module import time (critical for Vercel which skips ASGI lifespan)
_db_initialized = False

def _ensure_db():
    """Create tables and seed data once per cold start."""
    global _db_initialized
    if _db_initialized:
        return
    _db_initialized = True
    try:
        from app.database.base import Base
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database tables created ({DATABASE_URL})")
    except Exception as exc:
        logger.warning(f"DB init notice: {exc}")

# Run immediately on import
_ensure_db()


def get_db():
    _ensure_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()