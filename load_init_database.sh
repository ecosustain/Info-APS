#!/bin/bash

# Define variáveis para os caminhos
BASE_DIR=~/sisab/database
DATA_DIR=$BASE_DIR/data
BACKUP_DIR=$BASE_DIR/backup
BACKUP_FILE=$BACKUP_DIR/sisab_mongo_init_db_backup.zip

echo "Creating folders"
mkdir -p $DATA_DIR
mkdir -p $BACKUP_DIR

# Obtém o nome do usuário que está executando o script
CURRENT_USER=$(whoami)

# Define o grupo como o grupo principal do usuário atual
CURRENT_GROUP=$(id -gn "$CURRENT_USER")

# Atribui o dono da pasta ao usuário atual, com o grupo correto
sudo chown -R "$CURRENT_USER":"$CURRENT_GROUP" "$DATA_DIR"
sudo chown -R "$CURRENT_USER":"$CURRENT_GROUP" "$BACKUP_DIR"

# Concede permissões completas para o dono da pasta
sudo chmod -R u+rwx "$BACKUP_DIR"
sudo chmod -R u+rwx "$DATA_DIR"

echo "Downloading backup"
wget -O $BACKUP_FILE https://vpublic-files.s3.us-east-1.amazonaws.com/sisab_mongo_init_db_backup.zip

echo "Restoring backup"
unzip $BACKUP_FILE -d $BACKUP_DIR

rm -f $BACKUP_FILE

# Executa o comando de restauração no contêiner do MongoDB
CONTAINER_NAME=$(docker ps --filter "name=sisab_database" --format "{{.Names}}")
docker exec -it $CONTAINER_NAME mongorestore --uri="mongodb://localhost:27017/sisab_v2" --nsInclude="sisab_v2.*" /backup/sisab_v2
