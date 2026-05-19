from backend.database.db import engine, Base
from backend.database import models  # IMPORTANT: registers tables

print("Creating tables in database...")

Base.metadata.create_all(bind=engine)

print("Database setup complete!")