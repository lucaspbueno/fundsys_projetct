from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, Integer, Numeric  
from decimal import Decimal
from typing import TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .ativo import Ativo

class Lote(BaseModel, TimestampMixin):
    __tablename__ = "tb_lote"

    id_lote     : Mapped[int]     = mapped_column(Integer, primary_key=True)
    vl_pu_compra: Mapped[Decimal] = mapped_column(Numeric(24, 9), nullable=False)
    qtd_comprada: Mapped[Decimal] = mapped_column(Numeric(24, 9), nullable=False)
    dt_operacao : Mapped[date]    = mapped_column(Date, nullable=False)

    ativo       : Mapped["Ativo"] = relationship("Ativo", back_populates="lote")
