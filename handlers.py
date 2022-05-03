from utils import *


def greet_user(update, context):
    username = update.effective_user.first_name
    update.message.reply_text(f'Привет, {username}! Ты вызвал команду /start', reply_markup=main_keyboard())

def talk_to_me(update, context):
    # user_text = update.message.text 
    update.message.reply_text('Что хочешь сделать?', reply_markup=main_keyboard())

def show_last_5(update, context):
    chat_id = update.effective_chat.id
    update.message.reply_text('Вот последние 5 записей:')

    sheet = get_from_googlesheet()
    values = get_last_5_records(sheet)
    msg=''
    for i in values:
        msg = msg + f'{i[0]}, {i[1]}\n'
    context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=main_keyboard())

    # update.message.reply_text(values[0][0]) 
    # update.message.reply_text(str(values))  

    # json_string = json.dumps(values, ensure_ascii=False)
    # values = json.loads(json_string)
    # update.message.reply_text(f'\n{values}\n')
    # update.message.reply_text(f'\n{values[0]}\n')
    # update.message.reply_text(f'\n{values[0][0]}\n')


# def add_expense(update, context):
#     sheet = get_from_googlesheet()
#     pass


