FROM mongo:latest

# Define variáveis de ambiente
ENV BASE_DIR=/sisab/database
ENV DATA_DIR=$BASE_DIR/data
ENV BACKUP_DIR=$BASE_DIR/backup

# Cria as pastas necessárias com permissões apropriadas
RUN mkdir -p $DATA_DIR $BACKUP_DIR && \
    chown -R mongodb:mongodb $DATA_DIR $BACKUP_DIR

# Expor a porta padrão do MongoDB
EXPOSE 27017

# Iniciar o MongoDB usando o diretório padrão de dados
CMD ["mongod", "--bind_ip_all"]
