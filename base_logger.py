import logging


LOG_FILE_NAME = 'librus.log'
LOGGER_NAME = 'librus'


logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.INFO)

# format logów
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log do pliku
fh = logging.FileHandler(LOG_FILE_NAME)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

# log na konsolę
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

# dodanie do handlera
logger.addHandler(fh)
logger.addHandler(ch)
