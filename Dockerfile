FROM python:3.12-slim

# Instala dependências do sistema, incluindo ODBC
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    gnupg \
    curl \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Cria diretório de trabalho
WORKDIR /app

# Copia os arquivos do seu projeto
COPY . /app

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
