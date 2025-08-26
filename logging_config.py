import logging


class LogFormatter(logging.Formatter):
    """
    Formatter personalizado para adicionar cores ANSI aos logs com base no nível de severidade.

    Cores aplicadas:
        - DEBUG: Azul
        - INFO: Verde
        - WARNING: Amarelo
        - ERROR: Vermelho
        - CRITICAL: Magenta

    Isso facilita a visualização dos logs no terminal, destacando cada nível com uma cor diferente.

    Attributes:
        COLORS (dict): Mapeamento entre níveis de log e códigos de cor ANSI.
        RESET (str): Código ANSI para resetar a cor após o log.
    """
    COLORS = {
        logging.DEBUG: "\033[94m",     # Azul
        logging.INFO: "\033[92m",      # Verde
        logging.WARNING: "\033[93m",   # Amarelo
        logging.ERROR: "\033[91m",     # Vermelho
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        """
        Aplica a cor ao log formatado com base no nível de log.

        Args:
            record (LogRecord): Registro de log.

        Returns:
            str: Mensagem formatada com cor.
        """
        log_color = self.COLORS.get(record.levelno, self.RESET)
        formatted = super().format(record)
        return f"{log_color}{formatted}{self.RESET}"


def setup_logger(name: str = "app") -> logging.Logger:
    """
    Configura e retorna um logger.

    Args:
        name (str): Nome do logger.

    Returns:
        logging.Logger: Instância configurada do logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = LogFormatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


logger = setup_logger("app")
