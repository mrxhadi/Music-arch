import os
import shutil
from aiogram import types

DB_PATH = "songs.json"

async def send_database(message: types.Message):
    if os.path.exists(DB_PATH):
        await message.reply_document(types.InputFile(DB_PATH))
    else:
        await message.reply("Database file not found.")

async def update_database(message: types.Message):
    document = message.document
    if document.file_name == "songs.json":
        file_path = await document.download()
        shutil.move(file_path.name, DB_PATH)
        await message.reply("Database updated successfully.")
    else:
        await message.reply("Invalid file. Please send 'songs.json'.")
