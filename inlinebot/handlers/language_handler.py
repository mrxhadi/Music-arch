from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.user_db import set_user_language, get_user_language

async def send_language_selection(message: types.Message):
    """ارسال منوی انتخاب زبان به کاربر"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
        InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang_fa")
    )
    await message.answer("Please select your language:\nلطفاً زبان خود را انتخاب کنید:", reply_markup=keyboard)

async def language_callback_handler(callback_query: types.CallbackQuery):
    """ذخیره زبان انتخاب‌شده توسط کاربر"""
    user_id = callback_query.from_user.id
    selected_lang = callback_query.data.split("_")[1]  # گرفتن en یا fa

    set_user_language(user_id, selected_lang)

    messages = {
        "en": "Language set to English. Use /help to see available commands.",
        "fa": "زبان به فارسی تغییر یافت. از دستور /help برای مشاهده دستورات استفاده کنید."
    }

    await callback_query.message.answer(messages[selected_lang])
    await callback_query.answer()
