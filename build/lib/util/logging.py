import logging
import click


def init_logging(log_level='DEBUG'):
    level = None
    log_level = log_level.upper()
    match log_level:
        case 'CRITICAL':
            level = logging.CRITICAL
        case 'ERROR':
            level = logging.ERROR
        case 'WARNING':
            level = logging.WARNING
        case 'INFO':
            level = logging.INFO
        case 'DEBUG':
            level = logging.DEBUG
        case _:
            raise click.BadParameter("Invalid log level")

    logging.basicConfig(
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=level
    )


logger = logging.getLogger(__name__)
