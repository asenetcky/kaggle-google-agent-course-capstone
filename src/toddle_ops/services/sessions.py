from google.adk.sessions import DatabaseSessionService

from pathlib import Path

database_path = Path.cwd() / "data"

# basics sessions service
db_url = f"sqlite+aiosqlite:///{database_path.resolve()}/toddle_ops_sessions.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)
