from pathlib import Path
from dotenv import load_dotenv
import os
from supabase import create_client, Client

from google.adk.sessions import DatabaseSessionService

load_dotenv()

SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")
SUPABASE_USER= os.getenv("SUPABASE_USER")
#database_path = Path.cwd() / "data"

# basics sessions service
#db_url=f"postgresql+asyncpg://{SUPABASE_PASSWORD}@db.fbywrwsaakgfjovbxrte.supabase.co:5432/postgres"
db_url=f"postgresql+asyncpg://{SUPABASE_USER}:{SUPABASE_PASSWORD}@aws-0-us-west-2.pooler.supabase.com:5432/postgres"
#db_url = f"sqlite+aiosqlite:///{database_path.resolve()}/toddle_ops_sessions.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)

