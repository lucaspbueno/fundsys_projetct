# Arquitetura do Backend - FundSys

## Visão Geral

O backend foi refatorado seguindo o padrão arquitetural **Controller → Service → Persistence**, garantindo separação de responsabilidades e manutenibilidade.

## Estrutura de Pastas

```
backend/
├── app/
│   ├── controllers/          # Camada de Controle (API Endpoints)
│   │   ├── file.py          # Upload de arquivos XML
│   │   ├── analytics.py     # Analytics gerais
│   │   └── history.py       # Histórico de arquivos
│   ├── services/            # Camada de Serviços (Lógica de Negócio)
│   │   ├── file.py          # Processamento de arquivos
│   │   ├── analytics.py     # Serviços de analytics
│   │   └── history.py       # Serviços de histórico
│   ├── persiste/            # Camada de Persistência
│   │   ├── queries/         # Consultas ao banco
│   │   │   ├── analytics.py # Queries de analytics
│   │   │   └── history.py   # Queries de histórico
│   │   └── util/            # Inserções no banco
│   │       ├── ativo.py
│   │       ├── indexador.py
│   │       ├── lote.py
│   │       └── posicao.py
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── ativo.py
│   │   ├── indexador.py
│   │   ├── lote.py
│   │   ├── posicao.py
│   │   └── utils/
│   ├── schemas/             # Schemas Pydantic (DTOs)
│   │   ├── analytics.py     # DTOs de analytics
│   │   ├── history.py       # DTOs de histórico
│   │   └── upload_files_response.py
│   ├── DTOs/                # DTOs de parsing
│   │   ├── ativo.py
│   │   ├── indexador.py
│   │   ├── lote.py
│   │   ├── posicao.py
│   │   └── parserd_bundle.py
│   └── config/              # Configurações
│       ├── db.py
│       └── settings.py
├── alembic/                 # Migrações do banco
├── main.py                  # Aplicação FastAPI
└── pyproject.toml          # Dependências
```

## Fluxo de Dados

### 1. Upload de Arquivos
```
Controller (file.py) 
    → Service (file.py) 
    → Parser (XML → DTOs) 
    → Persistence (util/) 
    → Database
```

### 2. Consultas de Analytics
```
Controller (analytics.py) 
    → Service (analytics.py) 
    → Persistence (queries/analytics.py) 
    → Database 
    → Schema (analytics.py) 
    → Response
```

### 3. Consultas de Histórico
```
Controller (history.py) 
    → Service (history.py) 
    → Persistence (queries/history.py) 
    → Database 
    → Schema (history.py) 
    → Response
```

## Camadas da Arquitetura

### 1. **Controllers** (`/controllers/`)
- **Responsabilidade**: Receber requisições HTTP e retornar respostas
- **Tecnologias**: FastAPI, Pydantic
- **Padrão**: Endpoints REST com validação de entrada/saída

**Exemplo:**
```python
@analytics_routes.get("/overview", response_model=OverviewResponse)
async def get_overview(db: Session = Depends(get_db)):
    return get_overview_service(db)
```

### 2. **Services** (`/services/`)
- **Responsabilidade**: Lógica de negócio e orquestração
- **Tecnologias**: Python puro, SQLAlchemy Session
- **Padrão**: Funções que coordenam operações complexas

**Exemplo:**
```python
def get_overview_service(db: Session) -> OverviewResponse:
    data = get_overview_data(db)
    return OverviewResponse(**data)
```

### 3. **Persistence** (`/persiste/`)
- **Responsabilidade**: Acesso aos dados
- **Tecnologias**: SQLAlchemy ORM
- **Padrão**: Separação entre queries (consultas) e util (inserções)

**Exemplo:**
```python
def get_overview_data(db: Session) -> Dict[str, Any]:
    total_ativos = db.query(Ativo).count()
    # ... outras consultas
    return {"total_ativos": total_ativos, ...}
```

### 4. **Models** (`/models/`)
- **Responsabilidade**: Representação das tabelas do banco
- **Tecnologias**: SQLAlchemy ORM
- **Padrão**: Herança de BaseModel + TimestampMixin

### 5. **Schemas** (`/schemas/`)
- **Responsabilidade**: Validação e serialização de dados
- **Tecnologias**: Pydantic
- **Padrão**: DTOs para entrada/saída da API

## Vantagens da Arquitetura

### ✅ **Separação de Responsabilidades**
- Controllers: Apenas HTTP
- Services: Lógica de negócio
- Persistence: Acesso aos dados

### ✅ **Testabilidade**
- Cada camada pode ser testada independentemente
- Mocks fáceis de implementar

### ✅ **Manutenibilidade**
- Mudanças isoladas por camada
- Código organizado e legível

### ✅ **Reutilização**
- Services podem ser reutilizados
- Queries centralizadas

### ✅ **Escalabilidade**
- Fácil adição de novas funcionalidades
- Padrão consistente

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validação de dados
- **Alembic**: Migrações do banco
- **PostgreSQL**: Banco de dados
- **Docker**: Containerização

## Endpoints Disponíveis

### Upload de Arquivos
- `POST /api/file/upload_files` - Upload de arquivos XML

### Analytics
- `GET /api/analytics/overview` - Visão geral
- `GET /api/analytics/indexadores` - Estatísticas dos indexadores
- `GET /api/analytics/ativos` - Lista de ativos
- `GET /api/analytics/evolucao-mensal` - Evolução mensal

### Histórico
- `GET /api/history/files` - Lista de arquivos
- `GET /api/history/files/{id}` - Detalhes de um arquivo
- `GET /api/history/files/{id}/analytics` - Analytics de um arquivo

## Próximos Passos

1. **Testes Unitários**: Implementar testes para cada camada
2. **Documentação API**: Swagger/OpenAPI automático
3. **Cache**: Redis para consultas frequentes
4. **Logging**: Estruturado com diferentes níveis
5. **Monitoramento**: Métricas e health checks
