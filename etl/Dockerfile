# Use a imagem oficial do Python como base
FROM apache/airflow:2.7.1-python3.10

# Usuário root
USER root

# Defina as variáveis de ambiente
ENV DOWNLOAD_DIR='/opt/airflow/data/download'
ENV TRANSFORMACAO_DIR='/opt/airflow/data/transformacao'
ENV FINAL_DIR='/opt/airflow/data/consolidado'
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"


# Instale as dependências do SO
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    cron \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    libglib2.0-0 \
    libc6 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libnspr4 \
    libpangoft2-1.0-0 \
    libstdc++6 \
    libdrm2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    vim \
    --no-install-recommends

# Adicionar a chave do repositório do Google Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adicionar o repositório do Google Chrome
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Instalar o Google Chrome
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# Baixe o driver do Chrome
RUN wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.69/linux64/chromedriver-linux64.zip

# Extraia o driver do Chrome
RUN unzip chromedriver-linux64.zip

# Mova o driver do Chrome para o diretório de binários
RUN mv chromedriver-linux64/chromedriver /usr/local/bin/

# Usuário airflow
USER airflow

# Defina o diretório de trabalho dentro do container
WORKDIR /opt/airflow

# Copie o conteúdo da pasta atual para o diretório de trabalho no container
COPY . .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

USER root

# Criar os diretórios necessários
RUN mkdir -p /opt/airflow/data/download /opt/airflow/data/transformacao /opt/airflow/data/consolidado

RUN chown -R airflow: /opt/airflow

USER airflow

# Configura o script de entrada
ENTRYPOINT ["/opt/airflow/entrypoint.sh"]

# Define o comando padrão como webserver
CMD ["webserver"]