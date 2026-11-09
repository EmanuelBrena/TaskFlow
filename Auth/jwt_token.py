import jwt
from datetime import datetime, timedelta, timezone
import secrets

CHAVE_SECRETA = secrets.token_hex(32)
ALGORITMO = 'HS256'

def criar_token(usuario_id: int):
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=30)

    dados = {'sub': str(usuario_id),
             'exp': expiracao}

    token = jwt.encode(dados, CHAVE_SECRETA, algorithm=ALGORITMO)

    return token


def verificar_token(token: str):
    try:
        dados = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO], options={"require": ["sub", "exp"]})

        usuario_id = int(dados["sub"])

        return usuario_id

    except (jwt.InvalidTokenError, ValueError, TypeError):
        return None