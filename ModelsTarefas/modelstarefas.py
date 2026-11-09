from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from ModelCompartilhada.database import Base
from ModelCompartilhada.database import Base, Session


class ModelSqlalchemy(Base):
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    descricao = Column(String)
    concluida = Column(Boolean)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))