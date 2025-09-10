from pydantic import BaseModel
from app.DTOs import AtivoDTO, IndexadorDTO, LoteDTO, PosicaoDTO


class ParsedBundleDTO(BaseModel):
    """
    Pacote com as entidades DTO, que após serem transformadas em classes ORM seram inseridas no banco de dados em outra camada (persiste).
    """
    ativo    : AtivoDTO
    indexador: IndexadorDTO
    lote     : LoteDTO
    posicao  : PosicaoDTO
