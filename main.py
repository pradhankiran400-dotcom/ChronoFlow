import sys
import os
from pathlib import Path

# Add backend and ai_ml directories to Python path
ROOT_DIR = Path(__file__).resolve().parent
for p in [str(ROOT_DIR / "backend"), str(ROOT_DIR / "ai_ml"), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.main import app

handler = app
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
