import redis
import uuid
from datetime import datetime, timedelta
import os

# Inicializa conexão com o Redis
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# Obtenha a URL do Redis a partir da variável de ambiente REDIS_URL
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Configure o cliente Redis usando a URL
redis_client = redis.StrictRedis.from_url(redis_url, decode_responses=True)

class ProgressManager:
    def __init__(self):
        # Garantir que o cliente Redis está pronto para uso
        self.redis = redis_client

    def start_progress(self):
        # Gera um ID único para a barra de progresso e configura a estrutura de dados no Redis
        progress_id = str(uuid.uuid4())
        timestamp = int(datetime.now().timestamp())  # Timestamp atual em segundos

        # Define a chave e os campos
        key = f"progress_bar:{progress_id}"
        self.redis.hset(key, mapping={
            "progress_id": progress_id,
            "progress": 0,
            "message": "",
            "timestamp": timestamp
        })

        return progress_id

    def set_progress(self, progress_id, value, message=None):
        # Atualiza o progresso e o timestamp para o ID específico
        key = f"progress_bar:{progress_id}"

        if self.redis.exists(key):
            self.redis.hset(key, "progress", value)
            if message is not None:
                self.redis.hset(key, "message", message)
            self.redis.hset(key, "timestamp", int(datetime.now().timestamp()))

        else:
            print(f"Progress ID {progress_id} não encontrado.")

    def get_progress(self, progress_id):
        # Retorna o progresso do ID especificado
        key = f"progress_bar:{progress_id}"

        if self.redis.exists(key):
            progress = int(self.redis.hget(key, "progress"))
            message = self.redis.hget(key, "message")
            return {"progress": progress, "message": message}
        return None

    def reset_progress(self, progress_id):
        # Reseta o progresso para o ID específico
        key = f"progress_bar:{progress_id}"

        if self.redis.exists(key):
            self.redis.hset(key, "progress", 0)
            self.redis.hset(key, "message", "")
            self.redis.hset(key, "timestamp", int(datetime.now().timestamp()))

    def delete_old_progress(self):
        """Deleta todas as barras de progresso com timestamp inferior a 24 horas."""
        one_day_ago = int((datetime.now() - timedelta(days=1)).timestamp())

        # Busca todas as chaves que iniciam com 'progress_bar:'
        for key in self.redis.scan_iter("progress_bar:*"):
            # Obtém o timestamp da barra de progresso
            timestamp = int(self.redis.hget(key, "timestamp"))

            # Deleta se o timestamp é inferior ao limite
            if timestamp < one_day_ago:
                self.redis.delete(key)
                print(f"Deleted {key}")