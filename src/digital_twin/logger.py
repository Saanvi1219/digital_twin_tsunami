from loguru import logger
logger.add("logs/digital_twin.log", rotation="1 MB")
def get_logger():
    return logger
