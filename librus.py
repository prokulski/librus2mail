import requests
from bs4 import BeautifulSoup

from base_logger import logger


# URLe
OAUTH_URL = 'https://api.librus.pl/OAuth/Authorization?client_id=46&response_type=code&scope=mydata'
AUTH_URL = 'https://api.librus.pl/OAuth/Authorization?client_id=46'
GRANT_URL = 'https://api.librus.pl/OAuth/Authorization/Grant?client_id=46'
MESSAGES_URL = 'https://synergia.librus.pl/wiadomosci'
MESSAGE_BODY_URL = 'https://synergia.librus.pl'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'


class NotLogged(Exception):
    def __init__(self, message="Not logged into Librus"):
        logger.error(f"Nie zalogowany: {message}")
        self.message = message
        super().__init__(self.message)


class Librus():
    """
    Klasa na podstawie kodu z https://github.com/Mati365/librus-api/blob/master/lib/api.js
    """
    logged = False
    unread_count = None
    __headers = {'User-Agent': USER_AGENT}

    def __init__(self, config):
        self.__do_read_messages = config.get('read_messages', False)
        self.__librus_login = config.get('librus_login')
        self.__librus_password = config.get('librus_password')
        self.__login()

    def __login(self):
        self.__session = requests.Session()

        logger.info(f"Autoryzuję w Librusie konto {self.__librus_login}")
        res = self.__session.get(OAUTH_URL, headers=self.__headers)
        if res.status_code != 200:
            logger.error(
                f"Autoryzacja konta {self.__librus_login}: {res.status_code} {res.error}")
            raise requests.HTTPError(res.status_code, res.error)

        logger.info("Logowanie do Librusa")
        res = self.__session.post(AUTH_URL,
                                  data={'action': 'login',
                                        'login': self.__librus_login,
                                        'pass': self.__librus_password},
                                  headers=self.__headers)
        if res.status_code != 200:
            logger.error(
                f"Logowanie: {res.status_code} {res.error}")
            raise requests.HTTPError(res.status_code, res.error)

        logger.info("Grant uprawnień")
        res = self.__session.get(GRANT_URL, headers=self.__headers)
        if res.status_code != 200:
            logger.error(
                f"Grant uprawnień: {res.status_code} {res.error}")
            raise requests.HTTPError(res.status_code, res.error)

        self.__cookies = self.__session.cookies
        self.logged = True

    def __get_message_body(self, link):
        if not self.logged:
            raise NotLogged()

        url = f"{MESSAGE_BODY_URL}{link}"
        logger.info(f"Pobieram treść wiadomość {link}")
        res = self.__session.get(url,
                                 cookies=self.__cookies,
                                 headers=self.__headers)
        if res.status_code != 200:
            logger.error(
                f"Pobieranie treści wiadomości {link}: {res.status_code} {res.error}")
            raise requests.HTTPError(res.status_code, res.error)

        soup = BeautifulSoup(res.content, 'html.parser')

        message_body = soup.find('div',
                                 attrs={'class': 'container-message-content'})
        message_body = message_body.get_text()

        return message_body

    def get_messages(self):
        def correct_sender(s):
            # wyrzucenie powtórzonego nazwiska w nawiasie
            sender = s.strip()
            sender = sender.split('(')[0].strip()
            # odwrócenie kolejności - imię i nazwisko
            sender = ' '.join(sender.split()[::-1])
            return sender

        if not self.logged:
            raise NotLogged()

        logger.info("Pobieram listę wiadomości")
        res = self.__session.get(MESSAGES_URL,
                                 cookies=self.__cookies,
                                 headers=self.__headers)
        if res.status_code != 200:
            logger.error(
                f"Pobieranie listy wiadomości: {res.status_code} {res.error}")
            raise requests.HTTPError(res.status_code, res.error)

        soup = BeautifulSoup(res.content, 'html.parser')

        mess_tab = soup.find('table',
                             attrs={'class': 'decorated stretch'})
        mess_tab = mess_tab.find('tbody')

        messages = []
        for msg_row in mess_tab.find_all('tr'):
            tds = msg_row.find_all('td')
            message = {
                'title': tds[3].get_text().strip(),
                'sender': correct_sender(tds[2].get_text()),
                'is_unread': False,
                'datetime': tds[4].get_text().strip(),
                'link': tds[2].find('a').attrs.get('href').strip(),
                'has_attachment': True if tds[1].find('img') else False
            }

            # czy wiadomość przeczytana?
            if style := tds[2].attrs.get('style'):
                message['is_unread'] = style.find('bold') > 0

            # pobranie treści wiadomości
            if self.__do_read_messages:
                message['body'] = self.__get_message_body(message.get('link'))

            messages.append(message)

        # sortowanie w kolejności od najnowszych
        messages = sorted(messages, key=lambda m: m['datetime'], reverse=True)
        self.messages = messages

        self.unread_count = sum([m['is_unread'] for m in messages])
