
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from ModelsTarefas.modelstarefas import ModelSqlalchemy, Session
from ModelsTarefas.modelptarefas import ModelPydantic
from Auth.dependencias import obter_usuario_atual

router = APIRouter()


# CRIAR TAREFA
@router.post('/tarefas/criar')
def criar_tarefas(tarefa: ModelPydantic,usuario=Depends(obter_usuario_atual)):

    nova_tarefa = ModelSqlalchemy(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        concluida=tarefa.concluida,
        usuario_id=usuario["id"]
    )

    with Session() as sessao:
        sessao.add(nova_tarefa)
        sessao.commit()
        sessao.refresh(nova_tarefa)

        return {"mensagem": "Tarefa criada com sucesso!",
                "tarefa_id": nova_tarefa.id}


# LISTAR TAREFAS DO USUÁRIO AUTENTICADO
@router.get('/tarefas/listar')
def listar_tarefas(usuario=Depends(obter_usuario_atual)):

    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.usuario_id == usuario["id"]))

        return resultado.scalars().all()


# LISTAR UMA TAREFA PELO ID
@router.get('/tarefas/listar/{id}')
def listar_tarefa(id: int, usuario=Depends(obter_usuario_atual)):

    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.id == id,ModelSqlalchemy.usuario_id == usuario["id"]))

        tarefa = resultado.scalar_one_or_none()

        if tarefa is None:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada!")

        return tarefa


# ATUALIZAR TAREFA
@router.put('/tarefas/atualizar/{id}')
def atualizar_tarefa(id: int, t: ModelPydantic, usuario=Depends(obter_usuario_atual)):

    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.id == id, ModelSqlalchemy.usuario_id == usuario["id"]))

        tarefa = resultado.scalar_one_or_none()

        if tarefa is None:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada!")

        tarefa.titulo = t.titulo
        tarefa.descricao = t.descricao
        tarefa.concluida = t.concluida

        sessao.commit()

        return {"mensagem": f"Tarefa {t.titulo} atualizada com sucesso!"}


# DELETAR TAREFA
@router.delete('/tarefas/deletar/{id}')
def deletar_tarefa(id: int, usuario=Depends(obter_usuario_atual)):

    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.id == id,ModelSqlalchemy.usuario_id == usuario["id"]))

        tarefa = resultado.scalar_one_or_none()

        if tarefa is None:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada!")

        titulo = tarefa.titulo

        sessao.delete(tarefa)
        sessao.commit()

        return {"mensagem": f"Tarefa {titulo} deletada com sucesso!"}


# LISTAR MINHAS TAREFAS
@router.get('/tarefas/minhas')
def minhas_tarefas(usuario=Depends(obter_usuario_atual)):

    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.usuario_id == usuario["id"]))

        return resultado.scalars().all()


# BUSCAR TAREFA
@router.get('/tarefas/{id}')
def buscar_tarefa(id: int,usuario=Depends(obter_usuario_atual)):

    with Session() as sessao:
        resultado = sessao.execute(select(ModelSqlalchemy).where(ModelSqlalchemy.id == id,ModelSqlalchemy.usuario_id == usuario["id"]))

        tarefa = resultado.scalar_one_or_none()

        if tarefa is None:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada!")

        return tarefa
