import os
import json
from aiogram import types
from aiogram.types import FSInputFile

DB_PATH = "songs.json"
ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def handle_admin_commands(message: types.Message):
    user_id = message.from_user.id
    print(f"[INLINEBOT] Received message from {user_id}: {message.text}")

    if user_id != ADMIN_ID:
        await message.reply("شما دسترسی ندارید.")
        print(f"[INLINEBOT] Unauthorized user: {user_id}")
        return

    # اگر پیام فایل بود (برای آپدیت دیتابیس)
    if message.document:
        if message.document.file_name == "songs.json":
            await message.document.download(destination_file=DB_PATH)
            await message.reply("دیتابیس با موفقیت جایگزین شد.")
            print("[INLINEBOT] Database updated successfully.")
        else:
            await message.reply("فقط فایل songs.json قابل قبول است.")
            print("[INLINEBOT] Invalid file uploaded.")
        return  # پایان، چون فایل ارسال شده بوده

    # اگر دستور متنی بود
    text = message.text.split()[0]  # حذف احتمالی بات نیم مثل /list@MyBot
    print(f"[INLINEBOT] Command received: {text}")  # لاگ دستور برای بررسی

    if text == "/list":
        if os.path.exists(DB_PATH):
            songs = json.load(open(DB_PATH, "r", encoding="utf-8"))
            if not songs:
                await message.reply("دیتابیس خالی است.")
                print("[INLINEBOT] Database is empty.")
                return

            await message.answer_document(
                FSInputFile(DB_PATH),
                caption="دیتابیس فعلی آهنگ‌ها"
            )
            print("[INLINEBOT] Database sent successfully.")
        else:
            await message.reply("فایل دیتابیس پیدا نشد.")
            print("[INLINEBOT] Database file not found.")
