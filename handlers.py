import logging
from telegram import ParseMode

from telegram.ext import ConversationHandler

from utils import (
    get_googlesheet,
    get_last_5_records,
    get_total_amount,
    is_allow_user,
    main_keyboard,
    main_keyboard_no_one_time,
)


def greet_user(update, context):
    username = update.effective_user.first_name
    logging.info(f"Username {username} вызвал комагду /start")
    update.message.reply_text(f"Привет, {username}! Ты вызвал команду /start", reply_markup=main_keyboard_no_one_time())
    return ConversationHandler.END


def talk_to_me(update, context):
    update.message.reply_text("Что хочешь сделать?", reply_markup=main_keyboard_no_one_time())
    return ConversationHandler.END


@is_allow_user
def show_last_5(update, context):
    chat_id = update.effective_chat.id
    logging.info(f"chat_id {chat_id}, Username {update.effective_user.first_name} запросил историю записей")
    update.message.reply_text("Вот последние 5 записей:")
    sheet = get_googlesheet()
    total = get_total_amount(sheet)
    values = get_last_5_records(sheet)
    msg = ""
    for i in values:
        msg = msg + f"{i[0]}, {i[1]}\n"
    msg += f"<i>{total[0].capitalize()}: {total[1]}</i>\n"

    context.bot.send_message(
        chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML, reply_markup=main_keyboard_no_one_time()
    )
    return ConversationHandler.END


def catch_invalid_input_in_general(update, context):
    update.message.reply_text("Не понимаю картинку и песню. Но можешь станцевать!")
    update.message.reply_text("Я не пойму, но ты повеселишься", reply_markup=main_keyboard_no_one_time())
    return ConversationHandler.END
