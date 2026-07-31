from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL not set. Check your .env file.")
    
engine = create_engine(database_url, echo=True)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)