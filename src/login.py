import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

def get_logger(nome: str) -> logging.Logger:
    logger = logging.getLogger(nome)
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # Console
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    # Arquivo com data
    fh = logging.FileHandler(f"logs/{datetime.now().strftime('%Y%m%d')}.log")
    fh.setFormatter(fmt)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger