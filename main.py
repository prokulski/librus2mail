from time import sleep

from config import read_config
from base_logger import logger
from librus import Librus
from send_mail import send_mail


if __name__ == '__main__':
    config = read_config('config.yaml')

    checked = False
    while True:
        try:
            l = Librus(config)
            l.get_messages()
            checked = True
        except Exception as e:
            logger.error(f"Błąd w głównej pętli: {e}")
            checked = False

        if checked:
            if l.unread_count:
                logger.info("Pojawiły się nowe wiadomości")
                send_mail(config, l.messages)
            else:
                logger.info("Brak nowych wiadomości")

            del(l)

        logger.info(f"Czekam przez {config['wait_time_s']} sekund")
        sleep(config['wait_time_s'])
