from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from Auth.jwt_token import criar_token
from Auth.dependencias import obter_usuario_atual

from ModelsUsuarios.modelsqlalchemy import ModelSqlalchemy, Session
from Auth.senhahash import password_hash

router = APIRouter()


class LoginUsuario(BaseModel):
    email: str
    senha: str


@router.post('/auth/login')
def login(dados: LoginUsuario):

    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.email == dados.email))

        usuario = resultado.scalar_one_or_none()

        if usuario is None:
            raise HTTPException(status_code=401, detail='Email ou senha incorretos!')

        senha_correta = password_hash.verify(dados.senha, usuario.senha_hash)

        if not senha_correta:
            raise HTTPException(status_code=401, detail='Email ou senha incorretos!')

        token = criar_token(usuario.id)

        return {
            "access_token": token,
            "token_type": "bearer"
        }



from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Auth.jwt_token import verificar_token

# Recebe o token Bearer do cabeçalho Authorization
seguranca = HTTPBearer()


@router.get('/auth/me')
def usuario_autenticado(
    usuario = Depends(obter_usuario_atual)
):
    return usuario
