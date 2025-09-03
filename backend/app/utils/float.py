def str_to_float(value: str | None) -> float | None:
    """
    Converte string/numérico em float.
    - Retorna None se o valor for None, vazio ou inválido.
    - Aceita string com vírgula ou ponto decimal.
    """

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        v = value.strip()

        if not v:
            return None

        try:
            return float(v.replace(".", "").replace(",", "."))  # caso venha "1.591,75" -> "1591.75"
        except ValueError:
            return None

    return None
