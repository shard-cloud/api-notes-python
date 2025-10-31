## 📖 O que é este template?

API REST completa para gerenciamento de notas pessoais construída com **FastAPI**, **SQLAlchemy**, **Alembic** e **PostgreSQL**. Inclui autenticação por token JWT, CRUD completo, busca e paginação.

## 🎯 Casos de uso

- **Notas pessoais:** Sistema de anotações privadas
- **Backend para apps:** API para aplicativos de notas (mobile/web)
- **Aprendizado:** Exemplo de API REST com autenticação
- **Base para projetos:** Ponto de partida para sistemas maiores
- **Microserviço:** Componente de sistema de produtividade

## ✨ Características principais

### API REST Completa

- ✅ CRUD completo de notas (Create, Read, Update, Delete)
- ✅ Autenticação JWT com tokens seguros
- ✅ Busca por título e conteúdo
- ✅ Paginação de resultados
- ✅ Filtros e ordenação
- ✅ Validação robusta de dados

### Segurança

- 🔐 Autenticação por token JWT
- 🔒 Senhas hasheadas com bcrypt
- 🛡️ Validação de entrada (Pydantic)
- 🚫 Proteção de rotas sensíveis
- ⏰ Tokens com expiração configurável

### Performance e Escalabilidade

- ⚡ FastAPI (framework mais rápido do Python)
- 🗄️ SQLAlchemy ORM (async/await)
- 📊 Queries otimizadas
- 🔄 Connection pooling
- 📦 Build otimizado com Docker

### Qualidade de Código

- ✅ Validação com Pydantic
- ✅ Tratamento robusto de erros
- ✅ Logs estruturados
- ✅ Type hints completos
- ✅ Testes automatizados (pytest)

### DevOps

- 🐳 Docker e Docker Compose
- 🔄 Migrations com Alembic
- 🌱 Seeds para desenvolvimento
- 🏥 Health check endpoint
- 📊 Documentação automática (Swagger)

## 🏗️ Arquitetura

```
api-notes-python/
├── alembic/               # Migrations
├── src/
│   ├── main.py            # Entry point FastAPI
│   ├── config.py          # Configurações
│   ├── database.py        # Models e conexão DB
│   ├── schemas.py         # Pydantic schemas
│   ├── auth.py            # Autenticação JWT
│   └── routes/            # Endpoints
│       ├── auth.py        # Login/registro
│       └── notes.py       # CRUD de notas
├── seed/                  # Scripts de seed
├── tests/                 # Testes pytest
└── docs/                  # Documentação
```

### Stack Tecnológica

- **Runtime:** Python 3.11+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy (async)
- **Migrations:** Alembic
- **Database:** PostgreSQL
- **Auth:** JWT + bcrypt
- **Validation:** Pydantic
- **Tests:** pytest
- **Container:** Docker + Docker Compose

## 📊 Modelo de Dados

### User (Usuário)
```python
class User:
    id: int
    username: str (unique)
    email: str (unique)
    hashed_password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

### Note (Nota)
```python
class Note:
    id: int
    title: str
    content: str (optional)
    user_id: int (foreign key)
    created_at: datetime
    updated_at: datetime
```

## 🔗 Endpoints Disponíveis

### Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/token` | Login (obter token) |
| POST | `/auth/register` | Registro de usuário |

### Notas (Requer autenticação)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/notes/` | Listar notas (paginado) |
| GET | `/notes/{id}` | Buscar nota por ID |
| POST | `/notes/` | Criar nova nota |
| PUT | `/notes/{id}` | Atualizar nota |
| DELETE | `/notes/{id}` | Deletar nota |

### Sistema
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check |
| GET | `/docs` | Documentação Swagger |
| GET | `/redoc` | Documentação ReDoc |

## 🔐 Fluxo de Autenticação

1. **Registro:** POST `/auth/register` com username, email, password
2. **Login:** POST `/auth/token` com username, password
3. **Token:** Recebe JWT token válido por 24h
4. **Uso:** Header `Authorization: Bearer TOKEN` em todas as requisições
5. **Expiração:** Token expira automaticamente

## 🚀 Quick Start

```bash
# Clone e acesse
cd api-notes-python

# Suba com Docker Compose
docker-compose up -d

# Rode migrations
docker-compose exec api alembic upgrade head

# Crie usuário inicial
docker-compose exec api python seed/create_user.py

# Teste
curl http://localhost:80/health
curl -X POST http://localhost:80/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## 📈 Performance Esperada

- **Latência:** < 50ms para queries simples
- **Throughput:** > 5k requests/segundo
- **Memória:** ~100MB em idle
- **Startup:** < 5 segundos

## 🔄 Próximos passos

Continue para [Configuração](./02-configuracao.md) para setup detalhado.
