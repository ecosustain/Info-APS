# Saúde Básica em Dados
Projeto destinado à estruturação e análise de dados abertos de saúde pública do site sisab.saude.gov.br. 

## Objetivo
O objetivo principal do projeto é disponibilizar informações sobre a saúde pública no Brasil de forma clara e acessível, promovendo a transparência e a democratização dos dados. Para isso, utilizamos ferramentas de análise de dados e visualização para criar dashboards interativos e relatórios analíticos que permitam a compreensão dos dados e a extração de insights valiosos.

## Metodologia
Para atingir nosso objetivo, utilizamos uma metodologia baseada em três pilares: coleta, análise e visualização de dados. A coleta de dados é realizada a partir de fontes abertas disponíveis no site sisab.saude.gov.br, que disponibiliza informações sobre diversos indicadores de saúde pública. Em seguida, realizamos a análise dos dados, identificando padrões, tendências e relações entre as variáveis. Por fim, utilizamos ferramentas de visualização de dados para criar dashboards interativos e relatórios analíticos que permitam a compreensão dos dados e a extração de insights valiosos.


## Instalação
Para instalar os requisitos do projeto, siga os passos abaixo:
``` make install ```

## Configuração
Para configurar o projeto, siga os passos abaixo:

- Crie o arquivo de configuração config.ini a partir do arquivo de exemplo config.ini.example

## Estrutura de diretórios
```
.
├── Makefile # Arquivo de automação de tarefas
├── README.md # Documentação do projeto
├── analises # Análises de dados
├── dash-app
│   ├── README.md
│   ├── app.py
│   ├── callbacks
│   ├── components
│   ├── config
│   ├── data
│   ├── requirements.txt
│   └── utils
├── docker-compose.yml # Arquivo de configuração do Docker Compose
├── docs # Documentação do projeto
│   └── variaveis-validacao.md
├── etl # Extração, transformação e carregamento dos dados
│   ├── config_example.ini # Arquivo de configuração
│   ├── data # Diretório de dados extraídos
│   ├── database.py # Conexão com o banco de dados
│   ├── extracao_CID.ipynb # Extração de dados de CID
│   ├── extracao_codigos.py
│   ├── extracao_producao.py # Extração de dados de produção
│   ├── extracao_validacao.py # Extração de dados de validação
│   ├── transf_producao.py # Transformação de dados de produção
│   └── transf_validacao.py # Transformação de dados de validação
├── mapas
│   ├── BR_Municipios_2022 # Shapefiles dos municípios brasileiros
│   ├── BR_UF_2022 # Shapefiles das unidades federativas brasileiras
│   └── SP_Municipios_2022 # Shapefiles dos municípios de São Paulo
├── modelos
│   └── database
├── painel # Aplicação Web com Dash para visualização dos dados
│   ├── Dockerfile
│   ├── app.py # Arquivo principal
│   ├── assets # Diretório de arquivos estáticos
│   ├── callbacks # Diretório de callbacks
│   ├── data # Diretório de dados
│   ├── funcoes.py # Funções auxiliares
│   ├── paginas # Diretório de páginas
│   ├── requirements.txt # Requisitos do projeto
│   └── static # Diretório de arquivos estáticos
├── postgresql # Diretório do banco de dados
│   └── data:
├── requirements.txt # Requisitos do projeto
└── tests # Testes do projeto
```

## Autores
 - Daniel Schulz
 - Elinilson Vital
 - Leonardo Gomes
 - Lucas Macedo
 - Mariana Cruvinel

## Licença
MIT License
