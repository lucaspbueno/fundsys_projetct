from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Numeric, Date, Boolean, ForeignKey, text
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .fundo_investimento import FundoInvestimento
    from .lote import Lote
    from .posicao import Posicao
    from .indexador import Indexador

class Ativo(BaseModel, TimestampMixin):
    __tablename__ = "tb_ativo"

    id_ativo      : Mapped[int]           = mapped_column(Integer, primary_key=True)
    id_fundo      : Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tb_fundo_investimento.id_fundo_investimento"), nullable=True)
    id_lote       : Mapped[int]           = mapped_column(Integer, ForeignKey("tb_lote.id_lote"), nullable=False)
    id_indexador  : Mapped[int]           = mapped_column(Integer, ForeignKey("tb_indexador.id_indexador"), nullable=False)
    cd_ativo      : Mapped[str]           = mapped_column(String(100), nullable=False)
    cd_isin       : Mapped[str]           = mapped_column(String(100), nullable=False)
    nm_ativo      : Mapped[str]           = mapped_column(String(100), nullable=False)
    tp_ativo      : Mapped[str]           = mapped_column(String(100), nullable=False)
    vl_pu_emisssao: Mapped[Decimal]       = mapped_column(Numeric(24, 9), nullable=False)
    dt_emissao    : Mapped[date]          = mapped_column(Date, nullable=False)
    dt_vencimento : Mapped[date]          = mapped_column(Date, nullable=False)
    fl_ativo      : Mapped[bool]          = mapped_column(Boolean, nullable=False, server_default=text("true"))

    fundo         : Mapped[Optional["FundoInvestimento"]] = relationship("FundoInvestimento", back_populates="ativos")
    lote          : Mapped["Lote"]            = relationship("Lote", back_populates="ativos")
    posicoes      : Mapped[list["Posicao"]]   = relationship("Posicao", back_populates="ativo")
    indexador     : Mapped["Indexador"]       = relationship("Indexador", back_populates="ativos")
