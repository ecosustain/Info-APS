# backend/Dockerfile
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o conteúdo da aplicação
COPY . /app

# Instala as dependências
RUN pip install -r requirements.txt

# Expõe a porta 8001 para o serviço backend
EXPOSE 8001

# Executa a aplicação usando Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8001", "app:app", "--threads", "10"]
