# log.py
import logging

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
	logger = logging.getLogger(name)
	if not logger.hasHandlers():
		logger.setLevel(level)
		handler = logging.StreamHandler()
		formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
	return logger
