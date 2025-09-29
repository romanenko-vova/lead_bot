import logging
import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    PicklePersistence,
)

from handlers.progrev_handler import (
    start,
    get_answer,
    get_name,
    get_phone,
    get_inline_button,
)
from db.database import create_tables
from config.states import FIRST_MESSAGE, GET_NAME, GET_PHONE, INLINE_BUTTON
from logs.logger import logger

load_dotenv()


if __name__ == "__main__":
    persistence = PicklePersistence(filepath="lead_bot")
    application = (
        ApplicationBuilder()
        .token(os.getenv("TOKEN"))
        .persistence(persistence)
        .post_init(create_tables)
        .build()
    )
    # 1
    # Handler - обработчик, который будет обрабатывать
    # CommandHandler - обработчик, который будет обрабатывать команды
    # MessageHandler - обработчик, который будет обрабатывать сообщения
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_MESSAGE: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=get_answer,
                )
            ],
            GET_NAME: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=get_name,
                )
            ],
            GET_PHONE: [
                MessageHandler(
                    filters=filters.CONTACT,
                    callback=get_phone,
                )
            ],
            INLINE_BUTTON: [
                CallbackQueryHandler(
                    callback=get_inline_button, pattern="yes"
                ),
                CallbackQueryHandler(callback=start, pattern="no"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        persistent=True,
        name="conv_handler",
    )

    application.add_handler(conv_handler)
    logger.info("Бот запущен ✅")
    application.run_polling()
