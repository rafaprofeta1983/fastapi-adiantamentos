FROM python:3.12-slim

# Instalar dependências necessárias para adicionar repositórios
RUN apt-get update && \
    apt-get install -y curl gnupg2 apt-transport-https ca-certificates

# Adicionar chave e repositório da Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Atualizar repositórios
RUN apt-get update

# Instalar msodbcsql17 com o EULA aceito e forçando a sobrescrição de pacotes conflitantes
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 -o Dpkg::Options::="--force-overwrite" && \
    rm -rf /var/lib/apt/lists/*

# Outras instruções do Dockerfile
