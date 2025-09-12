from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FundoInvestimentoResponse(BaseModel):
    id_fundo_investimento: int
    nm_fundo_investimento: str
    ds_fundo_investimento: str
    total_ativos: int
    valor_total: float
    data_criacao: datetime
    ultima_atualizacao: Optional[datetime] = None

class FundoDetalhesResponse(BaseModel):
    id_fundo_investimento: int
    nm_fundo_investimento: str
    ds_fundo_investimento: str
    total_ativos: int
    valor_total: float
    total_indexadores: int
    data_criacao: datetime
    ultima_atualizacao: Optional[datetime] = None
    arquivos: List[dict]

class UploadFundoResponse(BaseModel):
    sucesso: bool
    mensagem: str
    fundo_id: Optional[int] = None
    arquivo_duplicado: bool = False
    fundo_existente: Optional[FundoInvestimentoResponse] = None

class FundoListResponse(BaseModel):
    fundos: List[FundoInvestimentoResponse]
    total: int

class ArquivoDuplicadoResponse(BaseModel):
    arquivo_duplicado: bool
    fundo_existente: FundoInvestimentoResponse
    mensagem: str

