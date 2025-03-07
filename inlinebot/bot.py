import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from dotenv import load_dotenv
from handlers.message_handler import handle_new_song
from handlers.admin_handler import handle_admin_commands
from handlers.inline_query_handler import handle_inline_query

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

router = Router()
dp.include_router(router)

# هندلر پیام‌ها (تشخیص گروه و پیوی)
@router.message()
async def message_handler(message: Message):
    # اگر پیام از پیوی ادمین باشد
    if message.chat.id == ADMIN_ID:
        print(f"[ADMIN] Received admin command: {message.text}")  # لاگ برای بررسی
        await handle_admin_commands(message)  # دستورهای ادمین
    elif message.chat.id == GROUP_ID:
        print(f"[GROUP] Received new song in group from {message.from_user.id}")  # لاگ برای بررسی
        await handle_new_song(message, bot)  # آهنگ‌ها از گروه
    else:
        print(f"[INLINEBOT] Received message from unknown chat ID: {message.chat.id}")

# هندلر اینلاین مود
@dp.inline_query()
async def inline_query_handler(inline_query):
    await handle_inline_query(inline_query, bot)

# اجرای ربات و شروع فرآیند
async def main():
    print("InlineBot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
