# DB Connection Logic

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

def _build_database_url() -> str:
    primary = os.getenv("DATABASE_URL")
    if primary:
        return primary

    render_internal = os.getenv("DATABASE_INTERNAL_URL") or os.getenv("RENDER_DATABASE_URL")
    if render_internal:
        return render_internal

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB")

    if all([user, password, host, db_name]):
        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    # fallback for local development
    return "postgresql://postgres:postgres@localhost:5432/ai_interviewer"

# Determine which DB connection string to use (Render env vars override local settings)
DATABASE_URL = _build_database_url()

# Sets up connection infrastructure to DB
engine = create_engine(DATABASE_URL)

# How to interact with the DB. Requests should create a session and then close it. (Temp convo with the database)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Each model/table will inherit from this base class so SQLAlchemy can keep track of them and create the tables in the DB
Base = declarative_base()

# FastAPI dependency injection to allow us to create DB session per request and close it after automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
