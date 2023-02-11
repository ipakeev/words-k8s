import logging

logger = logging.Logger("bot", level=logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s (%(funcName)s) | %(message)s"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
