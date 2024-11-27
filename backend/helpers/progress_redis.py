import uuid

import redis

# Inicializa conexão com o Redis
redis_client = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


class ProgressManagerRedis:
    def __init__(self):
        # Garantir que o cliente Redis está pronto para uso
        self.redis = redis_client

    def start_progress(self):
        # Gera um ID único para a barra de progresso
        progress_id = str(uuid.uuid4())
        self.redis.set(
            progress_id, 0
        )  # Inicializa a barra de progresso com valor 0
        return progress_id

    def set_progress(self, progress_id, value):
        # Atualiza o progresso para o ID específico
        if self.redis.exists(progress_id):
            self.redis.set(progress_id, value)

    def get_progress(self, progress_id):
        # Retorna o progresso do ID especificado
        if self.redis.exists(progress_id):
            return int(self.redis.get(progress_id))
        return None

    def reset_progress(self, progress_id):
        # Reseta o progresso para o ID específico
        if self.redis.exists(progress_id):
            self.redis.set(progress_id, 0)
