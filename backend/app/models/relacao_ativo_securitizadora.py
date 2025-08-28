from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, text, Boolean
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ativo import Ativo
    from .securitizadora import Securitizadora

class RelacaoAtivoSecuritizadora(BaseModel, TimestampMixin):
    __tablename__ = "tb_relacao_ativo_securitizadora"

    id_relacao_ativo_securitizadora: Mapped[int]  = mapped_column(Integer, primary_key=True)
    id_ativo                       : Mapped[int]  = mapped_column(Integer, ForeignKey("tb_ativo.id_ativo"), nullable=False)
    id_securitizadora              : Mapped[int]  = mapped_column(Integer, ForeignKey("tb_securitizadora.id_securitizadora"), nullable=False)
    fl_relacao_ativa               : Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    ativo         : Mapped["Ativo"]          = relationship("Ativo", back_populates="relacoes_securitizadoras")
    securitizadora: Mapped["Securitizadora"] = relationship("Securitizadora", back_populates="relacoes_ativos")