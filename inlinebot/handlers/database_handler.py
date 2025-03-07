import os
import shutil
from aiogram import types, Bot

DB_PATH = "songs.json"

async def send_database(message: types.Message, bot: Bot):
    if os.path.exists(DB_PATH):
        await bot.send_document(
            chat_id=message.chat.id,
            document=types.FSInputFile(DB_PATH),
            caption="Here is the current database."
        )
    else:
        await message.answer("Database file not found.")

async def update_database(message: types.Message, bot: Bot):
    if message.document and message.document.file_name == "songs.json":
        file = await bot.download(message.document)
        with open(DB_PATH, "wb") as f:
            f.write(file.read())
        await message.answer("Database updated successfully.")
    else:
        await message.answer("Invalid file. Please send 'songs.json'.")
