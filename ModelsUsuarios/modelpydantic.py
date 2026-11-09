from pydantic import BaseModel

class ModelPydantic(BaseModel):
    nome: str
    email: str
    senha: str