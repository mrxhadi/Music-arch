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

# هندلر ادمین برای پیوی (دستورات و مدیریت دیتابیس)
@router.message(F.chat.type == "private", F.chat.id == ADMIN_ID)
async def admin_command_handler(message: Message):
    print(f"[ADMIN] Received admin command or file from {message.from_user.id}")
    await handle_admin_commands(message, bot)

# هندلر گروه مشترک برای اضافه‌کردن آهنگ‌ها
@router.message(F.chat.id == GROUP_ID)
async def group_message_handler(message: Message):
    print(f"[GROUP] Received new message in group from {message.from_user.id}")
    await handle_new_song(message)

# سایر پیام‌های بی‌اهمیت (لاگ ساده)
@router.message()
async def log_unknown_messages(message: Message):
    print(f"[INLINEBOT] Ignored message from chat ID: {message.chat.id}")

# هندلر اینلاین مود
@dp.inline_query()
async def inline_query_handler(inline_query):
    await handle_inline_query(inline_query, bot)

# شروع بات
async def main():
    print("InlineBot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
