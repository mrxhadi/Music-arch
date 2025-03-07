from handlers.database_handler import send_database, update_database
from aiogram import types
import os

ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def handle_admin_commands(message: types.Message, bot):
    if message.from_user.id != ADMIN_ID:
        await message.reply("شما دسترسی ندارید.")
        return

    if message.text == "/list":
        await send_database(message, bot)

    elif message.document:
        await update_database(message, bot)

    else:
        await message.reply("Invalid command.")
