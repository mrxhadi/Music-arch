from aiogram import types
from handlers.search_handler import handle_search

async def handle_private_message(message: types.Message, bot):
    user_input = message.text.strip()
    
    if not user_input.startswith("/"):  # اگر پیام یک دستور نبود
        await handle_search(message, bot)
