from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class LoteDTO(BaseModel):
    vl_pu_compra: Decimal | None
    qtd_comprada: Decimal | None
    dt_operacao : date    | None
