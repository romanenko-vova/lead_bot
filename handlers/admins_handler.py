from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    ContextTypes,
)
from db.users_crud import get_users
from logs.logger import logger
import csv
import asyncio
from config.states import ADMIN_START
async def admins_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Список пользователей", callback_data="users_list")],
        [InlineKeyboardButton("Список пользователей с тегом Горячий", callback_data="hot_users_list")],
        [InlineKeyboardButton("Список пользователей с тегом Обычный", callback_data="usual_users_list")],
        [InlineKeyboardButton("Список пользователей с тегом Холодный", callback_data="cold_users_list")],
        [InlineKeyboardButton("Список пользователей csv", callback_data="csv_users_list")],
        [InlineKeyboardButton("Paссылка", callback_data="send_message")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Привет, админ!",
        reply_markup=markup,
    )
    return ADMIN_START

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    text = 'Список пользователей\:\n'
    text += '№ \- Ccылка \- Телефон \- Email\n'
    for n, user in enumerate(users, 1):
        print(user)
        text += f'{n}\. [{user[2]}](tg://user?id={user[1]}) \- {user[3]} \- {user[4]}\n'
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
        parse_mode="MarkdownV2",
    )
    await admins_start(update, context)
    
async def csv_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    with open('users.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['№', 'Ccылка', 'Телефон', 'Email'])
        for n, user in enumerate(users, 1):
            writer.writerow([n, user[2], user[3], user[4]])
            
    await context.bot.send_document(
        chat_id=update.effective_user.id,
        document=open('users.csv', 'rb'),
        caption='Список пользователей csv',
    )
    await admins_start(update, context)


async def spam_send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    logger.info(f'Рассылка началась, пользователей: {len(users)}')
    for user in users:
        try: 
            await context.bot.send_message(
                chat_id=user[1],
                text='Привет!',
            )
            await asyncio.sleep(0.07)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения пользователю {user[1]}: {e}')
            continue
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text='Рассылка завершена',
    )
    logger.info(f'Рассылка завершена')
    await admins_start(update, context)
    