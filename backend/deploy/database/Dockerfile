# Dar as seguintes permissoes :
#sudo chown -R 999:999 database/data
#sudo chmod -R 755 database/data

# database/Dockerfile
FROM mongo:latest

# Copia o banco de dados do host para o contêiner
COPY ./data /data/db

# Troca para o usuário mongodb para evitar problemas de permissão
USER mongodb

# Define o ponto de entrada padrão do MongoDB
CMD ["mongod"]

