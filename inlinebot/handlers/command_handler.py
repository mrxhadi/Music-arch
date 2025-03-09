from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.language import get_message
from database.user_db import get_user_language

router = Router()

@router.message(F.text == "/start")
async def send_welcome(message: Message):
    lang = get_user_language(message.from_user.id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="English 🇬🇧", callback_data="set_lang_en")],
            [InlineKeyboardButton(text="فارسی 🇮🇷", callback_data="set_lang_fa")]
        ]
    )

    await message.answer(get_message("start", lang), reply_markup=keyboard)


@router.message(F.text == "/help")
async def send_help(message: Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_message("help", lang))


@router.message(F.text == "/search")
async def initiate_search(message: Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(get_message("search_prompt", lang))
