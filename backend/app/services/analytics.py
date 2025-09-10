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


def get_overview_service(db: Session) -> OverviewResponse:
    """Service para buscar overview geral"""
    try:
        data = get_overview_data(db)
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
    indexador: Optional[str] = None, 
    limit: int = 50, 
    offset: int = 0
) -> AtivosResponse:
    """Service para buscar dados dos ativos"""
    try:
        data = get_ativos_data(db, indexador, limit, offset)
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
