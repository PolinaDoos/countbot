import logging
from telegram import ReplyKeyboardMarkup
import settings
import pygsheets
from telegram.ext import ConversationHandler


def main_keyboard():
    return ReplyKeyboardMarkup([['История записей'], ['Ввести расход']], resize_keyboard=True)

def cancel_keyboard():
    return ReplyKeyboardMarkup([['В начало']], resize_keyboard=True)

def get_from_googlesheet():
    gc = pygsheets.authorize(service_file=settings.GDRIVE_API_CREDENTIALS)
    book = gc.open_by_key(settings.GOOGLE_SHEETS)
    sheet = book.worksheet('title', settings.SELECTED_GSHEET)
    return sheet

def get_last_5_records(sheet):
    raw_values = sheet.get_values(start=settings.START_CELL, end=settings.END_CELL)[-5:]
    values = []
    for i in raw_values:
        values.append([str(i[0]), int(i[1])])
    return values

def add_to_googlesheet(values):
    sheet = get_from_googlesheet()
    sheet.append_table(values)

# декоратор для проверки прав доступа чата
def is_allow_user(func):
    def wrapped(*args, **kwargs):
        chat_id = args[0].effective_chat.id      
        if chat_id in settings.ALLOWED_CHAT_IDS:
            return func(*args, **kwargs)
        args[0].message.reply_text(text="Это приватная информация, чел! Обратитесь к @BarsukovaP")
        logging.info(f'chat_id {chat_id}, Username {args[0].effective_user.first_name} полез без спроса')
        return ConversationHandler.END
    return wrapped
