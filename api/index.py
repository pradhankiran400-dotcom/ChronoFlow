import os
import sys
from pathlib import Path

# Add project root, backend, and ai_ml to sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
for p in [str(ROOT_DIR / "backend"), str(ROOT_DIR / "ai_ml"), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.main import app

try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except Exception:
    handler = app

application = app
