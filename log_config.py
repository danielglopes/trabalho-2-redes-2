# log_config.py
import logging
import logging.config
import sys
from pathlib import Path

# Configuração base (os valores de handlers serão ajustados dinamicamente)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            # 'filename' será preenchido por setup_logging()
            "formatter": "default",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


def setup_logging():
    """
    Deve ser chamado antes de qualquer import que use logging.
    Ele irá:
      1. Determinar o nome do script que está rodando (sys.argv[0])
      2. Criar logs/<nome_do_pacote>/<nome_do_script>.log
      3. Ajustar o handler 'file' para usar esse caminho
      4. Aplicar dictConfig()
    """
    # 1) Qual script estamos executando?
    script_path = Path(sys.argv[0]).resolve()
    script_dirname = script_path.parent.name  # ex: 'servidor-horas'
    script_basename = script_path.stem  # ex: 'server'

    # 2) Monta o diretório logs/servidor-horas
    logs_base = Path.cwd() / "logs" / script_dirname
    logs_base.mkdir(parents=True, exist_ok=True)

    # 3) Define o arquivo de log
    log_file = logs_base / f"{script_basename}.log"

    # 4) Ajusta a configuração
    LOGGING["handlers"]["file"]["filename"] = str(log_file)

    # 5) Configura tudo
    logging.config.dictConfig(LOGGING)
