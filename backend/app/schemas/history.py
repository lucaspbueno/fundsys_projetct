from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class FileHistoryItem(BaseModel):
    """Item do histórico de arquivos"""
    id_lote: int
    nome_arquivo: str
    data_envio: datetime
    quantidade_ativos: int
    valor_total: Decimal
    indexadores: List[str]
    status: str


class FileHistoryResponse(BaseModel):
    """Resposta da listagem de histórico de arquivos"""
    files: List[FileHistoryItem]
    total: int
    limit: int
    offset: int


class FileDetailsResponse(BaseModel):
    """Detalhes de um arquivo específico"""
    lote: dict
    estatisticas: dict
    ativos: List[dict]


class FileAnalyticsResponse(BaseModel):
    """Analytics de um arquivo específico"""
    lote_id: int
    nome_arquivo: str
    data_envio: datetime
    total_ativos: int
    total_indexadores: int
    valor_total: Decimal
    indexadores: List[dict]
    top_ativos: List[dict]
