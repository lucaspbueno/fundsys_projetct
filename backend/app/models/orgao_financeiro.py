from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, text
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .fundo_investimento import FundoInvestimento

class OrgaoFinanceiro(BaseModel, TimestampMixin):
    __tablename__ = "tb_orgao_financeiro"

    id_orgao_financeiro: Mapped[int]  = mapped_column(Integer, primary_key=True)
    nr_cnpj            : Mapped[str]  = mapped_column(String(14), nullable=False)
    nm_razao_social    : Mapped[str]  = mapped_column(String(150), nullable=False)
    nm_fantasia        : Mapped[str]  = mapped_column(String(150), nullable=False)
    fl_ativo           : Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    fundos: Mapped[Optional[list["FundoInvestimento"]]] = relationship("FundoInvestimento", back_populates="orgao_financeiro")
