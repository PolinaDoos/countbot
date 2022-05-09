import logging
from telegram import KeyboardButton, ReplyKeyboardMarkup
from constants import COMMANDS_DICT
import settings
import pygsheets
from telegram.ext import ConversationHandler


def main_keyboard():
    return ReplyKeyboardMarkup(
        [[COMMANDS_DICT["История записей"][0], COMMANDS_DICT["Ввести расход"][0]], [COMMANDS_DICT["start"][0]]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def add_expense_start_keyboard():
    return ReplyKeyboardMarkup(
        [[COMMANDS_DICT["start"][0]]],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Введи расход",
    )


def cancel_keyboard():
    return ReplyKeyboardMarkup([COMMANDS_DICT["start"][0]], resize_keyboard=True)


def get_googlesheet():
    gc = pygsheets.authorize(service_file=settings.GDRIVE_API_CREDENTIALS)
    book = gc.open_by_key(settings.GOOGLE_SHEETS)
    sheet = book.worksheet("title", settings.SELECTED_GSHEET)
    return sheet


def get_last_5_records(sheet):
    raw_values = sheet.get_values(start=settings.START_CELL, end=settings.END_CELL)[-5:]
    values = []
    for i in raw_values:
        values.append([str(i[0]), i[1]])
    return values


def get_total_amount(sheet):
    total_period = sheet.get_value(settings.TOTAL_PERIOD)
    total_amount = sheet.get_value(settings.TOTAL_AMOUNT)
    return [total_period, total_amount]


def add_to_googlesheet(values):
    sheet = get_googlesheet()
    sheet.append_table(values)


# декоратор для проверки прав доступа чата
def is_allow_user(func):
    def wrapped(*args, **kwargs):
        chat_id = args[0].effective_chat.id
        if chat_id in settings.ALLOWED_CHAT_IDS:
            return func(*args, **kwargs)
        args[0].message.reply_text(text="Это приватная информация, чел! Обратитесь к @BarsukovaP")
        logging.info(f"chat_id {chat_id}, Username {args[0].effective_user.first_name} полез без спроса")
        return ConversationHandler.END

    return wrapped


# собирает список значений словаря, включая 1 уровень вложенности
def collect_values_list_from_dict(commands_dict):
    text_commands_list = []
    for i in [value for k, value in commands_dict.items()]:
        for j in i:
            text_commands_list.append(j)
    return text_commands_list
