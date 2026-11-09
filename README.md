# TaskFlow — Front-end para ProjetoCompleto

Interface moderna e responsiva em **HTML, CSS e JavaScript**, integrada à API **FastAPI + PostgreSQL + SQLAlchemy + JWT**.

## Funcionalidades
- Cadastro e login com JWT
- Painel com totais, pendências, concluídas e progresso
- Criar, listar, editar, concluir e excluir tarefas
- Pesquisa, filtros e ordenação
- Layout adaptável a desktop e celular
- Tarefas carregadas somente do usuário autenticado (`GET /tarefas/minhas`)

## Como integrar ao projeto existente
Copie a pasta `frontend/` para a raiz de `ProjetoCompleto/`, no mesmo nível de `main.py`.

### 1. Configurar CORS no FastAPI
No arquivo `main.py`, acrescente **antes** dos `include_router`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
```

> Esse exemplo é para desenvolvimento local. Em produção, informe a origem exata do site publicado.

### 2. Iniciar o Back-End

```bash
uvicorn main:app --reload
```

API esperada em `http://127.0.0.1:8000`.

### 3. Iniciar o Front-End
Na pasta `frontend/`, execute:

```bash
python -m http.server 5500 --bind 127.0.0.1
```

Abra **http://127.0.0.1:5500**.

Também funciona com a extensão Live Server do VS Code, desde que a porta/origem seja liberada no CORS.

### 4. Ajustar a URL da API
Edite `frontend/config.js` caso seu FastAPI esteja em outro host/porta.

## Endpoints esperados
| Método | Endpoint | Uso |
|---|---|---|
| POST | `/usuarios/cadastrar` | Cadastro `{nome,email,senha}` |
| POST | `/auth/login` | Login `{email,senha}` retorna `access_token` |
| GET | `/auth/me` | Perfil autenticado `{id,nome,email}` |
| GET | `/tarefas/minhas` | Lista tarefas do usuário |
| POST | `/tarefas/criar` | Cria `{titulo,descricao,concluida}` |
| PUT | `/tarefas/atualizar/{id}` | Atualiza tarefa própria |
| DELETE | `/tarefas/deletar/{id}` | Exclui tarefa própria |

Todos os endpoints de tarefas exigem `Authorization: Bearer <JWT>`.

## Segurança e publicação
- O JWT fica em `sessionStorage`, sendo descartado quando a aba/sessão é encerrada. É uma escolha simples para demonstração, **não substitui** uma estratégia de sessão segura para produção.
- Evite scripts de terceiros, mantenha dependências atualizadas e considere cookies HttpOnly com proteção CSRF numa versão de produção.
- As rotas antigas de usuários precisam ser revisadas para impedir exposição de hashes e operações não autorizadas.
- **Nunca** suba `.env`, chaves JWT ou credenciais de banco ao GitHub. Adicione-os ao `.gitignore`.
- O Dockerfile do Back-End não foi modificado. Este pacote contém somente o Front-End, que pode ser servido estaticamente ou colocado num container Nginx posteriormente.

## Observação
A implementação foi feita com base na estrutura da imagem e nos endpoints discutidos. Se algum endpoint/modelo estiver diferente no projeto local, ajuste-o conforme a API real.
