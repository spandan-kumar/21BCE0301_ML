from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
