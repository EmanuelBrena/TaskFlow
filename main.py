from fastapi import FastAPI
from BackEnd.rotasusuarios import router as usuarios_router
from BackEnd.rotastarefas import router as tarefas_router
from BackEnd.rotasautenticacao import router as autenticacao_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(usuarios_router)
app.include_router(tarefas_router)
app.include_router(autenticacao_router)