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


def normalize_db_url(url: str) -> str:
    if not url:
        return f"sqlite:///{DEFAULT_DB_PATH}"

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+pg8000://", 1)
    elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
        url = url.replace("postgresql://", "postgresql+pg8000://", 1)

    return url


def build_engine():
    target_url = normalize_db_url(RAW_DB_URL)

    # 1. Try connecting to configured target DB
    try:
        connect_args = {}
        if "sqlite" in target_url:
            connect_args["check_same_thread"] = False
        eng = create_engine(target_url, connect_args=connect_args, pool_pre_ping=True)
        # Test connection
        with eng.connect() as conn:
            pass
        return eng
    except Exception as exc:
        logger.warning(f"Primary DB connection failed ({exc}). Trying standard PostgreSQL or SQLite fallback...")

    # 2. Try psycopg2 if pg8000 had issues
    if "pg8000" in target_url:
        try:
            alt_url = target_url.replace("postgresql+pg8000://", "postgresql+psycopg2://", 1)
            eng = create_engine(alt_url, pool_pre_ping=True)
            with eng.connect() as conn:
                pass
            return eng
        except Exception:
            pass

    # 3. Safe fallback: in-memory / tmp SQLite database
    fallback_url = f"sqlite:///{DEFAULT_DB_PATH}"
    logger.info(f"Using safe local SQLite database at {fallback_url}")
    return create_engine(fallback_url, connect_args={"check_same_thread": False}, pool_pre_ping=True)


engine = build_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()