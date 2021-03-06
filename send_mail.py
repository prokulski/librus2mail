from os import environ
import yagmail
from base_logger import logger


def send_mail(config, df):
    # na potrzeby wysyłania maili
    GMAIL_USER = environ.get('GMAIL_USER')
    GMAIL_PASS = environ.get('GMAIL_PASS')

    # treść maila
    contents = f"""
    <p>W Librusie dla konta {config['librus_login']} <strong>({config['librus_login_name']})</strong> pojawiły się <strong>nowe wiadomości</strong>.</p>
    <p>&nbsp;</p>
    <p>Lista wszystkich wiadomości (nowe <strong>boldem</strong>):</p>
    <table border="1" cellspacing="0" cellpadding="10">
    <thead><tr><th>Tytuł</th><th>Nadawca</th><th>Data</th></tr></thead>
    <tbody>
    """

    for r in df:
        if r['is_unread']:
            contents += f"""
            <tr>
            <td><strong>{r['title']}</strong></td>
            <td><strong>{r['sender']}</strong></td>
            <td><strong>{r['datetime']}</strong></td>
            </tr>
            """
        else:
            contents += f"""
            <tr>
            <td>{r['title']}</td>
            <td>{r['sender']}</td>
            <td>{r['datetime']}</td>
            </tr>
            """

    contents += "</tbody></table>"

    # wyslanie maila
    logger.info("Wysyłam maila z podsumowaniem")
    yag = yagmail.SMTP(GMAIL_USER, GMAIL_PASS)

    contents = contents.replace("\n", "")

    yag.send(config['notification_receivers'],
             f"{config['librus_login_name']} ma nową wiadomość w Librusa (konto {config['librus_login']})",
             contents)
    logger.info("Mail z podsumowaniem wysłany")
