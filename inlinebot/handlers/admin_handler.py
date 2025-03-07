import os
import json
from aiogram import types
from aiogram.types import FSInputFile

DB_PATH = "songs.json"
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ارسال دیتابیس با دستور /list
async def handle_admin_commands(message: types.Message):
    # اطمینان از اینکه پیام از ادمین است
    if message.from_user.id != ADMIN_ID:
        await message.reply("شما دسترسی ندارید.")
        return

    # لاگ دریافت دستور
    print(f"[ADMIN_HANDLER] Received command from {message.from_user.id}: {message.text}")

    if message.text == "/list":
        # چک کردن و ساخت دیتابیس اگر نبود
        if not os.path.exists(DB_PATH):
            await message.reply("دیتابیس پیدا نشد.")
            return

        # لود دیتابیس و ارسال فایل
        songs = json.load(open(DB_PATH, "r", encoding="utf-8"))
        if not songs:
            await message.reply("دیتابیس خالی است.")
            return

        # ارسال دیتابیس به پیوی ادمین
        await message.answer_document(
            FSInputFile(DB_PATH),
            caption="دیتابیس فعلی آهنگ‌ها"
        )
        print(f"[ADMIN_HANDLER] Database sent to admin.")
