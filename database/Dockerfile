# database/Dockerfile
FROM mongo:latest

# Cria a pasta /data/db. Os dados iniciais serao baixados pelo script load_init_database.sh
RUN mkdir -p /data/db && chown mongodb:mongodb /data/db

ENV BASE_DIR=~/sisab/database
ENV DATA_DIR=$BASE_DIR/data
ENV BACKUP_DIR=$BASE_DIR/backup

# Creating folders
RUN mkdir -p $DATA_DIR
RUN mkdir -p $BACKUP_DIR

# Troca para o usuário mongodb para evitar problemas de permissão
USER mongodb

# Expor a porta 27017
EXPOSE 27017

# Define o ponto de entrada padrão do MongoDB com a porta alterada
CMD ["mongod", "--port", "27017"]