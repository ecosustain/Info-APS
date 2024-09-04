# Diretório do código fonte
SRC_DIR = .

# Limpar arquivos compilados Python e cache
clean:
	find $(SRC_DIR) -type f -name "*.py[co]" -delete
	find $(SRC_DIR) -type d -name "__pycache__" -delete 
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache

# Formatar código usando black
format:
	black --line-length 79 .
	isort . --profile black

# Lint com flake8
lint:
	pylint etl painel || true

# Verificar tipos com mypy
mypy:
	mypy $(SRC_DIR)

# Executar testes com pytest
test:
	pytest --cov=app

# Instalar dependências do projeto
install:
	@echo "Instalando os requisitos do projeto"
	pip install -r requirements.txt
	@echo "Criando os diretórios necessários para o projeto"
	mkdir -p etl/data/transformacao
	mkdir -p etl/data/consolidado
	@echo "Verificando se o arquivo config.ini existe..."
	@if [ ! -f etl/config.ini ]; then \
		echo "Arquivo config.ini não encontrado. Copiando config_example.ini para config.ini..."; \
		cp etl/config_example.ini etl/config.ini; \
	fi
	@echo "Atualizando o arquivo de configuração com o diretório raiz do projeto"
	@USER_HOME=$(shell echo ~); \
	PROJECT_ROOT=$(shell pwd); \
	sed -i 's|^home_dir = .*|home_dir = '"$$USER_HOME"'|' etl/config.ini; \
	sed -i 's|^root_dir = .*|root_dir = '"$$PROJECT_ROOT"'|' etl/config.ini

# Atualizar dependências do projeto
update:
	pip install --upgrade -r requirements.txt

# Recriar ambiente de desenvolvimento (exclui e reinstala dependências)
rebuild: clean install

# Tarefas padrões
.PHONY: clean format lint mypy test install update rebuild