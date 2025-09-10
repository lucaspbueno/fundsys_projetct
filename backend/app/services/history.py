from sqlalchemy.orm import Session
from app.persiste.queries.history import get_file_history, get_file_details, get_file_analytics
from app.schemas.history import FileHistoryResponse, FileDetailsResponse, FileAnalyticsResponse
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_file_history_service(
    db: Session, 
    limit: int = 10, 
    offset: int = 0
) -> FileHistoryResponse:
    """Service para buscar histórico de arquivos"""
    try:
        data = get_file_history(db, limit, offset)
        return FileHistoryResponse(**data)
    except Exception as e:
        logger.error(f"Erro no service de histórico: {e}")
        raise


def get_file_details_service(
    db: Session, 
    lote_id: int
) -> Optional[FileDetailsResponse]:
    """Service para buscar detalhes de um arquivo"""
    try:
        data = get_file_details(db, lote_id)
        if not data:
            return None
        return FileDetailsResponse(**data)
    except Exception as e:
        logger.error(f"Erro no service de detalhes do arquivo {lote_id}: {e}")
        raise


def get_file_analytics_service(
    db: Session, 
    lote_id: int
) -> Optional[FileAnalyticsResponse]:
    """Service para buscar analytics de um arquivo"""
    try:
        data = get_file_analytics(db, lote_id)
        if not data:
            return None
        return FileAnalyticsResponse(**data)
    except Exception as e:
        logger.error(f"Erro no service de analytics do arquivo {lote_id}: {e}")
        raise
