# models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL (e.g., from docker-compose.yml or environment variable)
DATABASE_URL = "postgresql://postgres:password@db/postgres"

# Set up the database connection and ORM base class
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Direction model
class Direction(Base):
    __tablename__ = "direction"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# Define the Laboratory model
class Laboratory(Base):
    __tablename__ = "laboratory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
