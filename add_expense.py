from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from utils import add_to_googlesheet, cancel_keyboard, main_keyboard

def add_expense_start(update, context):
    update.message.reply_text(
        f"Напиши, на что потрачено.\nЧтобы вернуться назад, нажми /start",
        # reply_markup=cancel_keyboard()
    )
    return "expense_type"

def input_expense_type(update, context):
    expense_name = update.message.text
    if expense_name == 'Ввести расход':
        return ConversationHandler.END
    if len(expense_name) > 2:
        context.user_data["expense_type"] = expense_name
        update.message.reply_text(f'сколько потрачено на {expense_name}?')
        return "amount"
    update.message.reply_text(
        f'{expense_name} - очень короткое название. Введи еще раз',
        # reply_markup=cancel_keyboard()
    )
    return "expense_type"

def input_amount(update, context):
    try:
        context.user_data['amount'] = int(update.message.text)
    except ValueError:
        return catch_invalid_input(update, context)
    add_to_googlesheet([context.user_data["expense_type"], context.user_data["amount"]])
    update.message.reply_text(
        f'Записано: {context.user_data["expense_type"]}, {context.user_data["amount"]}',
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END

def catch_invalid_input(update, context):
    update.message.reply_text("Не понимаю, черновик будет удален. Нужно начать заново",
                               reply_markup=main_keyboard())
    return ConversationHandler.END
