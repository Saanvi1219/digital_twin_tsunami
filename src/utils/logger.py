"""
==================================================
Logger Utility

Digital Twin Tsunami Prediction System
==================================================
"""

from pathlib import Path
from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    LOG_DIR / "project.log",
    rotation="5 MB",
    level="INFO",
    enqueue=True
)

logger.add(
    lambda msg: print(msg, end=""),
    colorize=True,
    level="INFO"
)


def get_logger():
    """
    Returns configured logger instance.
    """
    return logger