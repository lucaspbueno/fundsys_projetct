from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.config import get_db
from app.services.enrichment_service import EnrichmentService
from app.schemas.enrichment import (
    EnrichmentStatusResponse,
    EnrichmentResultResponse,
    BulkEnrichmentRequest,
    BulkEnrichmentResponse
)

logger = logging.getLogger(__name__)

enrichment_routes = APIRouter(prefix="/enrichment", tags=["Enrichment"])

@enrichment_routes.get("/status", response_model=EnrichmentStatusResponse)
async def get_enrichment_status(db: Session = Depends(get_db)):
    """Retorna o status atual do enriquecimento dos ativos"""
    try:
        service = EnrichmentService()
        status = service.get_enrichment_status(db)
        
        if 'erro' in status:
            raise HTTPException(status_code=500, detail=status['erro'])
        
        return EnrichmentStatusResponse(**status)
    except Exception as e:
        logger.error(f"Erro ao buscar status de enriquecimento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@enrichment_routes.post("/enrich/{ativo_id}", response_model=EnrichmentResultResponse)
async def enrich_single_ativo(
    ativo_id: int,
    db: Session = Depends(get_db)
):
    """Enriquece um único ativo com dados da ANBIMA"""
    try:
        service = EnrichmentService()
        resultado = service.enrich_single_ativo(db, ativo_id)
        
        if not resultado['sucesso']:
            raise HTTPException(status_code=400, detail=resultado.get('erro', 'Erro desconhecido'))
        
        return EnrichmentResultResponse(**resultado)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao enriquecer ativo {ativo_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@enrichment_routes.post("/enrich/bulk", response_model=BulkEnrichmentResponse)
async def enrich_multiple_ativos(
    request: BulkEnrichmentRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Enriquece múltiplos ativos com dados da ANBIMA"""
    try:
        service = EnrichmentService()
        
        if request.background:
            # Executar em background
            background_tasks.add_task(
                service.enrich_multiple_ativos,
                db,
                request.ativo_ids
            )
            return BulkEnrichmentResponse(
                message="Enriquecimento iniciado em background",
                total=len(request.ativo_ids),
                background=True
            )
        else:
            # Executar sincronamente
            resultado = service.enrich_multiple_ativos(db, request.ativo_ids)
            return BulkEnrichmentResponse(**resultado)
            
    except Exception as e:
        logger.error(f"Erro ao enriquecer múltiplos ativos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@enrichment_routes.post("/enrich/pending", response_model=BulkEnrichmentResponse)
async def enrich_pending_ativos(
    limit: int = Query(50, ge=1, le=200, description="Limite de ativos a processar"),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Enriquece ativos pendentes de enriquecimento"""
    try:
        service = EnrichmentService()
        
        if background_tasks:
            # Executar em background
            background_tasks.add_task(
                service.enrich_pending_ativos,
                db,
                limit
            )
            return BulkEnrichmentResponse(
                message="Enriquecimento de ativos pendentes iniciado em background",
                total=0,
                background=True
            )
        else:
            # Executar sincronamente
            resultado = service.enrich_pending_ativos(db, limit)
            return BulkEnrichmentResponse(**resultado)
            
    except Exception as e:
        logger.error(f"Erro ao enriquecer ativos pendentes: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@enrichment_routes.get("/ativos/{ativo_id}/enriched")
async def get_ativo_enriched_data(
    ativo_id: int,
    db: Session = Depends(get_db)
):
    """Retorna os dados enriquecidos de um ativo específico"""
    try:
        from app.persiste.util.ativo_enriquecido import get_ativo_enriquecido_by_ativo_id
        
        dados_enriquecidos = get_ativo_enriquecido_by_ativo_id(db, ativo_id)
        
        if not dados_enriquecidos:
            raise HTTPException(status_code=404, detail="Dados enriquecidos não encontrados")
        
        return {
            "ativo_id": ativo_id,
            "dados": {
                "serie": dados_enriquecidos.serie,
                "emissao": dados_enriquecidos.emissao,
                "devedor": dados_enriquecidos.devedor,
                "securitizadora": dados_enriquecidos.securitizadora,
                "resgate_antecipado": dados_enriquecidos.resgate_antecipado,
                "agente_fiduciario": dados_enriquecidos.agente_fiduciario,
                "fl_enriquecido": dados_enriquecidos.fl_enriquecido,
                "dt_ultimo_enriquecimento": dados_enriquecidos.dt_ultimo_enriquecimento,
                "fl_erro_enriquecimento": dados_enriquecidos.fl_erro_enriquecimento,
                "ds_erro_enriquecimento": dados_enriquecidos.ds_erro_enriquecimento
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar dados enriquecidos do ativo {ativo_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

