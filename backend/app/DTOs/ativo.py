from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class AtivoDTO(BaseModel):
    cd_ativo      : str     | None
    cd_isin       : str     | None
    perc_indexador: float   | None
    perc_cupom    : float   | None
    vl_pu_emissao : Decimal | None
    dt_emissao    : date    | None
    dt_vencimento : date    | None
