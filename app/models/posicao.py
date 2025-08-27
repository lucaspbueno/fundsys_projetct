from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, Date, ForeignKey
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ativo import Ativo

class Posicao(BaseModel, TimestampMixin):
    __tablename__ = "tb_posicao"

    id_posicao               : Mapped[int]     = mapped_column(Integer, primary_key=True)
    id_ativo                 : Mapped[int]     = mapped_column(Integer, ForeignKey("tb_ativo.id_ativo"), nullable=False)
    vl_pu_posicao            : Mapped[Decimal] = mapped_column(Numeric(24, 9), nullable=False)
    vl_principal             : Mapped[Decimal] = mapped_column(Numeric(24, 9), nullable=False)
    vl_financeiro_disponivel : Mapped[Decimal] = mapped_column(Numeric(24, 9), nullable=False)
    dt_posicao               : Mapped[date]    = mapped_column(Date, nullable=False)

    ativo                    : Mapped["Ativo"] = relationship("Ativo", back_populates="posicoes")
