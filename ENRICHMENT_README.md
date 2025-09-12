# Sistema de Enriquecimento de Dados ANBIMA

Este documento explica como funciona o sistema de enriquecimento de dados implementado para capturar informações adicionais dos ativos via API da ANBIMA.

## Funcionalidades Implementadas

### 1. Modelo de Banco de Dados
- **Tabela**: `tb_ativo_enriquecido`
- **Campos enriquecidos**:
  - `serie`: Série do ativo
  - `emissao`: Emissão do ativo
  - `devedor`: Nome do devedor
  - `securitizadora`: Nome da securitizadora
  - `resgate_antecipado`: Se permite resgate antecipado (boolean)
  - `agente_fiduciario`: Nome do agente fiduciário
  - `fl_enriquecido`: Flag indicando se foi enriquecido com sucesso
  - `dt_ultimo_enriquecimento`: Data do último enriquecimento
  - `fl_erro_enriquecimento`: Flag indicando erro no enriquecimento
  - `ds_erro_enriquecimento`: Descrição do erro

### 2. Serviços de Enriquecimento

#### AnbimaEnrichmentService
- Captura dados da API da ANBIMA via web scraping
- URL base: `https://data.anbima.com.br/certificado-de-recebiveis/{cod_ativo}/caracteristicas`
- Suporte a múltiplos ativos com delay entre requisições
- Tratamento de erros e retry automático

#### EnrichmentService
- Serviço principal de enriquecimento
- Enriquecimento individual ou em lote
- Enriquecimento de ativos pendentes
- Status de enriquecimento

### 3. Rotas da API

#### GET `/enrichment/status`
Retorna estatísticas do enriquecimento:
```json
{
  "total_ativos": 100,
  "enriquecidos": 80,
  "com_erro": 5,
  "sem_enriquecimento": 15,
  "percentual_enriquecidos": 80.0
}
```

#### POST `/enrichment/enrich/{ativo_id}`
Enriquece um único ativo.

#### POST `/enrichment/enrich/bulk`
Enriquece múltiplos ativos:
```json
{
  "ativo_ids": [1, 2, 3],
  "background": false
}
```

#### POST `/enrichment/enrich/pending`
Enriquece ativos pendentes:
```
?limit=50&background=false
```

#### GET `/enrichment/ativos/{ativo_id}/enriched`
Retorna dados enriquecidos de um ativo específico.

### 4. Analytics com Dados Enriquecidos

#### GET `/analytics/overview?enriched=true`
Retorna overview com dados enriquecidos quando disponíveis.

#### GET `/analytics/ativos?enriched=true`
Retorna lista de ativos com dados enriquecidos.

### 5. Frontend

#### Toggle de Dados Enriquecidos
- Botão para alternar entre dados normais e enriquecidos
- Exibição de dados adicionais quando em modo enriquecido
- Botão para enriquecer ativos pendentes

#### Exibição de Dados Enriquecidos
- Série e Emissão
- Devedor
- Securitizadora
- Resgate Antecipado
- Agente Fiduciário

## Como Usar

### 1. Executar Migração
```bash
cd backend
poetry run alembic upgrade head
```

### 2. Instalar Dependências
```bash
cd backend
poetry install
```

### 3. Enriquecer Dados
- **Automático**: O enriquecimento acontece automaticamente após o upload de arquivos
- **Manual**: Use as rotas da API ou o botão no frontend
- **Em lote**: Use `/enrichment/enrich/pending` para enriquecer ativos pendentes

### 4. Visualizar Dados Enriquecidos
- Acesse a página de Insights
- Clique no botão "Dados Enriquecidos" para alternar o modo
- Os dados enriquecidos aparecerão em verde abaixo dos dados normais

## Configurações

### Delay entre Requisições
O sistema usa um delay de 1 segundo entre requisições para não sobrecarregar o servidor da ANBIMA.

### Timeout
Timeout de 30 segundos para cada requisição.

### User-Agent
O sistema usa um User-Agent de navegador para evitar bloqueios.

## Tratamento de Erros

- Erros de rede são capturados e logados
- Ativos com erro são marcados com `fl_erro_enriquecimento = true`
- Descrição do erro é salva em `ds_erro_enriquecimento`
- O sistema continua funcionando mesmo com falhas no enriquecimento

## Monitoramento

- Logs detalhados de todas as operações
- Status de enriquecimento disponível via API
- Contadores de sucessos e falhas
- Data do último enriquecimento

## Limitações

- Depende da disponibilidade da API da ANBIMA
- Estrutura da página pode mudar (requer atualização do parser)
- Rate limiting do servidor da ANBIMA
- Alguns ativos podem não ter dados disponíveis na ANBIMA

