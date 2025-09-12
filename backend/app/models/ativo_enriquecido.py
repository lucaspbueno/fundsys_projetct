from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, Text, Date
from datetime import date
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .ativo import Ativo

class AtivoEnriquecido(BaseModel, TimestampMixin):
    __tablename__ = "tb_ativo_enriquecido"

    id_ativo_enriquecido: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_ativo: Mapped[int] = mapped_column(Integer, ForeignKey("tb_ativo.id_ativo"), nullable=False, unique=True)
    
    # Dados da ANBIMA
    serie: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    emissao: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    devedor: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    securitizadora: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resgate_antecipado: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    agente_fiduciario: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Controle de enriquecimento
    fl_enriquecido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    dt_ultimo_enriquecimento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fl_erro_enriquecimento: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ds_erro_enriquecimento: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    ativo: Mapped["Ativo"] = relationship("Ativo", back_populates="dados_enriquecidos")

