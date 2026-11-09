from pydantic import BaseModel

class ModelPydantic(BaseModel):
    titulo: str
    descricao: str
    concluida: bool