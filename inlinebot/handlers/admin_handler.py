import os
import json
from aiogram import types

DB_PATH = "songs.json"
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ارسال دیتابیس با دستور /list
async def handle_admin_commands(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("شما دسترسی ندارید.")
        return

    if message.text == "/list":
        if os.path.exists(DB_PATH):
            await message.answer_document(
                types.FSInputFile(DB_PATH),
                caption="دیتابیس فعلی آهنگ‌ها"
            )
        else:
            await message.reply("دیتابیس پیدا نشد.")

    # دریافت فایل جدید دیتابیس برای آپدیت دستی
    elif message.document:
        if message.document.file_name == "songs.json":
            file = await message.document.download(destination_file=DB_PATH)
            await message.reply("دیتابیس با موفقیت جایگزین شد.")
        else:
            await message.reply("لطفاً فقط فایل songs.json ارسال کنید.")
