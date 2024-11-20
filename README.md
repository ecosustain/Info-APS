# Saúde Básica em Dados
Projeto destinado à estruturação e análise de dados abertos de saúde pública do site sisab.saude.gov.br. 

## Objetivo
O objetivo principal do projeto é disponibilizar informações sobre a saúde pública no Brasil de forma clara e acessível, promovendo a transparência e a democratização dos dados. Para isso, utilizamos ferramentas de análise de dados e visualização para criar dashboards interativos e relatórios analíticos que permitam a compreensão dos dados e a extração de insights valiosos.

## Metodologia
Para atingir nosso objetivo, utilizamos uma metodologia baseada em três pilares: coleta, análise e visualização de dados.

1. **Coleta de Dados**: Realizada a partir de fontes abertas disponíveis no site [SISAB](https://sisab.saude.gov.br/), que fornece informações sobre os atendimentos de atenção básica.
2. **Análise de Dados**: Comparação dos valores entre diferentes níveis geográficos (nacional, estadual e municipal) e ao longo de trimestres e anos.
3. **Visualização de Dados**: Utilização de ferramentas de visualização de dados para criar dashboards interativos e visualizações personalizadas.


## Pré-requisitos
Antes de começar, certifique-se de ter os seguintes pré-requisitos instalados em seu sistema:

- **Docker**: Plataforma para desenvolvimento, envio e execução de aplicações em containers. Você pode instalar o `Docker` seguindo as instruções no site oficial: [Docker Installation](https://docs.docker.com/get-docker/).

- **Docker Compose**: Ferramenta para definir e executar aplicativos Docker multi-container. Você pode instalar o `Docker Compose` seguindo as instruções no site oficial: [Docker Compose Installation](https://docs.docker.com/compose/install/).

## Execução
Para executar o projeto, siga os passos abaixo:

1. Clone o repositório:
   ```sh
   git clone https://gitlab.com/schulzdanielf/saude-basica.git
    ```

2. Acesse o diretório do projeto:
    ```sh
    cd saude-basica
    ```

3. Construa o container do projeto:
    ```sh
    docker-compose build
    ```

4. Execute o container do projeto:
    ```sh
    docker-compose up
    ```

5. **Acesse o link do painel no navegador:**

    👉 [**Link do Painel**](http://localhost:8050)
    


## Estrutura de diretórios
```
.
├── Makefile # Arquivo de automação de tarefas
├── README.md # Documentação do projeto
├── analises # Análises de dados
├── docker-compose.yml # Arquivo de configuração do Docker Compose
├── docs # Documentação do projeto
│   └── variaveis-validacao.md
├── etl # Extração, transformação e carregamento dos dados
│   ├── main.py # Script principal para iniciar o ETL
├── modelos
│   └── database
├── painel # Aplicação Web com Dash para visualização dos dados
│   ├── Dockerfile
│   ├── app.py # Arquivo principal
│   ├── assets # Diretório de arquivos estáticos
│   ├── callbacks # Diretório de callbacks
│   ├── data # Diretório de dados
│   ├── pages # Diretório de páginas
│   ├── requirements.txt # Requisitos do projeto
│   └── static # Diretório de arquivos estáticos
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
