import logging.config
import logging
from fontastic.utils.logging_conf import LOGGING_APPLICATION_CONF


class Logger:
    '''
    This class contains methods to work with Standard logger
    '''

    def get_logger(self):
        '''
        Method to instantiate the logger and returns the logger with the set configuration

        Returns:
            [Logger] -- An instance of logging
        '''

        # Refers to the loggers section in the logging_conf.py
        logging.config.dictConfig(LOGGING_APPLICATION_CONF)
        logger = logging.getLogger('app')
        handler = logging.StreamHandler()
        logger.addHandler(logger.handlers[0])
        return logger
