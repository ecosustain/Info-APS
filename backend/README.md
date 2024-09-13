# Saúde Básica Backend

O sistema foi desenvolvido com o framework Django, com uma área administrativa para gerenciamento do sistema de
informação.

## Estrutura do Projeto

O sistema está organizado nas seguintes pastas:

- **core**: Armazena os modelos de dados (`core/models`), scripts de seed (`management/commands`) para popular as
  tabelas do domínio e configurações iniciais.
- **website**: Site estático com informações técnicas sobre o sistema, como modelos conceituais e físicos de
  dados, além de artefatos para apoiar o desenvolvimento.
- **saude_basica_backend**: Diretório do projeto Django, incluindo as configurações do sistema.

## Configuração Inicial

### Pré-Requisitos

Antes de iniciar, certifique-se de ter o Python e o pip instalados em seu ambiente. O sistema foi testado com Python
3.12+ e Postgresql 14 em sistema operacional Linux.


### Configuração do Ambiente

Para configurar o ambiente e instalar as dependências necessárias, siga os passos:

1. Clone o repositório para sua máquina local.
2. Crie um ambiente virtual:

```bash
python -m venv saude_basica_env
```

3. Ative o ambiente virtual:

```bash
source saude_basica_env/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Configuração do Banco de Dados

O modelo de Sistema Gerenciador de Banco de Dados (SGBD) é Relacional e o sistema foi implantado em Postgresql 14.

- Criar um banco de dados novo:
  No console psql:
    ```postgresql
    CREATE DATABASE saude_basica_development;
    ```

- Criação do banco de dados e carregamento inicial: Inicialize o banco de dados com os seguintes comandos.

    ```bash
    python manage.py makemigrations # Cria o script de migração
    python manage.py migrate # Cria o modelo físico de dados no SGBD configurado
    ```

### Carregando tabelas de domínio

Execute os scripts de seed na raiz do projeto para popular as tabelas básicas do domínio. Esse comando carrega os dados
iniciais da pastas seed_json.

```bash
python manage.py seed # Carrega as tabelas básicas de domínio. Esse comando não carrega os dados
```

### Importando dados de uma pasta
Para carregar os dados diretamente de arquivos:
- Ler a instruções no arquivo seed.py para habilitar o código necessário

# Carregando o banco com dados

- Baixar o arquivo [Banco de Dados Completo](https://dlab-public-files.s3.us-east-2.amazonaws.com/saude_basica_v1.psql.zip)
- Descompactar e carregar pelo psql. Garanta que o usuário saude_basica e o banco de dados saude_basica_development
  existam.

```bash
   psql -f saude_basica_v1.psql --host localhost --port 5432 --username saude_basica --password --dbname saude_basica_development
```

## Uso

Para iniciar o servidor localmente, execute:

```bash
    python manage.py runserver
```

O sistema estará acessível via `http://localhost:8000/`.

## Administração

Para acessar a área administrativa é necessário criar um usuario pelo prompt:

```bash
python manager.py createsuperuser
```

Acesse o sistema de administração do Django em `http://localhost:8000/admin` para gerenciar as tabelas do sistema.
