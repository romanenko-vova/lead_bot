import logging
import os
from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from handlers.progrev_handler import (
    start,
    get_answer,
    get_name,
    get_phone,
    get_inline_button,
)

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

from config.states import FIRST_MESSAGE, GET_NAME, GET_PHONE, INLINE_BUTTON


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()
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
    )

    application.add_handler(conv_handler)

    application.run_polling()
