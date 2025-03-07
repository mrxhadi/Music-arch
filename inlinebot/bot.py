import os
from aiogram import Bot, Dispatcher, executor, types
from handlers.inline_query_handler import handle_inline_query
from handlers.database_handler import send_database, update_database

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# اینلاین مود
@dp.inline_handler()
async def inline_query_handler(query: types.InlineQuery):
    await handle_inline_query(query)

# ارسال دیتابیس با دستور /list
@dp.message_handler(commands=["list"])
async def handle_list_command(message: types.Message):
    await send_database(message)

# بروزرسانی دیتابیس با فایل
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_database_update(message: types.Message):
    await update_database(message)

if __name__ == "__main__":
    print("Inline Bot is running...")
    executor.start_polling(dp, skip_updates=True)
