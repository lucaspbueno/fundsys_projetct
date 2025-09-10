from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Lote

def insert_lote(
    db    : Session,
    lote  : Lote,
    *,
    commit: bool = False,
) -> Lote:
    """
    Insere um novo `Lote`.

    - Adiciona o objeto à sessão e usa `flush()` para garantir a geração da PK.
    - Se `commit=True`, tenta realizar o commit e faz rollback em caso de erro.
    - Retorna o objeto `Lote` já persistido (mas não necessariamente commitado).
    
    Obs: O controle de transação deve ser feito preferencialmente fora desta função.
    """

    # Adiciona na session e garante PK com flush
    db.add(lote)
    db.flush()

    # Commit opcional
    if commit:
        try:
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Erro ao inserir Lote: {lote}") from e

    return lote
