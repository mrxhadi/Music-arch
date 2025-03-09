from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.language import get_message
from database.user_db import get_user_language

router = Router()  # ایجاد Router برای مدیریت هندلرها

@router.message(commands=["start"])
async def send_welcome(message: types.Message):
    lang = get_user_language(message.from_user.id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="English 🇬🇧", callback_data="set_lang_en")],
        [InlineKeyboardButton(text="فارسی 🇮🇷", callback_data="set_lang_fa")]
    ])

    await message.answer(get_message("start", lang), reply_markup=keyboard)

@router.message(commands=["help"])
async def send_help(message: types.Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_message("help", lang))

@router.message(commands=["search"])
async def initiate_search(message: types.Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_message("search_prompt", lang))
