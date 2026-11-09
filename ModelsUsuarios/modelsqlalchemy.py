from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from ModelCompartilhada.database import Base
import os
from ModelCompartilhada.database import Base, Session


class ModelSqlalchemy(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha_hash = Column(String)
