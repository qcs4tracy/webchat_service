import logging
import logging.config
import logging.handlers

logger = None

if not logger:
    logging.config.fileConfig('logger.conf')
    logger = logging.getLogger('infolog')