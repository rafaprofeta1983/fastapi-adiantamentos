# Usa uma imagem base do Python
FROM python:3.12-slim

# Cria e define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o diretório de trabalho
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8000 (padrão do Uvicorn)
EXPOSE 8000

# Define a variável de ambiente para o uvicorn
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
