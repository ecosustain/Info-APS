# Dashboard de Saúde Básica

**Dashboard de Saúde Básica** é um dashboard interativo desenvolvido com Plotly Dash que permite visualizar e analisar
dados de saúde básica coletados do sistema SUS, pelo portal [SISAB](https://sisab.saude.gov.br/) . O projeto utiliza um banco de dados PostgreSQL para armazenar os dados e alimenta os componentes do dashboard com consultas dinâmicas.

## 📋 Visão Geral

Este projeto foi criado para fornecer uma interface de visualização de dados de saúde, permitindo que os usuários
explorem informações sobre primeiro atendimento e procedimentos em diferentes estados e regiões do Brasil. O dashboard inclui:

- Dropdowns dinâmicos para seleção de estados e regiões.
- Sumários de atendimentos por estado, região, município e ano.
- Mapa interativo exibindo a distribuição dos atendimentos em diferentes locais.

## 🚀 Tecnologias Utilizadas

- **Python**: Linguagem principal para o desenvolvimento.
- **Dash (Plotly)**: Framework utilizado para criar o dashboard interativo.
- **PostgreSQL**: Banco de dados utilizado para armazenar e consultar os dados clínicos.
- **Pandas**: Utilizado para manipulação e processamento dos dados.
- **psycopg2**: Biblioteca utilizada para conectar ao PostgreSQL.

## 📂 Estrutura do Projeto

```plaintext
project_name/
│
├── app.py                     # Arquivo principal que inicia o Dash
├── requirements.txt           # Dependências do projeto
│
├── assets/                    # Arquivos estáticos (CSS, JS)
│   └── styles.css             # Estilos personalizados
│
├── components/                # Componentes do layout do Dash
│   ├── header.py              # Cabeçalho do dashboard
│   ├── dropdowns.py           # Dropdowns para seleção de estados e regiões
│   ├── graph.py               # Carrega os gráficos
│
├── callbacks/                 # Callbacks que gerenciam a interatividade
│   ├── update_dropdown.py     # Callbacks para atualizar os dropdows
│   └── update_bar_graph.py        # Callback para atualizar os gráficos
│
├── config/                    # Configurações do projeto
│   └── settings.py            # Configurações de conexão com o banco de dados
│
├── data/                      # Gerenciamento de conexões com o banco de dados
│   └── database.py            # Classe para conectar e buscar dados no PostgreSQL
│
└── utils/                     # Funções utilitárias
    └── queries.py             # Consultas SQL utilizadas no projeto
```

## 🛠️ Instalação

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Clone o Repositório

```bash
git clone https://gitlab.com/schulzdanielf/saude-basica.git
cd dash-app
```

### 2. Crie um Ambiente Virtual e Ative-o

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados

Certifique-se de ter um banco de dados PostgreSQL configurado com as tabelas e dados necessários. Atualize o arquivo `config/settings.py` com suas credenciais do banco de dados:

```python
# config/settings.py
DATABASE_CONFIG = {
    'dbname': 'your_database_name',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'localhost',
    'port': 5432
}
```

### 5. Execute o Aplicativo

Para iniciar o aplicativo, execute o seguinte comando:

```bash
python app.py
```

O aplicativo estará disponível em [http://127.0.0.1:8050](http://127.0.0.1:8050).

