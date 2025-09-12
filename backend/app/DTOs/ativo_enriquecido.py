from pydantic import BaseModel
from typing import Optional
from datetime import date

class AtivoEnriquecidoDTO(BaseModel):
    id_ativo_enriquecido: Optional[int] = None
    id_ativo: int
    serie: Optional[str] = None
    emissao: Optional[str] = None
    devedor: Optional[str] = None
    securitizadora: Optional[str] = None
    resgate_antecipado: Optional[bool] = None
    agente_fiduciario: Optional[str] = None
    fl_enriquecido: bool = True
    dt_ultimo_enriquecimento: Optional[date] = None
    fl_erro_enriquecimento: bool = False
    ds_erro_enriquecimento: Optional[str] = None

