redis:
    build:
      context: ./redis  # Caminho para o Dockerfile (se estiver usando um)
    image: redis:latest  # Pode ser omitido se estiver usando um Dockerfile
    container_name: redis-server
    ports:
      - "6379:6379"  # Mapeia a porta 6379 do contêiner para a 6379 do host
    networks:
      - app_network
    volumes:
      - redis_data:/data  # Volume para persistir dados do Redis
