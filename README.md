# RESTful API com Flask: Backend Robusto com Docker, PostgreSQL e Testes Automatizados

Este projeto é uma API RESTful desenvolvida com Flask, estruturada para oferecer um backend sólido e escalável. Utiliza Docker para conteinerização, PostgreSQL como banco de dados relacional e inclui testes automatizados para garantir a qualidade do código.

## 🧱 Estrutura do Projeto
├── application/ # Código-fonte da aplicação Flask
├── tests/ # Testes automatizados com pytest
├── kubernetes/ # Manifests para implantação em Kubernetes
├── docker-compose.yaml # Orquestração de serviços com Docker Compose
├── dockerfile # Dockerfile para criação da imagem da aplicação
├── requirements.txt # Dependências do projeto
├── config.py # Configurações da aplicação
├── wsgi.py # Ponto de entrada para servidores WSGI
├── Makefile # Comandos utilitários para automação
├── .flake8 # Configurações do Flake8 para linting
├── conftest.py # Configurações para os testes
└── LICENSE # Licença MIT

## ⚙️ Tecnologias Utilizadas

- **Flask**: Framework web leve e flexível para Python.
- **PostgreSQL**: Banco de dados relacional robusto.
- **Docker**: Conteinerização da aplicação para ambientes consistentes.
- **Docker Compose**: Orquestração de múltiplos containers.
- **Kubernetes**: Implantação e gerenciamento de containers em escala.
- **pytest**: Framework de testes para Python.
- **Flake8**: Ferramenta de linting para manter a qualidade do código.

## 🚀 Como Executar o Projeto

 **Clone o repositório:**

   ```bash
   git clone https://github.com/Lucas-Casa-Mausa/restapi-flask.git
   cd restapi-flask
   
   Construa e inicie os containers:

   Copiar
   Editar
   docker-compose up --build
   Isso iniciará a aplicação Flask e o banco de dados PostgreSQL.
    
   Acesse a API:    
   A aplicação estará disponível em http://localhost:5000.
    
   🧪 Executando os Testes
   Para rodar os testes automatizados:
    
   bash
   Copiar
   Editar
   docker-compose exec web pytest
   🧹 Linting do Código
   Para verificar a qualidade do código com Flake8:
    
   bash
   Copiar
   Editar
   docker-compose exec web flake8
```
