from .utils import BaseModel, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean
from typing import TYPE_CHECKING, Optional
import hashlib

if TYPE_CHECKING:
    from .fundo_investimento import FundoInvestimento

class ArquivoOriginal(BaseModel, TimestampMixin):
    __tablename__ = "tb_arquivo_original"

    id_arquivo_original: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_fundo_investimento: Mapped[int] = mapped_column(Integer, ForeignKey("tb_fundo_investimento.id_fundo_investimento"), nullable=False)
    
    # Dados do arquivo
    nm_arquivo: Mapped[str] = mapped_column(String(255), nullable=False)
    nm_arquivo_original: Mapped[str] = mapped_column(String(255), nullable=False)
    conteudo_arquivo: Mapped[str] = mapped_column(Text, nullable=False)
    hash_arquivo: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    tamanho_arquivo: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Controle
    fl_processado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    fl_erro_processamento: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ds_erro_processamento: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    fundo_investimento: Mapped["FundoInvestimento"] = relationship("FundoInvestimento", back_populates="arquivos_originais")
    
    @classmethod
    def calcular_hash(cls, conteudo: str) -> str:
        """Calcula o hash SHA-256 do conteúdo do arquivo"""
        return hashlib.sha256(conteudo.encode('utf-8')).hexdigest()

