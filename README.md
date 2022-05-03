# PS_countbot

PS_countbot - это бот для Telegram, который выводит информацию о последних тратах и позволяет внести новые траты с указанием категории.
Работает в связке с GoogleSheets по API.

### Установка

1. Клонируйте репозиторий, создайте виртуальное окружение
2. Установите зависимости `pip install -r requirements.txt`
3. Создайте файл settings.py и создайте в нем переменные:
    ```
    API_KEY = 
    PROXY_URL = 
    PROXY_USERNAME = 
    PROXY_PASSWORD = 
    GDRIVE_API_CREDENTIALS = 
    GOOGLE_SHEETS = 
    SELECTED_GSHEET = 
    ```
    Значения переменных можно запросить у автора проекта.
