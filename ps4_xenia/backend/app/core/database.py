from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from .config import settings
import redis
import time
import logging
import json
from functools import wraps

# Setup Logger
logger = logging.getLogger("db_persistence")

# Database Setup
engine = create_engine(settings.DATABASE_URL, echo=False)  # Disable echo for prod-like logs

# Redis Setup
try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("✅ Connected to Redis")
except redis.ConnectionError:
    logger.warning("⚠️ Redis connection failed. Caching will be disabled.")
    redis_client = None

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def commit_with_retry(session: Session, max_retries: int = 3, delay: float = 0.5):
    """
    Commits session with retry logic for transient database errors.
    REQ-10: Persistence and Consistency
    """
    attempt = 0
    while attempt < max_retries:
        try:
            session.commit()
            return
        except OperationalError as e:
            attempt += 1
            if attempt == max_retries:
                logger.error(f"❌ DB Commit failed after {max_retries} attempts: {str(e)}")
                raise e
            logger.warning(f"⚠️ DB Commit failed (Attempt {attempt}/{max_retries}). Retrying in {delay}s...")
            time.sleep(delay)
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"❌ DB Commit Error: {str(e)}")
            raise e

