LOGGING_APPLICATION_CONF = {
    'version': 1,  # required
    'disable_existing_loggers': True,  # this config overrides all other loggers
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s -- %(message)s'
        },
        'sysout': {
            'format': '%(asctime)s\t%(levelname)s -- %(filename)s:%(lineno)s -- %(message)s',

        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sysout'
        }
    },
    'loggers': {
        'app': {  # 'root' logge
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}