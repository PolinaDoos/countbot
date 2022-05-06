import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from add_expense import (
    add_expense_start,
    catch_invalid_input,
    input_amount,
    input_expense_type,
)
from handlers import catch_invalid_input_in_general, greet_user, show_last_5, talk_to_me, end_conversation
import settings


logging.basicConfig(
    filename="countbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Настройки прокси
PROXY = {
    "proxy_url": settings.PROXY_URL,
    "urllib3_proxy_kwargs": {
        "username": settings.PROXY_USERNAME,
        "password": settings.PROXY_PASSWORD,
    },
}


def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    add_expense = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("^(Ввести расход)$"), add_expense_start)],
        states={
            "expense_type": [
                CommandHandler("start", greet_user),
                MessageHandler(Filters.regex("^(Ввести расход)$"), add_expense_start),
                MessageHandler(Filters.regex("^(История записей)$"), show_last_5),
                MessageHandler(Filters.text, input_expense_type),
            ],
            "amount": [
                CommandHandler("start", greet_user),
                MessageHandler(Filters.text, input_amount),
            ],
        },
        fallbacks=[
            MessageHandler(~Filters.text, catch_invalid_input),
            MessageHandler(
                Filters.regex("^(отбой)$"),
                end_conversation,
            ),
        ],
    )

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("lasts", show_last_5))
    dp.add_handler(MessageHandler(Filters.regex("^(История записей)$"), show_last_5))
    dp.add_handler(add_expense)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(MessageHandler(~Filters.text, catch_invalid_input_in_general))

    # логирование
    logging.info("Бот стартовал")

    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()

    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()


if __name__ == "__main__":
    main()
