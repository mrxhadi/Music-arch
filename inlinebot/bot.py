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

# لاگ گرفتن از همه پیام‌ها
@router.message()
async def log_all_messages(message: Message):
    print(f"[INLINEBOT] Received message from chat ID: {message.chat.id}")

# هندلر مخصوص گروه مشترک (بررسی و اضافه‌کردن آهنگ)
@router.message(F.chat.id == GROUP_ID)
async def group_message_handler(message: Message):
    print(f"[GROUP] Received new song in group from {message.from_user.id}")
    await handle_new_song(message)

# هندلر مخصوص ادمین برای مدیریت (مثل /list)
@router.message(F.chat.id == ADMIN_ID, F.text.startswith("/"))
async def admin_command_handler(message: Message):
    print(f"[ADMIN] Received admin command: {message.text}")
    await handle_admin_commands(message)

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
