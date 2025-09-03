from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Indexador

def insert_indexador(
    db       : Session,
    indexador: Indexador,
    cache    : dict[str, Indexador],
    *,
    commit   : bool = False,
) -> Indexador:
    """
    Insere um Indexador garantindo deduplicação por `cd_indexador`.

    - Usa cache local para evitar consultas/reinserções na mesma chamada.
    - Se já existir no cache, retorna o objeto.
    - Se não existir, adiciona à session e faz `flush()` para obter PK.
    - Se `commit=True`, tenta commitar e faz rollback em caso de erro.
    - Sempre armazena o resultado em cache.
    
    Obs: A transação deve ser controlada preferencialmente fora desta função.
    """

    # Normaliza e valida o código
    cd_indexador = (indexador.cd_indexador or "").strip()
    if not cd_indexador:
        raise ValueError("cd_indexador vazio ou None")

    # Retorna do cache, se já existir
    if cd_indexador in cache:
        obj = cache[cd_indexador]

        return obj

    # Adiciona na session e garante PK com flush
    db.add(indexador)
    db.flush()

    # Commit opcional
    if commit:
        try:
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Erro ao inserir o Indexador: {indexador}") from e

    # Guarda no cache e retorna
    cache[cd_indexador] = indexador

    return indexador
