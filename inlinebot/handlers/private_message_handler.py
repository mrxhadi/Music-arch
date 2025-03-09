from aiogram import types
from database.user_database import set_user_language, get_user_language
from utils.language import get_language_keyboard
from handlers.command_handler import handle_command

async def handle_private_message(message: types.Message, bot):
    user_id = message.from_user.id

    # درخواست انتخاب زبان هنگام /start
    if message.text == "/start":
        await message.answer("Choose your language:", reply_markup=get_language_keyboard())
        return

    # تنظیم زبان کاربر
    if message.text in ["English", "فارسی"]:
        set_user_language(user_id, message.text)
        await message.answer(f"Language set to {message.text}.")
        return

    # پردازش سایر دستورات
    await handle_command(message, bot)
