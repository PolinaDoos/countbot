from telegram import ReplyKeyboardMarkup
import settings
import pygsheets


def main_keyboard():
    return ReplyKeyboardMarkup([['История записей'], ['Ввести расход']], resize_keyboard=True)

def cancel_keyboard():
    return ReplyKeyboardMarkup([['В начало']], resize_keyboard=True)

def get_from_googlesheet():
    # gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS')
    gc = pygsheets.authorize(service_file=settings.GDRIVE_API_CREDENTIALS)
    book = gc.open_by_key(settings.GOOGLE_SHEETS)
    sheet = book.worksheet('title', settings.SELECTED_GSHEET)
    return sheet

def get_last_5_records(sheet):
    raw_values = sheet.get_values(start=settings.START_CELL, end=settings.END_CELL)
    values = []
    for i in raw_values:
        values.append([str(i[0]), int(i[1])])
    return values[-5:]

def add_to_googlesheet(values):
    sheet = get_from_googlesheet()
    sheet.append_table(values)
