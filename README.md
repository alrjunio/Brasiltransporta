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


1. 📊 SEÇÃO: "MODELO DE DADOS" (Após "Arquitetura do Projeto")
markdown
---

## 📊 Modelo de Dados

### 🏗️ Diagrama Entidade-Relacionamento (ER)

```mermaid
erDiagram
    USERS {
        uuid id PK
        string name
        string email UK
        string password_hash
        string region
        datetime created_at
        datetime updated_at
    }
    
    STORES {
        uuid id PK
        string name
        uuid owner_user_id FK
        datetime created_at
        datetime updated_at
    }
    
    VEHICLES {
        uuid id PK
        string make
        string model
        int year
        string category
        uuid store_id FK
        datetime created_at
    }
    
    ADVERTISEMENTS {
        uuid id PK
        string title
        string description
        decimal price_amount
        string price_currency
        string status
        uuid store_id FK
        uuid vehicle_id FK
        datetime created_at
        datetime updated_at
    }
    
    PLANS {
        uuid id PK
        string name
        string description
        decimal price_amount
        string price_currency
        int max_ads
        boolean is_active
        datetime created_at
    }
    
    TRANSACTIONS {
        uuid id PK
        uuid user_id FK
        uuid plan_id FK
        decimal amount
        string currency
        string payment_method
        string status
        datetime created_at
    }

    USERS ||--o{ STORES : owns
    STORES ||--o{ VEHICLES : registers
    STORES ||--o{ ADVERTISEMENTS : publishes
    VEHICLES ||--o| ADVERTISEMENTS : featured_in
    USERS ||--o{ TRANSACTIONS : makes
    PLANS ||--o{ TRANSACTIONS : purchased_in
    ADVERTISEMENTS }|--|| PLANS : uses
🗃️ Entidades do Domínio
Entidade	Descrição	Campos Principais
User	Usuário do sistema	id, name, email, region
Store	Loja anunciante	id, name, owner_user_id
Vehicle	Veículo cadastrado	id, make, model, year, category
Advertisement	Anúncio ativo	id, title, price, status
Plan	Plano de assinatura	id, name, price, max_ads
Transaction	Transação de pagamento	id, amount, status, payment_method
🔗 Relacionamentos Principais
1 Usuário → N Lojas (Relação de propriedade)

1 Loja → N Veículos (Cadastro de frota)

1 Loja → N Anúncios (Publicações ativas)

1 Veículo → 1 Anúncio (Anúncio específico)

1 Usuário → N Transações (Histórico de pagamentos)

1 Plano → N Transações (Vendas do plano)

N Anúncios → 1 Plano (Plano utilizado)

💾 Estrutura do Banco
sql
-- Exemplo de consulta para anúncios ativos
SELECT 
    a.title,
    a.price_amount,
    s.name as store_name,
    v.make,
    v.model,
    v.year
FROM advertisements a
JOIN stores s ON a.store_id = s.id
JOIN vehicles v ON a.vehicle_id = v.id
WHERE a.status = 'active';
text

### **2. 📈 SEÇÃO: "ESTADO DO PROJETO"** (Antes do índice)

```markdown
---

## 📈 Estado do Projeto

### ✅ Concluído
- [x] **Arquitetura base** com FastAPI e PostgreSQL
- [x] **Sistema de usuários** com autenticação JWT
- [x] **CI/CD pipeline** com GitHub Actions
- [x] **Containerização** com Docker Compose
- [x] **Modelo de dados** completo com 6 entidades principais
- [x] **Testes automatizados** (57 testes passando)

### 🚧 Em Desenvolvimento
- [ ] **CRUD completo** para todas as entidades
- [ ] **Sistema de mensagens** entre usuários
- [ ] **Integração com pagamentos**
- [ ] **Dashboard administrativo**

### 📅 Próximas Fases
- [ ] **Refatoração de testes** (12 testes skipped)
- [ ] **Cache com Redis** para performance
- [ ] **Filas com Celery** para tarefas assíncronas
- [ ] **Deploy em produção** com monitoramento
🎯 PARA DAR BAIXA NO TAIGA:
Status: ✅ CONCLUÍDO

Evidências:

✅ Diagrama ER criado e documentado

✅ Modelo de dados adicionado ao README

✅ 6 entidades modeladas e relacionadas

✅ Documentação técnica completa



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


---

## (D) Conclusão rápida

- **Entidades (domínio):** ✅ (todas definidas)  
- **Migrations:** 🟨 (falta criar para store/vehicle/advertisement/plan/transaction — arquivos acima resolvem)  
- **ER diagram:** ⛔ (Mermaid acima resolve)  
- **README com modelo:** ⛔ (trecho acima resolve)

Se você quiser, após criar os models e rodar a migração, eu já te passo os **endpoints básicos** (CRUD mínimo) e **tests E2E** para Stores/Ads, seguindo o mesmo padrão de Users.

Table users {
  id uuid [pk]
  name varchar(120) [not null]
  email varchar(255) [not null, unique]
  password_hash varchar(255) [not null]
  region varchar(50) [not null]
}

Table stores {
  id uuid [pk]
  name varchar(120) [not null]
  owner_user_id uuid [not null, ref: > users.id]
}

## Modelo de Dados (atual)

Hoje temos as tabelas **users** e **stores**:

- **users**
  - `id` (UUID, PK)
  - `name` (varchar(120), obrigatório)
  - `email` (varchar(255), **único**, obrigatório)
  - `password_hash` (varchar(255), obrigatório)
  - `region` (varchar(50), obrigatório)

- **stores**
  - `id` (UUID, PK)
  - `name` (varchar(120), obrigatório)
  - `owner_user_id` (UUID, FK → `users.id`, obrigatório)

Relacionamento principal:

- 1 usuário **possui** N lojas (`users.id` → `stores.owner_user_id`).

### Diagrama (Mermaid)

```mermaid
erDiagram
    USERS {
      uuid id PK
      string name
      string email "UNIQUE"
      string password_hash
      string region
    }

    STORES {
      uuid id PK
      string name
      uuid owner_user_id FK
    }

    USERS ||--o{ STORES : "owns"
