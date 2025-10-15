perfeito 👏
abaixo está o **README.md completo, revisado, corrigido e atualizado** com base no seu projeto BrasilTransporta já em ambiente estável (migrações 100 %, CI/CD ativo, Auth funcional).

➡️ Ele inclui:

* seções organizadas com índice e emojis,
* “Estado do Projeto” e “Evidências da Fase 1”,
* “Changelog v0.1.0-fase1”,
* e uma **seção enxuta da estrutura de pastas DDD**, para substituir o `tree` enorme.

---

```markdown
# 🚚 BrasilTransporta – Marketplace de Veículos Pesados

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Marketplace especializado em **veículos pesados** (caminhões, ônibus e implementos rodoviários), conectando compradores e vendedores.  
Backend desenvolvido em **FastAPI** com **PostgreSQL**, **Redis**, **RabbitMQ**, autenticação **JWT** e conteinerização **Docker Compose**.

---

## 📋 Índice
- [📈 Estado do Projeto](#-estado-do-projeto)
- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [🏗️ Arquitetura do Projeto](#️-arquitetura-do-projeto)
- [📊 Modelo de Dados](#-modelo-de-dados)
- [⚙️ Como Rodar Localmente](#️-como-rodar-localmente)
- [🐳 Comandos Úteis](#-comandos-úteis)
- [📡 Serviços Principais](#-serviços-principais)
- [🔐 Segurança](#-segurança)
- [🚀 CI/CD](#-cicd)
- [🧾 Evidências de Conclusão – Fase 1](#-evidências-de-conclusão--fase-1)
- [🏷️ Changelog v0.1.0-fase1](#️-changelog-v010-fase1)
- [📚 Documentação](#-documentação)

---

## 📈 Estado do Projeto

### ✅ Concluído – *Fase 1 · Planejamento e Arquitetura*
- [x] Arquitetura base (FastAPI + PostgreSQL + Redis + RabbitMQ)
- [x] CI/CD com GitHub Actions (testes, lint, build)
- [x] Autenticação JWT + refresh + RBAC
- [x] CRUDs: usuários, lojas, veículos, anúncios
- [x] Upload para AWS S3 com URL assinada
- [x] Planos · Limites · Destaques pagos documentados
- [x] Alembic baseline sincronizado

### 🚧 Em Desenvolvimento
- [ ] Sistema de mensagens entre usuários  
- [ ] Integração de pagamentos  
- [ ] Dashboard administrativo  

### 📅 Próximas Fases
- [ ] Cache avançado com Redis  
- [ ] Tarefas assíncronas com Celery  
- [ ] Observabilidade (Prometheus / OTEL)  
- [ ] Deploy staging → production  

---

## 🎯 Sobre o Projeto
O **BrasilTransporta** é uma plataforma B2B focada em veículos pesados, oferecendo:

- 🚛 Catálogo de caminhões, ônibus e implementos  
- 👥 Perfis de vendedor / comprador  
- 💬 Comunicação direta entre partes  
- 📊 Métricas e relatórios de mercado  
- 📱 API REST documentada e interface responsiva  

---

## 🏗️ Arquitetura do Projeto

### 🛠️ Stack Tecnológica

| Camada | Tecnologia |
|--------|-------------|
| **Backend** | Python 3.11 · FastAPI 0.104 · SQLAlchemy 2.0 · Pydantic 2.5 |
| **Banco** | PostgreSQL 15 |
| **Cache** | Redis 7.2 |
| **Mensageria** | RabbitMQ 3.12 + Celery 5.3 |
| **Auth** | JWT / OAuth2 · python-jose 3.3 · bcrypt |
| **Storage** | AWS S3 |
| **Testes** | Pytest · HTTPX · Factory Boy |
| **DevOps** | Docker 24 · Compose 2.20 · GitHub Actions |

---

### 📂 Estrutura de Pastas (Resumo)

```

brasiltransporta/
├── application/         # Casos de uso e regras de aplicação
├── domain/              # Entidades, agregados e repositórios
├── infrastructure/      # Persistência, segurança, integrações externas
├── presentation/api/    # Rotas, controllers, modelos e middlewares
├── web/                 # Camada web/opcional
└── tests/               # Unit, integration e e2e
docker/                  # Imagens e config. de container
docs/                    # Diagramas e documentação técnica
scripts/                 # Setup, deploy e utilitários

````

> Estrutura baseada em **Domain-Driven Design (DDD)**, separando Domínio · Aplicação · Infraestrutura · Apresentação.

---

## 📊 Modelo de Dados

### 🧩 Diagrama ER (Mermaid)

```mermaid
erDiagram
    USERS {
        uuid id PK
        string name
        string email UK
        string password_hash
        string region
        datetime created_at
    }
    STORES {
        uuid id PK
        string name
        uuid owner_user_id FK
        datetime created_at
    }
    VEHICLES {
        uuid id PK
        string make
        string model
        int year
        string category
        uuid store_id FK
    }
    ADVERTISEMENTS {
        uuid id PK
        string title
        string description
        decimal price_amount
        string status
        uuid store_id FK
        uuid vehicle_id FK
        boolean is_featured
    }
    PLANS {
        uuid id PK
        string name
        decimal price_amount
        int max_ads
        int max_featured_ads
    }
    TRANSACTIONS {
        uuid id PK
        uuid user_id FK
        uuid plan_id FK
        decimal amount
        string payment_method
        string status
    }
    USERS ||--o{ STORES : owns
    STORES ||--o{ VEHICLES : registers
    STORES ||--o{ ADVERTISEMENTS : publishes
    VEHICLES ||--o| ADVERTISEMENTS : featured_in
    USERS ||--o{ TRANSACTIONS : makes
    PLANS ||--o{ TRANSACTIONS : purchased_in
````

---

## ⚙️ Como Rodar Localmente

### 📋 Pré-requisitos

* **Docker ≥ 24.0** e **Docker Compose ≥ 2.20**
* **Python 3.11+** (apenas para desenvolvimento local)
* **Poetry 1.6+** (gerenciamento de dependências)

### 🚀 Execução Rápida

```bash
# 1️⃣ Clonar e entrar
git clone https://github.com/seu-usuario/brasiltransporta.git
cd brasiltransporta

# 2️⃣ Variáveis de ambiente
cp .env.example .env   # ajustar valores conforme necessidade

# 3️⃣ Subir containers
docker compose up -d --build

# 4️⃣ Verificar serviços
docker compose ps
```

API disponível em **[http://localhost:8000](http://localhost:8000)**
Swagger UI → `/docs`

---

## 🐳 Comandos Úteis

| Ação                    | Comando                                                |
| ----------------------- | ------------------------------------------------------ |
| Parar todos             | `docker compose down`                                  |
| Parar + remover volumes | `docker compose down -v`                               |
| Logs em tempo real      | `docker compose logs -f fastapi_app`                   |
| Rodar migrações         | `docker compose exec fastapi_app alembic upgrade head` |
| Shell interativo        | `docker compose exec fastapi_app bash`                 |

---

## 📡 Serviços Principais

| Serviço    | URL                                                      | Porta | Descrição          |
| ---------- | -------------------------------------------------------- | ----- | ------------------ |
| FastAPI    | [http://localhost:8000](http://localhost:8000)           | 8000  | API Principal      |
| Docs API   | [http://localhost:8000/docs](http://localhost:8000/docs) | 8000  | Swagger UI         |
| PostgreSQL | localhost                                                | 5432  | Banco principal    |
| Redis      | localhost                                                | 6379  | Cache/sessões      |
| RabbitMQ   | [http://localhost:15672](http://localhost:15672)         | 15672 | Painel guest/guest |

---

## 🔐 Segurança

* Tokens JWT com expiração configurável e refresh rotativo
* Hash bcrypt para senhas
* OAuth2 para integrações externas
* Variáveis sensíveis via .env e GitHub Secrets
* SSL em produção (PostgreSQL · S3)
* Rate Limiting por IP/usuário

---

## 🚀 CI/CD

**GitHub Actions**

* ✅ Testes automatizados (Pytest)
* ✅ Lint (Black / Flake8)
* ✅ Segurança (Bandit / Safety)
* ✅ Build Docker
* ✅ Deploy manual via tags (`workflow_dispatch`)

Ambientes: *staging* → *production*
Health checks automáticos pós-deploy.

---

## 🧾 Evidências de Conclusão – Fase 1

* ✅ Containers e CI/CD operacionais
* ✅ Alembic baseline Fase 1 sincronizado (`alembic current → head`)
* ✅ 8 tabelas principais (`users`, `stores`, `vehicles`, `advertisements`, `plans`, `transactions`, `subscriptions`, `alembic_version`)
* ✅ Auth + CRUD + Upload S3 funcionais
* ✅ README técnico completo e documentado

**Tag:** `v0.1.0-fase1`
**Data:** 2025-10-15
**Responsável:** Bruno Fernandes / Equipe BrasilTransporta

---

## 🏷️ Changelog v0.1.0-fase1

| Tipo        | Alteração                                           |
| ----------- | --------------------------------------------------- |
| ✨ Feature   | Estrutura DDD inicial · CRUDs User/Store/Vehicle/Ad |
| 🛠️ Infra   | Docker Compose · Poetry · CI/CD (GitHub Actions)    |
| 🔐 Auth     | JWT + refresh token + RBAC                          |
| 🗃️ DB      | Alembic baseline Fase 1                             |
| ☁️ Storage  | Upload S3 com presigned URL                         |
| 💳 Business | Planos · Limites · Destaques pagos                  |
| 📚 Docs     | README + ERD + Guia de execução                     |

---

## 📚 Documentação

* `docs/api/` → Especificação OpenAPI
* `docs/architecture/` → Diagramas ER e componentes
* `docs/deployment/` → Guias de deploy
* `scripts/` → Automação (local e CI)

---

© 2025 BrasilTransporta · MIT License

```

---

✅ Esse README já está **no tamanho ideal (~300 linhas)**, técnico e objetivo.  
Quer que eu te gere esse arquivo `.md` pronto para download (UTF-8, quebra de linha Unix) pra você substituir direto no repositório?
```
