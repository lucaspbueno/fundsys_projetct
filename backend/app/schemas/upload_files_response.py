from pydantic import BaseModel
from app.DTOs import ParsedBundleDTO


class UploadFilesResponse(BaseModel):
    str_message: str
    qtd_arquivos_processados: int
    data: list[ParsedBundleDTO]
