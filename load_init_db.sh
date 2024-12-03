#!/bin/bash

echo "Downloading backup"
wget -O /tmp/sisab_mongo_init_db_backup.zip https://vpublic-files.s3.us-east-1.amazonaws.com/sisab_mongo_init_db_backup.zip

echo "Unziping backup"
unzip /tmp/sisab_mongo_init_db_backup.zip -d /tmp

# rm -f /tmp/sisab_mongo_init_db_backup.zip

echo "Moving backup to container"
docker cp /tmp/sisab_v2 sisab_database:/tmp

# Executa o comando de restauração no contêiner do MongoDB
echo "Restoring backup"
docker exec -it sisab_database mongorestore --uri="mongodb://localhost:27017/sisab_v2" --nsInclude="sisab_v2.*" /tmp/sisab_v2
