
from ModelCompartilhada.database import Base, engine

from ModelsUsuarios.modelsqlalchemy import ModelSqlalchemy as Usuario
from ModelsTarefas.modelstarefas import ModelSqlalchemy as Tarefa


Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")
