RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 -o Dpkg::Options::="--force-overwrite" && \
    rm -rf /var/lib/apt/lists/*
