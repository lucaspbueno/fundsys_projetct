from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import date

class EnrichmentStatusResponse(BaseModel):
    total_ativos: int
    enriquecidos: int
    com_erro: int
    sem_enriquecimento: int
    percentual_enriquecidos: float

class EnrichmentResultResponse(BaseModel):
    sucesso: bool
    ativo_id: int
    dados: Optional[Dict[str, Any]] = None
    enriquecido: Optional[bool] = None
    erro: Optional[str] = None
    mensagem: Optional[str] = None

class BulkEnrichmentRequest(BaseModel):
    ativo_ids: List[int]
    background: bool = False

class BulkEnrichmentResponse(BaseModel):
    sucessos: Optional[List[Dict[str, Any]]] = None
    erros: Optional[List[Dict[str, Any]]] = None
    total: int
    enriquecidos: int = 0
    falhas: int = 0
    background: bool = False
    message: Optional[str] = None

class AtivoEnriquecidoResponse(BaseModel):
    ativo_id: int
    serie: Optional[str] = None
    emissao: Optional[str] = None
    devedor: Optional[str] = None
    securitizadora: Optional[str] = None
    resgate_antecipado: Optional[bool] = None
    agente_fiduciario: Optional[str] = None
    fl_enriquecido: bool
    dt_ultimo_enriquecimento: Optional[date] = None
    fl_erro_enriquecimento: bool
    ds_erro_enriquecimento: Optional[str] = None

