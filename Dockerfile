# Usa imagem base com Python
FROM python:3.12-slim

# Instala pacotes necessários para o pyodbc
RUN apt-get update && \
    apt-get install -y \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos para dentro da imagem
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Uvicorn
EXPOSE 8000

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
