from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# connect_args={"check_same_thread": False} is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency function to yield a database session.
    Automatically closes the session after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
