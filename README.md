# 🚚 BrasilTransporta - Marketplace de Veículos Pesados

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Projeto em desenvolvimento para criação de um **Marketplace de Veículos Pesados**, conectando compradores e vendedores de caminhões, ônibus e equipamentos pesados com backend em **FastAPI**, banco de dados **PostgreSQL** e conteinerização via **Docker**.

---

## 📋 Índice

- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [🏗️ Arquitetura do Projeto](#️-arquitetura-do-projeto)
- [⚙️ Como Rodar Localmente](#️-como-rodar-localmente)
- [🐳 Comandos Úteis](#-comandos-úteis)
- [📡 Serviços e Endpoints](#-serviços-e-endpoints)
- [🔧 Desenvolvimento](#-desenvolvimento)
- [🚀 CI/CD](#-cicd)
- [🔐 Segurança](#-segurança)
- [📚 Documentação](#-documentação)

---

## 🎯 Sobre o Projeto

O **BrasilTransporta** é uma plataforma marketplace especializada em veículos pesados, oferecendo:

- 🚛 **Catálogo de veículos** pesados (caminhões, ônibus, implementos rodoviários)
- 👥 **Perfis de usuários** para vendedores e compradores
- 💬 **Sistema de mensagens** entre partes interessadas
- 📊 **Análises e métricas** de mercado
- 📱 **Interface responsiva** para diversos dispositivos

---

## 🏗️ Arquitetura do Projeto
brasiltransporta/
├── backend/ # Código fonte FastAPI
│ ├── app/ # Aplicação principal
│ │ ├── api/ # Endpoints da API
│ │ ├── core/ # Configurações e segurança
│ │ ├── models/ # Modelos de dados
│ │ └── services/ # Lógica de negócio
│ └── tests/ # Testes automatizados
├── docker/ # Configurações Docker
├── docs/ # Documentação
├── scripts/ # Scripts de automação
└── docker-compose.yml # Orquestração de containers


### 🛠️ Stack Tecnológica

- **Backend**: Python 3.11, FastAPI 0.104.1, SQLAlchemy 2.0, Pydantic 2.5
- **Database**: PostgreSQL 15, Redis 7.2
- **Message Broker**: RabbitMQ 3.12
- **Queue**: Celery 5.3
- **Container**: Docker 24+, Docker Compose 2.20+
- **Auth**: JWT, OAuth2, Python-Jose 3.3
- **File Storage**: AWS S3
- **Testing**: Pytest, HTTPX, Factory Boy

---

## ⚙️ Como Rodar Localmente

### 📋 Pré-requisitos

- **Docker** versão 24.0+ e **Docker Compose** versão 2.20+
- **Python** 3.11.5+ (apenas para desenvolvimento)
- **Poetry** 1.6.0+ (gerenciamento de dependências)

### 🚀 Execução Rápida

**Clonar o repositório**
   ```bash
   git clone https://github.com/seu-usuario/brasiltransporta.git
   cd brasiltransporta

Configurar variáveis de ambiente

# Copiar e ajustar variáveis
cp .env.example .env
# Editar o arquivo .env com suas configurações

Instalar dependências com Poetry (desenvolvimento)

poetry install
poetry shell  # Ativar ambiente virtual

Executar containers

# Iniciar todos os serviços
docker-compose up -d --build

# Ou para desenvolvimento com logs
docker-compose up --build

Executar setup inicial 

# PowerShell (Windows)
pwsh ./scripts/setup.ps1

# Bash (Linux/Mac)
bash ./scripts/setup.sh

Verificar serviços

docker-compose ps

🐳 Comandos Úteis

Gestão de Containers

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (dados)
docker-compose down -v

# Ver logs em tempo real
docker-compose logs -f [serviço]

# Recriar containers específicos
docker-compose up -d --build --force-recreate backend db

# Executar comandos em containers
docker-compose exec backend python -m pytest

Desenvolvimento

# Rodar testes
pwsh ./scripts/test-local.ps1
# ou
bash ./scripts/test-local.sh

# Ver qualidade de código
poetry run black app/ --check
poetry run flake8 app/

# Aplicar formatação automática
poetry run black app/
poetry run isort app/

📡 Serviços e Endpoints
Serviço	        URL	                        Porta	        Descrição
FastAPI	        http://localhost:8000	    8000	        API Principal
Docs API	    http://localhost:8000/docs	8000	        Documentação Interativa
PostgreSQL	    localhost	                5432	        Banco de dados principal
Redis	        localhost	                6379	        Cache e sessões
RabbitMQ	    http://localhost:15672	    15672	        Management UI (guest/guest)

🔌 Exemplos de Uso da API

# Health Check
curl http://localhost:8000/health

# Listar veículos (exemplo)
curl -H "Authorization: Bearer {token}" http://localhost:8000/api/veiculos


🔧 Desenvolvimento

# Instalar pre-commit hooks
pre-commit install

# Rodar testes específicos
poetry run pytest tests/ -v

# Rodar testes com cobertura
poetry run pytest --cov=app tests/

# Debug com containers
docker-compose exec backend bash

🔍 Troubleshooting Comum

# Solução: Verificar se PostgreSQL está rodando
docker-compose ps | grep db
docker-compose logs db


🚀 CI/CD
GitHub Actions
O projeto possui pipelines configurados para:

✅ Testes Automatizados
Trigger: Push em PRs para main/develop

Execução: Linux runner Ubuntu 22.04

Ações:

✅ Testes com pytest

✅ Qualidade código (Black, Flake8)

✅ Segurança (Bandit, Safety)

✅ Build de containers

🚀 Deploy
Trigger: Manual (workflow_dispatch) ou push em tags

Ambientes: staging → production

Ações:

🏗️ Build e push de imagens Docker

🚀 Deploy com Docker Compose

📊 Health checks automáticos

🔐 Segurança
Autenticação & Autorização
JWT tokens com expiração configurável

OAuth2 flow para integrações

Hash de senhas com bcrypt

Rate limiting por IP/usuário

Configurações Sensíveis
Variáveis via ambiente (.env)

Segredos gerenciados no GitHub Secrets

SSL/HTTPS em produção

Armazenamento
AWS S3 para arquivos estáticos

PostgreSQL com conexões SSL

Redis com autenticação

📚 Documentação
📖 Documentação Disponível
docs/api/ - Especificação completa da API

docs/architecture/ - Diagramas de arquitetura

docs/deployment/ - Guias de deploy