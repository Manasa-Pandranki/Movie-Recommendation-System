
from backend.database import engine, Base
from backend import models

# Create all database tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")

print("Tables:", list(Base.metadata.tables.keys()))
