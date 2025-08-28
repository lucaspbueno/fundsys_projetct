from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .ativo import Ativo

class FundoInvestimento(BaseModel, TimestampMixin):
    __tablename__ = "tb_fundo_investimento"

    id_fundo_investimento: Mapped[int]           = mapped_column(Integer, primary_key=True)
    id_orgao_financeiro  : Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tb_orgao_financeiro.id_orgao_financeiro"), nullable=True)
    nm_fundo_investimento: Mapped[str]           = mapped_column(String(100), nullable=False)
    ds_fundo_investimento: Mapped[str]           = mapped_column(String(200), nullable=False)

    ativos: Mapped[list["Ativo"]] = relationship("Ativo", back_populates="fundo")
