import sys
import os
from pathlib import Path

# Add backend and ai_ml directories to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
for p in [str(ROOT_DIR / "backend"), str(ROOT_DIR / "ai_ml"), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
