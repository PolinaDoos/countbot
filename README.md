# PS_countbot

PS_countbot - это бот для Telegram, который выводит информацию о последних тратах и позволяет внести новые траты с указанием категории.

Работает в связке с GoogleSheets по API.

В файле переменных окружения указываются CREDENTIALS google-shhet, с которым работает бот.

### Установка

1. Клонируйте репозиторий, создайте и активируйте виртуальное окружение
2. Установите зависимости `pip install -r requirements.txt`
3. Создайте файл .env в корне проекта и создайте в нем переменные:
    ```
    PROXY_URL="str"
    PROXY_USERNAME="str"
    PROXY_PASSWORD="str"
    API_KEY='str'
    GDRIVE_API_CREDENTIALS='{full .json content}'
    GOOGLE_SHEETS="str"
    SELECTED_GSHEET="sheet name"
    START_CELL="A1 or other"
    END_CELL="B100 or other"
    TOTAL_PERIOD="A1 or other"
    TOTAL_AMOUNT="A1 or other"
    ALLOWED_CHAT_IDS="[number, number]"
    ```
    Значения переменных можно запросить у автора проекта.
