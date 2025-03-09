from aiogram import types
from aiogram import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.language import get_message
from database.user_db import get_user_language

def register_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(send_help, commands=["help"])
    dp.register_message_handler(initiate_search, commands=["search"])


async def send_welcome(message: types.Message):
    lang = get_user_language(message.from_user.id)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"))
    keyboard.add(InlineKeyboardButton("فارسی 🇮🇷", callback_data="set_lang_fa"))

    await message.answer(get_message("start", lang), reply_markup=keyboard)


async def send_help(message: types.Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_message("help", lang))


async def initiate_search(message: types.Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_message("search_prompt", lang))
