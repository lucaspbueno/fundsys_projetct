from __future__ import annotations
from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import Any, Dict, List
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio

from app.DTOs import ParsedBundleDTO, AtivoDTO, IndexadorDTO, LoteDTO, PosicaoDTO
from app.utils import FileLoader, Parser, convert_to_list, str_to_datetime_utc, str_to_decimal, str_to_float
from app.persiste import persist_bundles
from app.services.enrichment_service import EnrichmentService

logger = logging.getLogger(__name__)

async def upload_files_with_enrichment_service(
    ls_files: List[UploadFile],
    db: Session,
    loader: FileLoader,
    parser: Parser,
    enable_enrichment: bool = True
) -> List[ParsedBundleDTO]:
    """
    Lê cada arquivo, parseia o XML, persiste no banco e enriquece os dados via ANBIMA.
    
    Args:
        ls_files: Lista de arquivos para upload
        db: Sessão do banco de dados
        loader: Carregador de arquivos
        parser: Parser de XML
        enable_enrichment: Se deve habilitar o enriquecimento via ANBIMA
        
    Returns:
        Lista de bundles processados
    """
    # Primeiro, processar e persistir os arquivos normalmente
    bundles = await upload_files_service(ls_files, db, loader, parser)
    
    if not enable_enrichment or not bundles:
        return bundles
    
    # Enriquecer os dados via ANBIMA
    try:
        enrichment_service = EnrichmentService()
        
        # Extrair IDs dos ativos recém-criados
        ativo_ids = [bundle.ativo.id_ativo for bundle in bundles if hasattr(bundle.ativo, 'id_ativo')]
        
        if ativo_ids:
            logger.info(f"Iniciando enriquecimento de {len(ativo_ids)} ativos")
            
            # Enriquecer ativos em paralelo (com limite de threads)
            with ThreadPoolExecutor(max_workers=3) as executor:
                # Criar tasks para enriquecimento assíncrono
                loop = asyncio.get_event_loop()
                tasks = []
                
                for ativo_id in ativo_ids:
                    task = loop.run_in_executor(
                        executor, 
                        enrichment_service.enrich_single_ativo, 
                        db, 
                        ativo_id
                    )
                    tasks.append(task)
                
                # Aguardar todos os enriquecimentos
                resultados = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Log dos resultados
                sucessos = sum(1 for r in resultados if isinstance(r, dict) and r.get('sucesso', False))
                erros = len(resultados) - sucessos
                
                logger.info(f"Enriquecimento concluído: {sucessos} sucessos, {erros} erros")
                
                # Log de erros específicos
                for i, resultado in enumerate(resultados):
                    if isinstance(resultado, Exception):
                        logger.error(f"Erro no enriquecimento do ativo {ativo_ids[i]}: {resultado}")
                    elif isinstance(resultado, dict) and not resultado.get('sucesso', False):
                        logger.warning(f"Falha no enriquecimento do ativo {ativo_ids[i]}: {resultado.get('erro', 'Erro desconhecido')}")
        
    except Exception as e:
        logger.error(f"Erro durante o enriquecimento: {e}")
        # Não falhar o upload por causa do enriquecimento
    
    return bundles

async def upload_files_service(
    ls_files: List[UploadFile],
    db: Session,
    loader: FileLoader,
    parser: Parser,
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

    return persist_bundles(db, bundles)

