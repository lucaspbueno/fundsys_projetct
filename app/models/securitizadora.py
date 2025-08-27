from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, text
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .relacao_ativo_securitizadora import RelacaoAtivoSecuritizadora


class Securitizadora(BaseModel, TimestampMixin):
    __tablename__ = "tb_securitizadora"

    id_securitizadora: Mapped[int]  = mapped_column(Integer, primary_key=True)
    nr_cnpj          : Mapped[str]  = mapped_column(String(14), unique=True, nullable=False)
    nm_razao_social  : Mapped[str]  = mapped_column(String(150), unique=True, nullable=False)
    nm_fantasia      : Mapped[str]  = mapped_column(String(150), nullable=False)
    fl_ativa         : Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    relacoes_ativos: Mapped[list["RelacaoAtivoSecuritizadora"]] = relationship("RelacaoAtivoSecuritizadora", back_populates="securitizadora")
