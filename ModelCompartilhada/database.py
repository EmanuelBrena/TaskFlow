import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password=os.getenv("SENHA_POSTGRESQL"),
        host="localhost",
        port=5432,
        database="ProjetoCompleto"
    )

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
