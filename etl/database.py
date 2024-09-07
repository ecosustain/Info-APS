import psycopg2


def conectar_db():
    """Conecta ao banco de dados PostgreSQL local."""
    try:
        conn = psycopg2.connect(
            dbname="saude_basica",  # Substitua pelo nome do seu banco de dados
            user="postgres",  # Substitua pelo usuário do banco de dados
            password="saude-basica",  # Substitua pela senha do banco de dados
            host="127.0.0.1",  # Substitua pelo host, se necessário
            port="5432",  # Porta padrão do PostgreSQL
        )
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
