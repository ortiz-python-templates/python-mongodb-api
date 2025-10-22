from loguru import logger
import sys

def setup_logger():
    logger.remove()  # remove default handler
    logger.add(
        sys.stdout,
        format="[ {time:YYYY-MM-DD HH:mm:ss} | {level} | {name} ] {message}",
        level="INFO",
        colorize=True,
        enqueue=True  # thread-safe
    )
    return logger
