from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.config import get_db
from app.services.analytics import (
    get_overview_service, 
    get_indexadores_service, 
    get_ativos_service, 
    get_evolucao_mensal_service
)
from app.schemas.analytics import (
    OverviewResponse, 
    IndexadoresResponse, 
    AtivosResponse, 
    EvolucaoMensalResponse
)
from typing import Optional
import logging

logger = logging.getLogger(__name__)

analytics_routes = APIRouter(prefix="/analytics", tags=["Analytics"])

@analytics_routes.get("/overview", response_model=OverviewResponse)
async def get_overview(db: Session = Depends(get_db)):
    """Retorna visão geral dos dados do fundo"""
    try:
        return get_overview_service(db)
    except Exception as e:
        logger.error(f"Erro ao buscar overview: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@analytics_routes.get("/ativos", response_model=AtivosResponse)
async def get_ativos(
    db: Session = Depends(get_db),
    indexador: Optional[str] = Query(None, description="Filtrar por indexador"),
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação")
):
    """Retorna lista de ativos com filtros"""
    try:
        return get_ativos_service(db, indexador, limit, offset)
    except Exception as e:
        logger.error(f"Erro ao buscar ativos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@analytics_routes.get("/indexadores", response_model=IndexadoresResponse)
async def get_indexadores(db: Session = Depends(get_db)):
    """Retorna estatísticas dos indexadores"""
    try:
        return get_indexadores_service(db)
    except Exception as e:
        logger.error(f"Erro ao buscar indexadores: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@analytics_routes.get("/evolucao-mensal", response_model=EvolucaoMensalResponse)
async def get_evolucao_mensal(
    db: Session = Depends(get_db),
    ano: Optional[int] = Query(None, description="Ano para filtrar")
):
    """Retorna evolução mensal dos ativos"""
    try:
        return get_evolucao_mensal_service(db, ano)
    except Exception as e:
        logger.error(f"Erro ao buscar evolução mensal: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")