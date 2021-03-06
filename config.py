TG_TOKEN = "###"
TG_API_URL = "###"


# Логирование
import logging.config


LOGGING = {
    'disable_existing_loggers': True,
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s.%(funcName)s | %(asctime)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING)


def debug_requests(logger):
    def inner2(f,):
        """Декоратор для обработки событий"""
        def inner(*args, **kwargs):
            try:
                logger.info(f"Обращение к функции {f.__name__}")
                return f(*args, **kwargs)
            except Exception:
                logger.exception(f"Ошибка в функции {f.__name__}")
                raise
        return inner
    return inner2
