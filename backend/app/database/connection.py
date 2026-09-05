import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parents[2]
is_serverless = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

if is_serverless:
    DEFAULT_DB_PATH = Path("/tmp/chronoflow.db")
else:
    DEFAULT_DB_PATH = BACKEND_DIR / "chronoflow.db"

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH}"
elif DATABASE_URL.startswith("postgres://"):
    # SQLAlchemy requires postgresql:// instead of postgres://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()