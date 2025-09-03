from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Ativo

def insert_ativo(
    db     : Session,
    ativo  : Ativo,
    *,
    commit : bool = False,
) -> Ativo:
    """
    Insere um novo `Ativo`.

    - Adiciona o objeto à sessão e usa `flush()` para garantir a geração da PK.
    - Se `commit=True`, tenta realizar o commit e faz rollback em caso de erro.
    - Retorna o objeto `Ativo` já persistido (mas não necessariamente commitado).
    
    Obs: O controle de transação deve ser feito preferencialmente fora desta função.
    """

    # Adiciona na sessão e garante PK com flush
    db.add(ativo)
    db.flush()

    # Commit opcional
    if commit:
        try:
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Erro ao inserir Ativo: {ativo}") from e

    return ativo
