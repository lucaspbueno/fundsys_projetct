from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.config import get_db
from app.services.history import get_file_history_service, get_file_details_service, get_file_analytics_service
from app.schemas.history import FileHistoryResponse, FileDetailsResponse, FileAnalyticsResponse
from typing import Optional
import logging

logger = logging.getLogger(__name__)

history_routes = APIRouter(prefix="/history", tags=["History"])

@history_routes.get("/files", response_model=FileHistoryResponse)
async def get_file_history(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Retorna histórico de arquivos enviados"""
    try:
        return get_file_history_service(db, limit, offset)
    except Exception as e:
        logger.error(f"Erro ao buscar histórico de arquivos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao buscar histórico")

@history_routes.get("/files/{lote_id}", response_model=FileDetailsResponse)
async def get_file_details(
    lote_id: int,
    db: Session = Depends(get_db)
):
    """Retorna detalhes de um arquivo específico"""
    try:
        result = get_file_details_service(db, lote_id)
        if not result:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar detalhes do arquivo {lote_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao buscar detalhes do arquivo")

@history_routes.get("/files/{lote_id}/analytics", response_model=FileAnalyticsResponse)
async def get_file_analytics(
    lote_id: int,
    db: Session = Depends(get_db)
):
    """Retorna analytics de um arquivo específico"""
    try:
        result = get_file_analytics_service(db, lote_id)
        if not result:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar analytics do arquivo {lote_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao buscar analytics do arquivo")
