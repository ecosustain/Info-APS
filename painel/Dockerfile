# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o conteúdo da pasta atual para o diretório de trabalho no container
COPY . .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Variaveis de ambiente
ENV HOST='0.0.0.0'
ENV PORT=8050

# Exponha a porta em que a aplicação irá rodar
EXPOSE 8050

# Comando para rodar a aplicação
CMD ["python", "app.py"]
