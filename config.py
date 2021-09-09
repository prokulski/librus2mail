from os import environ
import yaml
from base_logger import logger


def read_config(config_file='config.yaml'):
    logger.info(f"Wczytuję konfigurację z {config_file}")
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # na potrzeby wysyłania maili
    config['GMAIL_USER'] = environ.get('GMAIL_USER')
    config['GMAIL_PASS'] = environ.get('GMAIL_PASS')

    return config
