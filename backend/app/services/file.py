from __future__ import annotations
from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import Any, Dict, List
from app.DTOs import ParsedBundleDTO, AtivoDTO, IndexadorDTO, LoteDTO, PosicaoDTO
from app.utils import FileLoader, Parser, convert_to_list, str_to_datetime_utc, str_to_decimal, str_to_float
from app.persiste import persist_bundles


async def upload_files_service(
    ls_files: List[UploadFile],
    db      : Session,
    loader  : FileLoader,
    parser  : Parser,
    fundo_id: int = None,
) -> List[ParsedBundleDTO]:
    """
    Lê cada arquivo, parseia o XML e retorna uma lista de ParsedBundleDTO,
    contendo (Lote, Indexador, Ativo, Posicao) já ligados entre si.

    Não faz persistência nem validação de unicidade/deduplicação.
    """
    bundles: List[ParsedBundleDTO] = []

    for file in ls_files:
        text = await loader.load_text(file)
        doc: Dict[str, Any] = parser.parse_xml_text_to_dict(text) or {}
        root = doc.get("arquivoposicao_4_01", {})
        fundos = convert_to_list(root.get("fundo"))

        for fundo in fundos:
            titprivado_list = convert_to_list(fundo.get("titprivado", []))
            
            for titprivado in titprivado_list:
                # --- construir entidades individuais ---
                lote = LoteDTO(
                    vl_pu_compra = str_to_decimal(titprivado.get("pucompra")),
                    qtd_comprada = str_to_decimal(titprivado.get("qtdisponivel")),
                    dt_operacao  = str_to_datetime_utc(titprivado.get("dtoperacao")),
                )

                indexador = IndexadorDTO(
                    cd_indexador  = titprivado.get("indexador"),
                    sgl_indexador = titprivado.get("sgl_indexador", ""),
                )

                ativo = AtivoDTO(
                    cd_ativo       = titprivado.get("codativo"),
                    cd_isin        = titprivado.get("isin"),
                    vl_pu_emissao  = str_to_decimal(titprivado.get("puemissao")),
                    perc_indexador = str_to_float(titprivado.get("percindex")),
                    perc_cupom     = str_to_float(titprivado.get("coupom")),
                    dt_emissao     = str_to_datetime_utc(titprivado.get("dtemissao")),
                    dt_vencimento  = str_to_datetime_utc(titprivado.get("dtvencimento")),
                )

                posicao = PosicaoDTO(
                    vl_pu_posicao            = str_to_decimal(titprivado.get("puposicao")),
                    vl_principal             = str_to_decimal(titprivado.get("principal")),
                    vl_financeiro_disponivel = str_to_decimal(titprivado.get("valorfindisp")),
                    dt_posicao               = str_to_datetime_utc(titprivado.get("dtoperacao")),
                )

                bundles.append(
                    ParsedBundleDTO(
                        lote      = lote,
                        indexador = indexador,
                        ativo     = ativo,
                        posicao   = posicao,
                    )
                )

    return persist_bundles(db, bundles, fundo_id)
