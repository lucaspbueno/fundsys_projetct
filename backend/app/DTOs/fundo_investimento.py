from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FundoInvestimentoDTO(BaseModel):
    id_fundo_investimento: Optional[int] = None
    nm_fundo_investimento: str
    ds_fundo_investimento: str
    id_orgao_financeiro: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ArquivoOriginalDTO(BaseModel):
    id_arquivo_original: Optional[int] = None
    id_fundo_investimento: int
    nm_arquivo: str
    nm_arquivo_original: str
    conteudo_arquivo: str
    hash_arquivo: str
    tamanho_arquivo: int
    fl_processado: bool = False
    fl_erro_processamento: bool = False
    ds_erro_processamento: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class FundoComArquivoDTO(BaseModel):
    fundo: FundoInvestimentoDTO
    arquivo: ArquivoOriginalDTO

