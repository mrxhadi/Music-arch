from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.user_db import set_user_language, get_user_language

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.message(F.text == "/language")
async def send_language_selection(message: Message):
    """ارسال منوی انتخاب زبان به کاربر"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")],
            [InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang_fa")]
        ]
    )
    logger.info(f"[LANGUAGE] Sent language selection menu to user {message.from_user.id}")
    await message.answer("Please select your language:\nلطفاً زبان خود را انتخاب کنید:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("set_lang_"))
async def language_callback_handler(callback_query: CallbackQuery):
    """ذخیره زبان انتخاب‌شده توسط کاربر"""
    user_id = callback_query.from_user.id
    selected_lang = callback_query.data.replace("set_lang_", "") 

    logger.info(f"[LANGUAGE] Received callback from user {user_id}: {callback_query.data}")

    set_user_language(user_id, selected_lang)

    messages = {
        "en": "Language set to English. Use /help to see available commands.",
        "fa": "زبان به فارسی تغییر یافت. از دستور /help برای مشاهده دستورات استفاده کنید."
    }

    await callback_query.message.answer(messages[selected_lang])
    await callback_query.answer()
    logger.info(f"[LANGUAGE] Language set to {selected_lang} for user {user_id}")
