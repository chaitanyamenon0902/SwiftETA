import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Look up two folders to find the .env file in the repository root
# __file__ is backend/db.py -> parent is backend/ -> parent.parent is root/
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# 2. Extract the environment variable safely
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("CRITICAL: DATABASE_URL is missing from your environment setup!")

# 3. SQLAlchemy 2.0 fix (converts old 'postgres://' prefixes to 'postgresql://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. Initialize engine and session setup normally
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()