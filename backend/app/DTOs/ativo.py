from pydantic import BaseModel

class AtivoDTO(BaseModel):
    cd_ativo     : str | None
    cd_isin      : str | None
    nm_ativo     : str | None
    tp_ativo     : str | None
    vl_pu_emissao: str | None
    dt_emissao   : str | None
    dt_vencimento: str | None
