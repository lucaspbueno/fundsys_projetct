from __future__ import annotations
from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import Any, Dict, List
from app.DTOs import ParsedBundleDTO, AtivoDTO, IndexadorDTO, LoteDTO, PosicaoDTO
from app.utils import FileLoader, Parser, convert_to_list, str_to_datetime_utc, str_to_decimal, str_to_float


async def upload_files_service(
    ls_files: List[UploadFile],
    db      : Session,
    loader  : FileLoader,
    parser  : Parser,
) -> List[ParsedBundleDTO]:
    """
    Lê cada arquivo, parseia o XML e retorna uma lista de ParsedBundleDTO,
    contendo (Lote, Indexador, Ativo, Posicao) já ligados entre si.

    Não faz persistência nem validação de unicidade/deduplicação.
    """
    bundles: List[ParsedBundleDTO] = []

    for file in ls_files:
        text   = await loader.load_text(file)
        doc: Dict[str, Any] = parser.parse_xml_text_to_dict(text) or {}
        root   = doc.get("arquivoposicao_4_01", {})
        fundos = convert_to_list(root.get("fundo"))

        for a in fundos:
            # --- construir entidades individuais ---
            lote = LoteDTO(
                vl_pu_compra = str_to_decimal(a.get("pucompra")),
                qtd_comprada = str_to_decimal(a.get("qtdisponivel")),
                dt_operacao  = str_to_datetime_utc(a.get("dtoperacao")),
            )

            indexador = IndexadorDTO(
                cd_indexador  = a.get("indexador"),
                sgl_indexador = a.get("sgl_indexador"),
            )

            ativo = AtivoDTO(
                cd_ativo       = a.get("codativo"),
                cd_isin        = a.get("isin"),
                vl_pu_emissao  = str_to_decimal(a.get("puemissao")),
                perc_indexador = str_to_float(a.get("percindex")),
                perc_cupom     = str_to_float(a.get("perccupom")),
                dt_emissao     = str_to_datetime_utc(a.get("dtemissao")),
                dt_vencimento  = str_to_datetime_utc(a.get("dtvencimento")),
            )

            posicao = PosicaoDTO(
                vl_pu_posicao            = str_to_decimal(a.get("puposicao")),
                vl_principal             = str_to_decimal(a.get("principal")),
                vl_financeiro_disponivel = str_to_decimal(a.get("valorfindisp")),
                dt_posicao               = str_to_datetime_utc(a.get("dtoperacao")),
            )

            bundles.append(
                ParsedBundleDTO(
                    lote      = lote,
                    indexador = indexador,
                    ativo     = ativo,
                    posicao   = posicao,
                )
            )

    return bundles
