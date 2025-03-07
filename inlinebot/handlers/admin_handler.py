import os
import json
from aiogram import types
from aiogram.types import FSInputFile
from database.songs_db import create_db_if_not_exists

DB_PATH = "songs.json"
ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def handle_admin_commands(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("شما دسترسی ندارید.")
        return

    if message.text.strip() == "/list":
        print(f"[ADMIN_HANDLER] /list command received from {message.from_user.id}")

        create_db_if_not_exists()

        if not os.path.exists(DB_PATH):
            await message.reply("دیتابیس پیدا نشد.")
            return

        songs = json.load(open(DB_PATH, "r", encoding="utf-8"))
        if not songs:
            await message.reply("دیتابیس خالی است.")
            return

        await message.answer_document(
            FSInputFile(DB_PATH),
            caption="دیتابیس فعلی آهنگ‌ها"
        )
        print(f"[ADMIN_HANDLER] Database sent to admin.")
    else:
        await message.reply("دستور نامعتبر است.")
