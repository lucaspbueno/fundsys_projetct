from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


class IndexadorStats(BaseModel):
    """Estatísticas de um indexador"""
    nome: str
    quantidade: int
    percentual: float


class TopAtivo(BaseModel):
    """Top ativo por valor"""
    codigo: str
    valor: Decimal
    indexador: str


class OverviewResponse(BaseModel):
    """Resposta do overview geral"""
    total_ativos: int
    total_indexadores: int
    valor_total: Decimal
    indexadores: List[IndexadorStats]
    top_ativos: List[TopAtivo]


class IndexadorDetail(BaseModel):
    """Detalhes de um indexador"""
    codigo: str
    sigla: str
    quantidade: int
    percentual: float
    valor_total: Decimal


class IndexadoresResponse(BaseModel):
    """Resposta da listagem de indexadores"""
    indexadores: List[IndexadorDetail]


class AtivoDetail(BaseModel):
    """Detalhes de um ativo"""
    codigo: str
    valor_principal: Decimal
    indexador: str
    data_vencimento: Optional[str] = None


class AtivosResponse(BaseModel):
    """Resposta da listagem de ativos"""
    ativos: List[AtivoDetail]
    total: int
    limit: int
    offset: int


class EvolucaoMensalItem(BaseModel):
    """Item da evolução mensal"""
    mes: int
    quantidade: int
    valor_total: Decimal


class EvolucaoMensalResponse(BaseModel):
    """Resposta da evolução mensal"""
    evolucao: List[EvolucaoMensalItem]
