# Saúde Básica Mongo-Backend

O sistema foi desenvolvido com flask e mongodb como o objetivo de servir como API's endpoint e algumas páginas administrativas.

## Estrutura do Projeto

O sistema está organizado nas seguintes pastas:

- **apis**: Arquivos que codificam as apis, cada arquivo trata do escopo de um endpoint.
- **config**: Configurações gerais do sistema.
- **database**: Conexão com o banco de dados e classes para gerenciameto de dados.
- **heplpers**: Arquivos com classes de propósitos gerais.
- **templates**: Arquivos com os htmls para views.
- **tests**: Arquivos com os testes de unidades.
- **uploads**: Diretório para onde são enviados as coleções por upload, quando é importado os dados de um arquivo csv.
- **views**: Views que respondem as páginas htmls do sistema.
- **application.py**: Arquivo que executa a aplicação.
- **route.py**: Arquivo que gerencia as rotas das Api's e das views.


## Configuração Inicial

### Pré-Requisitos

Antes de iniciar, certifique-se de ter o Python e o pip instalados no seu ambiente. O sistema foi testado com Python
3.12+ e MogoDB 6.0.18 em sistema operacional Linux Ubuntu 22.04 LTS.

### Configuração do Ambiente

Para configurar o ambiente e instalar as dependências necessárias, siga os passos:

1. Crie um ambiente virtual:

```bash
python -m venv sisab-api
```

2. Ative o ambiente virtual:

```bash
source sisab-api/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Configuração do Banco de Dados

O modelo de Sistema Gerenciador de Banco de Dados (SGBD) é não Relacional e o sistema foi implantado em MongoDB 6.0.18.

# Carregando o banco com dados

- Baixar o arquivo [Banco de Dados Completo](https://vpublic-files.s3.us-east-1.amazonaws.com/sisab-mongodb-dump.zip)
```bash
  wget https://vpublic-files.s3.us-east-1.amazonaws.com/sisab-mongodb-dump.zip
```
- Descompactar.
```bash
  unzip sisab-mongodb-dump.zip
```
- Carregar o banco.
```bash
  mongorestore --db <nome_banco_dados> --dir <diretótio>
```

Por exemplo: se o nome do banco de dados por sisab_v2 e a pasta onde foi descompactado o banco chama-se sisab. Execute:
```bash
  mongorestore --db sisab_v2 --dir sisab/
```

## Uso

Para iniciar o servidor localmente, execute:

```bash
    python application.py
```

O sistema estará acessível via `http://localhost:5000/`.
