FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY criar_tabelas.py .
COPY main.py .
COPY Auth/ ./Auth
COPY BackEnd/ ./BackEnd
COPY Docker/ ./Docker
COPY FrontEnd/ ./FrontEnd
COPY ModelCompartilhada/ ./ModelCompartilhada
COPY ModelsTarefas/ ./ModelsTarefas
COPY ModelsUsuarios/ ./ModelsUsuarios

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]