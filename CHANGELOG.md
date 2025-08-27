# Changelog
Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.  
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)  
e este projeto adota [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [0.2.0] - 2025-08-27
### Added
- Configuração do **Alembic** e suporte a migrações. :contentReference[oaicite:0]{index=0}
- Template de **Pull Request** para padronização das contribuições. :contentReference[oaicite:1]{index=1}
- **Modelos base**: `BaseModel` e `TimestampMixin`. :contentReference[oaicite:2]{index=2}

### Changed
- Migração do gerenciamento de dependências para o **Poetry** (com documentação da versão do Python) e atualização de **Dockerfile/docker-compose**; `entrypoint` para executar migrações no startup. :contentReference[oaicite:3]{index=3}

### Fixed
- Bump da versão do projeto para **0.2.0** no `pyproject.toml`. :contentReference[oaicite:4]{index=4}

---

## [0.1.0] - 2025-08-26
### Added
- Inicialização do projeto com **FastAPI** e **SQLAlchemy**. :contentReference[oaicite:5]{index=5}
- Arquivos de configuração do ambiente e Docker. :contentReference[oaicite:6]{index=6}
- Configuração de **logging** (inicial) e updates de requirements. :contentReference[oaicite:7]{index=7}
- Dependências **psycopg2-binary** e **pydantic-settings**. :contentReference[oaicite:8]{index=8}
- Atualização do `.env-exemple` com `POSTGRES_HOST`. :contentReference[oaicite:9]{index=9}
- Correções de caminhos de diretório em Dockerfile/docker-compose. :contentReference[oaicite:10]{index=10}
- Estrutura inicial de banco + **CORS** e **middleware de logging**. :contentReference[oaicite:11]{index=11}
- Dependência do serviço **db** no `docker-compose` da API. :contentReference[oaicite:12]{index=12}

