# Librus2mail

Skrypt loguje się na konto rodzica w Librusie, przechodzi do skrzynki wiadomości i ściąga listę wiadomości (nagłówki lub treści).

Jeśli pojawi się nowa wiadomość - wysyła mailem pełną listę wiadomości (tabela z nagłówkami: tytuł wiadomości, imię i nazwisko nadawcy, datę utworzenia wiadomości). W przyszłości będzie też wysyłanie treści wiadomości.

Za wzór komunikacji z Librusem (głównie logowanie) posłużyło [repo](https://github.com/Mati365/librus-api/) [https://github.com/Mati365/librus-api/](https://github.com/Mati365/librus-api/)

## Uruchomienie

Uruchamia się to cudo przez

`python main.py`

Potrzebny Python 3.8+ (walrus operator <3)

## Konfiguracja

Konfiguracja zawarta jest w pliku *config.yaml*. Parametry podzielone są na konta (każde konto w Librusie może mieć innych odbiorców powiadomień), w związku z tym plik konfiguracyjny składa się z sekcji parametrów globalnych i sekcji parametrów per konto (tablica parametrów w bloku **librus_users**). Znaczenie parametrów:

#### Parametry globalne
* **wait_time_s** - jak długo czekać pomiędzy kolejnymi logowaniami do Librusa?

#### Parametry dla konta
* **librus_login** - ID konta rodzica (to co wpisuje się w pole *login*)
* **librus_password** - hasło do konta rodzica (to co wpisuje się w pole *hasło*)
* **librus_login_name** - (na przykład) imię dziecka - jak się ma ich więcej to łatwiej rozróżnić niż po numerach kont ;)
* **read_messages** - czy skrypt ma zbierać treść wiadomości?
  * **UWAGA:** na razie treść wiadomości nie jest nigdzie wykorzystywana, a wejście w wiadomość (skrypt to robi) sprawia, że staje się ona przeczytana. Zalecam ustawienie flagi na *false*
* **notification_receivers** - lista adresów email odbiorców powiadomień

### Dodatkowo

Skrypt do wysyłania powiadomień mailowych używa biblioteki *[yagmail](https://github.com/kootenpv/yagmail)*, w związki z tym muszą być ustawione zmienne środowiskowe:

* **GMAIL_USER** - użytkownik Google Mail z którego konta będzie wysyłane powiadomienie
* **GMAIL_PASS** - hasło do tego konta

Po szczegóły konfiguracji GMaila odsyłam na stronę biblioteki.

## Do zrobienia

* wysyłanie treści wiadomości mailem