FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências e ODBC
RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https ca-certificates \
    build-essential unixodbc-dev gcc g++ \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 -o Dpkg::Options::="--force-overwrite" \
 && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos para dentro do container
COPY . .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
