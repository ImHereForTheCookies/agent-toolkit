"""uvicorn entry point: `uvicorn app.server:app` (db path from PANTRY_DB)."""
import os

from . import db
from .main import create_app

DB_PATH = os.environ.get("PANTRY_DB", "pantry.db")
db.seed(DB_PATH)
app = create_app(DB_PATH)
