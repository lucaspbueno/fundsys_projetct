from sqlalchemy.orm import Session
from app.persiste.queries.analytics import (
    get_overview_data, 
    get_indexadores_data, 
    get_ativos_data, 
    get_evolucao_mensal_data
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


def get_overview_service(db: Session, fundo_id: Optional[int] = None, enriched: bool = False) -> OverviewResponse:
    """Service para buscar overview geral"""
    try:
        if fundo_id:
            from app.persiste.queries.fundo_analytics import get_fundo_analytics_data
            data = get_fundo_analytics_data(db, fundo_id, enriched)
        else:
            data = get_overview_data(db, enriched)
        return OverviewResponse(**data)
    except Exception as e:
        logger.error(f"Erro no service de overview: {e}")
        raise


def get_indexadores_service(db: Session) -> IndexadoresResponse:
    """Service para buscar dados dos indexadores"""
    try:
        data = get_indexadores_data(db)
        return IndexadoresResponse(**data)
    except Exception as e:
        logger.error(f"Erro no service de indexadores: {e}")
        raise


def get_ativos_service(
    db: Session, 
    fundo_id: Optional[int] = None,
    indexador: Optional[str] = None, 
    limit: int = 50, 
    offset: int = 0,
    enriched: bool = False
) -> AtivosResponse:
    """Service para buscar dados dos ativos"""
    try:
        if fundo_id:
            from app.persiste.queries.fundo_analytics import get_fundo_ativos_data
            data = get_fundo_ativos_data(db, fundo_id, indexador, limit, offset, enriched)
        else:
            data = get_ativos_data(db, indexador, limit, offset, enriched)
        return AtivosResponse(**data)
    except Exception as e:
        logger.error(f"Erro no service de ativos: {e}")
        raise


def get_evolucao_mensal_service(
    db: Session, 
    ano: Optional[int] = None
) -> EvolucaoMensalResponse:
    """Service para buscar evolução mensal"""
    try:
        data = get_evolucao_mensal_data(db, ano)
        return EvolucaoMensalResponse(**data)
    except Exception as e:
        logger.error(f"Erro no service de evolução mensal: {e}")
        raise
