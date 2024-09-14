from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace this with your actual database URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.vuvfapysswkzhtfdhjgj:Hp1010hp1010@@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
