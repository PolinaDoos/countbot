import logging
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from utils import (
    add_expense_start_keyboard,
    add_to_googlesheet,
    is_allow_user,
    main_keyboard,
)


@is_allow_user
def add_expense_start(update, context):
    update.message.reply_text(
        f"Напиши, на что потрачено.\nЧтобы вернуться в начало, нажми /start",
        reply_markup=add_expense_start_keyboard()
    )
    return "expense_type"


@is_allow_user
def input_expense_type(update, context):
    expense_name = update.message.text
    if len(expense_name) > 2:
        context.user_data["expense_type"] = expense_name.lower()
        update.message.reply_text(
            f"сколько потрачено на {expense_name}?",
        )
        return "amount"
    update.message.reply_text(
        f"{expense_name} - очень короткое название. Введи еще раз",
    )
    return "expense_type"


@is_allow_user
def input_amount(update, context):
    try:
        context.user_data["amount"] = int(update.message.text)
    except ValueError:
        return catch_invalid_input(update, context)
    expense_type = context.user_data["expense_type"]
    amount = context.user_data["amount"]
    add_to_googlesheet([expense_type, amount])
    logging.info(f"Записан расход: {expense_type}, {amount}, автор {update.effective_user.first_name}")
    update.message.reply_text(f"Записано: {expense_type}, {amount}", reply_markup=main_keyboard())
    return ConversationHandler.END


@is_allow_user
def catch_invalid_input(update, context):
    update.message.reply_text("Не понимаю, черновик удален. Нужно начать заново", reply_markup=main_keyboard())
    return ConversationHandler.END
