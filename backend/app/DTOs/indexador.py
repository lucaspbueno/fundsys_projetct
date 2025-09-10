from pydantic import BaseModel

class IndexadorDTO(BaseModel):
    cd_indexador : str | None
    sgl_indexador: str | None
