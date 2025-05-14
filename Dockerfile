FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https ca-certificates \
    build-essential unixodbc-dev gcc g++ \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
 && rm -rf /var/lib/apt/lists/*

# Atualizar repositórios
RUN apt-get update

# Instalar msodbcsql17 com o EULA aceito e forçando a sobrescrição de pacotes conflitantes
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 -o Dpkg::Options::="--force-overwrite" && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt    

# Outras instruções do Dockerfile

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
