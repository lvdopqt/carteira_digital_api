# Carteira Digital API

Este projeto implementa uma API para uma "Carteira Digital Municipal", simulando funcionalidades como gestão de usuários, autenticação, gestão de documentos digitais, consulta e recarga de saldo de transporte público (mockado) e uma interação simples com um chatbot.

## Funcionalidades Implementadas

* **Autenticação e Autorização:** Cadastro de usuários, login via JWT, proteção de endpoints com base no usuário autenticado.

* **Gestão de Usuários:** Criação de novos usuários.

* **Gestão de Documentos:** Armazenamento e listagem de documentos digitais associados a um usuário.

* **Transporte Público (Mockado):** Consulta de saldo e simulação de recarga de passe de transporte.

* **Chatbot (Simples):** Endpoint que recebe perguntas e retorna respostas pré-definidas.

* **Health Check:** Endpoint simples para verificar se a API está online.

## Stack Tecnológica

* **Framework Web:** FastAPI

* **ORM:** SQLAlchemy

* **Banco de Dados:** PostgreSQL (via Docker)

* **Validação de Dados:** Pydantic

* **Hashing de Senhas:** Passlib (bcrypt)

* **JWT:** Python-Jose

* **Gerenciamento de Dependências:** Pip / Virtual Environments

* **Migrações de Banco de Dados:** Alembic

* **Containerização:** Docker / Docker Compose

* **Testes:** Pytest, Httpx, Pytest-Asyncio

* **CI/CD:** GitHub Actions

## Estrutura do Código

O projeto segue uma estrutura modular e em camadas para separar as responsabilidades:

* `alembic/`: Arquivos de configuração e scripts para migrações de banco de dados com Alembic.

* `app/`: Contém o código principal da aplicação.

  * `api/`: Agrega os routers versionados.

    * `v1/`: Contém os routers específicos da versão 1 da API.

  * `core/`: Configurações da aplicação (settings), segurança (JWT) e hashing.

  * `db/`: Configuração da conexão com o banco de dados, base declarativa do ORM e dependência de sessão.

  * `dependencies/`: Funções de dependência reutilizáveis (como a dependência do UserService).

  * `models/`: Definições dos modelos ORM do SQLAlchemy que mapeiam as tabelas do banco de dados.

  * `repos/`: Camada de repositório, responsável pela interação direta com o banco de dados (CRUD).

  * `routes/`: Definição dos endpoints da API usando `APIRouter`, agrupados por funcionalidade (auth, users, documents, etc.).

  * `schemas/`: Definições dos schemas de dados Pydantic para validação de requisições, serialização de respostas e modelos de dados.

  * `services/`: Camada de serviço, contém a lógica de negócio, orquestra as interações entre repositórios e outras partes da aplicação.

  * `main.py`: Ponto de entrada da aplicação FastAPI, onde os routers principais são incluídos.

* `tests/`: Contém os testes automatizados para a API e outras partes do código.

  * `api/`: Testes para os endpoints da API.

  * `conftest.py`: Fixtures e configurações globais para os testes.

* `docker-compose.yml`: Define os serviços Docker (aplicação e banco de dados) e como eles se relacionam.

* `Dockerfile`: Define como construir a imagem Docker da aplicação.

* `requirements.txt`: Lista as dependências do projeto.

## Configuração e Como Rodar o Projeto

### Pré-requisitos

* Python 3.8+

* Docker e Docker Compose

* Git

### Passos para Configuração

1. **Clone o repositório:**

```
git clone <url_do_repositorio>
cd <pasta_criada>
```


2. **Crie e ative um ambiente virtual:**

```
python -m venv .venv
source .venv/bin/activate # No Windows use .venv\Scripts\activate
```

3. **Instale as dependências:**

```
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis (ajuste os valores conforme necessário, especialmente para o banco de dados se não usar o Docker Compose padrão):

```
DATABASE_URL=postgresql://user:password@db:5432/carteira_db
SECRET_KEY=sua_chave_secreta_forte_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440 # 60 * 24 (1 dia)
API_V1_STR=/api/v1
DEBUG=True
```

**Importante:** 
Para rodar o Alembic localmente contra o banco de dados no Docker Compose, você precisará temporariamente ajustar `DATABASE_URL` no seu ambiente local para apontar para `localhost` (ex: `postgresql://user:password@localhost:5432/carteira_db`) ou rodar o comando Alembic com a variável de ambiente sobrescrita.

5. **Inicie o banco de dados com Docker Compose:**

```
docker-compose up -d db
```


Aguarde alguns instantes para o contêiner do PostgreSQL iniciar completamente.

6. **Execute as migrações do banco de dados:**
Certifique-se de que seu ambiente virtual está ativado e o contêiner `db` está rodando. Se estiver rodando Alembic localmente contra o DB no Docker, certifique-se de que sua `DATABASE_URL` aponta para `localhost`.

```
alembic upgrade head
```

Isso criará as tabelas `users` e `documents` (e quaisquer outras que você tenha definido e migrado) no banco de dados.

7. **Inicie a aplicação:**
Certifique-se de que seu ambiente virtual está ativado e os contêineres `db` e `web` (se estiver usando Docker Compose para a aplicação) estão rodando. Se estiver rodando a aplicação localmente, certifique-se de que sua `DATABASE_URL` aponta para `localhost`.

```
uvicorn app.main:app --reload
```


A API estará disponível em `http://127.0.0.1:8000`.

## Rodando os Testes

Para executar a suíte de testes Pytest:

1. Certifique-se de que seu ambiente virtual está ativado.

2. Certifique-se de que o banco de dados (contêiner `db` ou local) está acessível. Os testes usam um banco de dados SQLite em memória por padrão, então o contêiner `db` não é estritamente necessário *para rodar os testes*, mas é necessário para o Alembic e a aplicação.

3. Execute o comando:

```
pytest
```

## CI/CD com GitHub Actions

O projeto inclui um workflow de CI configurado com GitHub Actions na pasta `.github/workflows/ci.yml`. Este workflow é disparado em pushes e pull requests para o branch `main`. Ele configura o ambiente Python, instala as dependências e executa os testes automaticamente, fornecendo feedback sobre a saúde do código.

## Documentação da API

A API é autodocumentada usando o padrão OpenAPI do FastAPI. Com a aplicação rodando localmente, você pode acessar:

* **Documentação Interativa (Swagger UI):** `http://127.0.0.1:8000/docs`

* **Documentação Interativa (Redoc):** `http://127.0.0.1:8000/redoc`

* **Esquema OpenAPI (JSON):** `http://127.0.0.1:8000/openapi.json`

A documentação inclui informações sobre os endpoints, parâmetros, schemas de requisição/resposta e tags para organizar as funcionalidades.

