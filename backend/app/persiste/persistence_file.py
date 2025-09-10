from __future__ import annotations
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback

from app.DTOs import ParsedBundleDTO
from app.models import Indexador, Lote, Ativo, Posicao

# funções que acessam o banco
from app.persiste.util import (
    insert_indexador,
    insert_lote,
    insert_ativo,
    insert_posicao,
)

def persist_bundles(
    db: Session,
    bundles: List[ParsedBundleDTO],
) -> List[ParsedBundleDTO]:
    """
    Persiste todos os bundles em uma única transação.

    - Deduplica Indexador via cache local + insert_indexador.
    - Insere Lote, Ativo e Posicao (nessa ordem).
    - Reaponta ativo.indexador para a instância deduplicada.
    - Commit único; rollback em erro.
    """
    cache_indexador: Dict[str, Indexador] = {}

    try:
        # Não comitamos nas funções individuais; comitamos tudo no final
        for bundle in bundles:
            ativo     = bundle.ativo
            lote      = bundle.lote
            indexador = bundle.indexador
            posicao   = bundle.posicao

            # 1) Indexador (dedup por cache local da execução)
            # Converter DTO para modelo
            indexador_model = Indexador(
                cd_indexador=indexador.cd_indexador,
                sgl_indexador=indexador.sgl_indexador
            )
            indexador = insert_indexador(db, indexador_model, cache_indexador, commit=False)

            # 2) Lote - Converter DTO para modelo
            lote_model = Lote(
                vl_pu_compra=lote.vl_pu_compra,
                qtd_comprada=lote.qtd_comprada,
                dt_operacao=lote.dt_operacao
            )
            lote = insert_lote(db, lote_model, commit=False)

            # 3) Ativo (relaciona ao Lote e Indexador já persistidos/flushados)
            ativo_model = Ativo(
                cd_ativo=ativo.cd_ativo,
                cd_isin=ativo.cd_isin,
                vl_pu_emissao=ativo.vl_pu_emissao,
                perc_indexador=ativo.perc_indexador,
                perc_cupom=ativo.perc_cupom,
                dt_emissao=ativo.dt_emissao,
                dt_vencimento=ativo.dt_vencimento,
                lote=lote,
                indexador=indexador
            )
            ativo = insert_ativo(db, ativo_model, commit=False)

            # 4) Posicao (relaciona ao Ativo)
            posicao_model = Posicao(
                vl_pu_posicao=posicao.vl_pu_posicao,
                vl_principal=posicao.vl_principal,
                vl_financeiro_disponivel=posicao.vl_financeiro_disponivel,
                dt_posicao=posicao.dt_posicao,
                ativo=ativo
            )
            posicao = insert_posicao(db, posicao_model, commit=False)

            # Atualiza o bundle com as instâncias “vivas” (com PKs)
            bundle.lote      = lote
            bundle.indexador = indexador
            bundle.ativo     = ativo
            bundle.posicao   = posicao

        # Commit único (tudo-ou-nada)
        db.commit()
        return bundles

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro SQLAlchemy: {e}")
        print(f"Stack trace: {traceback.format_exc()}")
        # Relevante deixar a exceção clara aqui para facilitar o handler na rota/service
        raise RuntimeError("Falha ao persistir bundles em transação única.") from e
    except Exception as e:
        db.rollback()
        print(f"Erro inesperado na persistência: {e}")
        print(f"Stack trace: {traceback.format_exc()}")
        raise RuntimeError("Falha inesperada ao persistir bundles.") from e
