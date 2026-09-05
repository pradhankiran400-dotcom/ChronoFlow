import sys
from pathlib import Path

# Add project root, backend, and ai_ml to sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "backend"))
sys.path.insert(0, str(ROOT_DIR / "ai_ml"))
sys.path.insert(0, str(ROOT_DIR))

from app.main import app
