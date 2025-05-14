FROM python:3.12-slim

# Instala dependências básicas
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    ca-certificates \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Adiciona repositório da Microsoft para o ODBC Driver 17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Atualiza e instala o msodbcsql17
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && rm -rf /var/lib/apt/lists/*

# Cria o diretório de trabalho
WORKDIR /app

# Copia o conteúdo do projeto
COPY . .

# Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta usada pelo Uvicorn
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
