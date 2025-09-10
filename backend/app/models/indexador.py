from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .ativo import Ativo

class Indexador(BaseModel, TimestampMixin):
    __tablename__ = "tb_indexador"

    id_indexador : Mapped[int]           = mapped_column(Integer, primary_key=True)
    cd_indexador : Mapped[str]           = mapped_column(String(100), nullable=False)
    sgl_indexador: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    ativos: Mapped[list["Ativo"]] = relationship("Ativo", back_populates="indexador")
