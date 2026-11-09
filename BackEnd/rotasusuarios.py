from fastapi import APIRouter, HTTPException
from Auth.senhahash import password_hash
from ModelsUsuarios.modelpydantic import ModelPydantic
from ModelsUsuarios.modelsqlalchemy import ModelSqlalchemy, Session
from sqlalchemy import select

router = APIRouter()


@router.get('/')
async def home():
    return {'mensagem': 'Bem Vindo(a)!'}


@router.post('/usuarios/cadastrar')
async def cadastrar_usuario(user: ModelPydantic):

    novo_usuario = ModelSqlalchemy(
        nome = user.nome,
        email = user.email,
        senha_hash = password_hash.hash(user.senha)
    )

    with Session() as sessao:
        sessao.add(novo_usuario)
        sessao.commit()

        return f'Usuario {user.nome} cadastrado com sucesso!'


@router.get('/usuarios/listar')
async def listar_usuarios():
    users = []

    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy))

        for usuarios in resultado.scalars():
            users.append(usuarios)

    return users

@router.get('/usuarios/listar/{id}')
async def listar_usuario(id: int):
    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.id == id))

        for usuario in resultado.scalars():
            return usuario

    raise HTTPException(status_code=404, detail='Usuário não encontrado!')


@router.put('/usuarios/atualizar/{id}')
async def atualizar_usuario(id: int, user: ModelPydantic):
    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.id == id))

        for usuario in resultado.scalars():
            usuario.nome = user.nome
            usuario.email = user.email
            usuario.senha_hash = password_hash.hash(user.senha)

            sessao.commit()

            return f'Usuario {user.nome} atualizado com sucesso!'

    raise HTTPException(status_code=404, detail='Usuário não encontrado!')


@router.delete('/usuarios/deletar/{id}')
async def deletar_usuario(id: int):
    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.id == id))

        for usuario in resultado.scalars():
            sessao.delete(usuario)
            sessao.commit()

            return f'Usuario {usuario.nome} deletado com sucesso!'

    raise HTTPException(status_code=404, detail='Usuário não encontrado!')