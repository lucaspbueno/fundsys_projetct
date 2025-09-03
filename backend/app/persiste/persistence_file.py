from __future__ import annotations
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

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
            indexador = insert_indexador(db, indexador, cache_indexador, commit=False)

            # 2) Lote
            lote = insert_lote(db, lote, commit=False)

            # 3) Ativo (relaciona ao Lote e Indexador já persistidos/flushados)
            ativo.lote = lote
            ativo.indexador = indexador
            ativo = insert_ativo(db, ativo, commit=False)

            # 4) Posicao (relaciona ao Ativo)
            posicao.ativo = ativo
            posicao = insert_posicao(db, posicao, commit=False)

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
        # Relevante deixar a exceção clara aqui para facilitar o handler na rota/service
        raise RuntimeError("Falha ao persistir bundles em transação única.") from e
