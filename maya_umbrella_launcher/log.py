import os
import logging


def get_logger():
    print('xxx log setup')
    _logger = logging.getLogger('maya_umbrella_launcher')
    _logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(os.path.join(os.path.expanduser('~'), 'maya_umbrella_launcher.log'), mode='w')
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)

    return _logger


logger = get_logger()
