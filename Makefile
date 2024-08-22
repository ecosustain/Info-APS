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
	black .
	isort . --profile black

# Lint com flake8
lint:
	flake8 --config=configs/.flake8 .

# Verificar tipos com mypy
mypy:
	mypy $(SRC_DIR)

# Executar testes com pytest
test:
	pytest --cov=app

# Instalar dependências do projeto
install:
	pip install -r requirements.txt

# Atualizar dependências do projeto
update:
	pip install --upgrade -r requirements.txt

# Recriar ambiente de desenvolvimento (exclui e reinstala dependências)
rebuild: clean install

# Tarefas padrões
.PHONY: clean format lint mypy test install update rebuild