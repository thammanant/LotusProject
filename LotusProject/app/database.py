from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# use PostgresSQL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@lotusproject-db:5432/lotus'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
