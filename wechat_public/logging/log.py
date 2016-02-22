import logging
import logging.config
import logging.handlers
import os
logger = None

if not logger:
    path = os.path.join(os.path.dirname(__file__), 'logger.conf')
    logging.config.fileConfig(path)
    logger = logging.getLogger('infolog')

def getlogger(name):
    return logging.getLogger('root')