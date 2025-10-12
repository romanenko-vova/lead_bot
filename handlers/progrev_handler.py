from datetime import timedelta
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import FIRST_MESSAGE, GET_NAME, GET_PHONE, INLINE_BUTTON
from utils.escape_sym import escape_sym
from handlers.jobs import send_job_message
from db.users_crud import create_user, get_user, update_user
from logs.logger import logger
from db.user_tags_crud import create_user_tag
from config.config import ADMIN_ID
from handlers.admins_handler import admins_start


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная информация о том что произошло
    # update.effective_user - информация о человеке
    # update.effective_chat - информация о чате
    # update.effective_message - информация о сообщении
    # context - контекст, в котором мы можем использовать бота
    if update.effective_user.id == int(ADMIN_ID):
        return await admins_start(update, context)
    
    query = update.callback_query
    """отвечаем на кнопку InlineKeyboardButton"""
    if query:
        await query.answer()
        await query.delete_message()
    else:
        if not await get_user(update.effective_user.id):
            await create_user(update.effective_user.id)
            logger.info(f"Пользователь {update.effective_user.id} создан 🚀")
            await create_user_tag(update.effective_user.id, "Горячий")
            logger.info(f"Пользователь {update.effective_user.id} добавлен в таблицу users_tags 🚀")

    keyboard = [["Да", "Нет"], ["Ещё не знаю"]]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        input_field_placeholder="Выбери вариант ответа",
    )
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=escape_sym(
            f"Привет, {update.effective_user.first_name}. \n*Хочешь гайд?*"
        ),
        reply_markup=markup,
        parse_mode="MarkdownV2",
    )
    
    job = context.job_queue.run_once(
        send_job_message,
        when=timedelta(seconds=30),
        data={"message": "Привет"},
        name=f"send_job_message_{update.effective_user.id}",
        chat_id=update.effective_user.id,
    )
    context.user_data['job_name'] = job.name
    
    return FIRST_MESSAGE


async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отменяем запланированное сообщение, если пользователь ответил
    if 'job_name' in context.user_data:
        for jobs in context.job_queue.get_jobs_by_name(context.user_data['job_name']):
            jobs.schedule_removal()
    answer = update.effective_message.text
    keyboard = [[update.effective_user.first_name]]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        input_field_placeholder="Нажми на своё имя или напишите",
    )
    context.user_data["answer"] = answer
    if answer == "Да":
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Чтобы забрать гайд, напиши своё имя.",
            reply_markup=markup,
        )
        return GET_NAME
    else:
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data="yes"),
                InlineKeyboardButton("Нет", callback_data="no"),
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Тогда всё!",
            reply_markup=markup,
        )
        context.job_queue.run_once(
            send_job_message,
            when=timedelta(seconds=30),
            data={"message": "Привет"},
            name="send_job_message",
            chat_id=update.effective_user.id,
        )
        return INLINE_BUTTON


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text
    await update_user(update.effective_user.id, name)
    keyboard = [
        [KeyboardButton("Отправить номер телефона", request_contact=True)]
    ]
    markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        input_field_placeholder="Нажми на кнопку",
    )
    context.user_data["name"] = name
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Чтобы забрать гайд, напиши свой номер телефона.",
        reply_markup=markup,
    )
    return GET_PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.effective_message.contact.phone_number
    context.user_data["phone"] = phone
    print(context.user_data)


async def get_inline_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    if query.data == "yes":
        keyboard = [[InlineKeyboardButton("Да", callback_data="yes")]]
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Спасибо за ответ!", reply_markup=markup
        )
