from typing import Optional
from decimal import Decimal, InvalidOperation

def str_to_decimal(value: str | None) -> Decimal | None:
    """Converte string para Decimal, aceitando vírgula como separador.
    Retorna None para vazio/None/inválido.
    """

    if value is None:
        return None

    v = value.strip()

    if not v:
        return None

    # normalização simples: "1.234,56" -> "1234.56" ; "123,45" -> "123.45"
    if "," in v:
        v = v.replace(".", "").replace(",", ".")

    try:
        return Decimal(v)
    except (InvalidOperation, ValueError):
        return None
