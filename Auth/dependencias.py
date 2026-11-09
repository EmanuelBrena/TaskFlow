
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from Auth.jwt_token import verificar_token
from ModelsUsuarios.modelsqlalchemy import (
    ModelSqlalchemy as Usuario,
    Session
)

seguranca = HTTPBearer(auto_error=False)


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(seguranca)
):
    if credenciais is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não informado!", headers={"WWW-Authenticate": "Bearer"})

    usuario_id = verificar_token(credenciais.credentials)

    if usuario_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado!", headers={"WWW-Authenticate": "Bearer"})

    with Session() as sessao:
        usuario = sessao.get(Usuario, usuario_id)

        if usuario is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado!",headers={"WWW-Authenticate": "Bearer"})

        return {"id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email}
