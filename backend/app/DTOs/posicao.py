from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class PosicaoDTO(BaseModel):
    vl_pu_posicao           : Decimal | None
    vl_principal            : Decimal | None
    vl_financeiro_disponivel: Decimal | None
    dt_posicao              : date    | None