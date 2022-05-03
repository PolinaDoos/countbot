import json
import logging
import pygsheets
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='countbot.log', level=logging.INFO)

# Настройки прокси
PROXY = {'proxy_url': settings.PROXY_URL,
        'urllib3_proxy_kwargs': {
            'username': settings.PROXY_USERNAME,
            'password': settings.PROXY_PASSWORD
        }
    }


def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)
    # mybot = Updater("КЛЮЧ БОТА", use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("lasts", show_last_5))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    

    # логирование
    logging.info("Бот стартовал")
    
    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()

    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()


def greet_user(update, context):
    username = update.effective_user.first_name
    print('Вызван /start')
    update.message.reply_text(f'Привет, {username}! Ты вызвал команду /start')


def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)
        


def show_last_5(update, context):
    chat_id = update.effective_chat.id
    update.message.reply_text('Вот последние 5 записей:')

    sheet = get_from_googlesheet()
    values = get_last_5_records(sheet)
    msg=''
    for i in values:
        msg = msg + f'{i[0]}, {i[1]}\n'
    print(msg)
    context.bot.send_message(chat_id=chat_id, text=msg)

    # update.message.reply_text(values[0][0]) 
    # update.message.reply_text(str(values))  

    # json_string = json.dumps(values, ensure_ascii=False)
    # values = json.loads(json_string)
    # update.message.reply_text(f'\n{values}\n')
    # update.message.reply_text(f'\n{values[0]}\n')
    # update.message.reply_text(f'\n{values[0][0]}\n')


def get_from_googlesheet():
    # gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS')
    gc = pygsheets.authorize(service_file=settings.GDRIVE_API_CREDENTIALS)
    book = gc.open_by_key(settings.GOOGLE_SHEETS)
    sheet = book.worksheet('title', settings.SELECTED_GSHEET)
    return sheet


def get_last_5_records(sheet):
    raw_values = sheet.get_values(start='J22', end='K500')
    values = []
    for i in raw_values:
        values.append([str(i[0]), int(i[1])])
    return values[-5:]


if __name__ == "__main__":
    main()
