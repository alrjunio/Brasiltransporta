# 🚚 BrasilTransporta - Marketplace de Veículos Pesados

Projeto em desenvolvimento para criação de um **Marketplace de Veículos Pesados**, com backend em **FastAPI**, banto de dados **PostgreSQL** e conteinerização via **Docker**.

---

## 📌 Tecnologias Usadas

- **Backend**: Python 3.11, FastAPI, SQLAlchemy
- **Database**: PostgreSQL, Redis
- **Message Broker**: RabbitMQ
- **Queue**: Celery
- **Container**: Docker, Docker Compose
- **Auth**: JWT, OAuth2
- **File Storage**: AWS S3

---

## 🏗️ Arquitetura do Projeto
brasiltransporta/
├── backend/ # Código fonte FastAPI
│ ├── app/ # Aplicação principal
│ └── tests/ # Testes automatizados
├── docker/ # Configurações Docker
└── docs/ # Documentação


---

## ⚙️ Como Rodar Localmente

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento)
- Poetry (gerenciamento de dependências)

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/brasiltransporta.git
cd brasiltransporta

2. Instalar dependências com Poetry
poetry install

3. Rodar containers do projeto
docker-compose up -d --build

4. Executar scripts auxiliares (opcional)
# Setup inicial (ex.: criar banco de dados, seeds)
pwsh ./scripts/setup.ps1

# Rodar testes locais
pwsh ./scripts/test-local.ps1

5. Acessar a aplicação

Backend FastAPI: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

📦 CI/CD - GitHub Actions

O projeto possui pipelines configurados para:

Testes automatizados

Rodam em Linux runner

Executam pytest para validar backend

Verificam qualidade de código com Black e Flake8

Deploy

Pipeline acionável manualmente (workflow_dispatch)

Executa Docker Compose para deploy em ambiente de produção (configurado futuramente)

📚 Documentação Adicional

Documentação detalhada da API será disponibilizada em docs/

Configurações Docker detalhadas em docker/

Scripts de setup e testes em scripts/

🔐 Segurança

Autenticação via JWT e OAuth2

Armazenamento de arquivos em AWS S3

Configurações sensíveis via variáveis de ambiente

