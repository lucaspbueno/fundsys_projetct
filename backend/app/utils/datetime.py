from datetime import datetime, timezone
from typing import Optional


def str_to_datetime_utc(date_str: str | None, input_format: str = "%Y%m%d") -> datetime | None:
    """
    Converte string no formato YYYYMMDD para datetime UTC.

    :param date_str: Data em formato string / Ex: "20280821"
    :param input_format: Formato esperado da string (default: "YYYY-MM-DD HH:MM:SS")
    :return: datetime com tz UTC
    """
    if not date_str:
        return None
    try:

        # Faz o parse da string para datetime (sem tz)
        dt_naive = datetime.strptime(date_str, input_format)

        # Coloca timezone UTC
        return dt_naive.replace(tzinfo=timezone.utc)
    
    except Exception:
        return None
