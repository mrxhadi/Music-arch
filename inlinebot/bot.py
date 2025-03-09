import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from dotenv import load_dotenv
from handlers.message_handler import handle_new_song
from handlers.admin_handler import handle_admin_commands
from handlers.inline_query_handler import handle_inline_query
from handlers.command_handler import register_commands
from handlers.search_handler import handle_search
from handlers.language_handler import handle_language_selection, process_language_callback
from database.user_database import get_user_language

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

# ثبت دستورات در Dispatcher
register_commands(dp)

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

# هندلر پیام‌های خصوصی برای پردازش جستجو و زبان
@router.message(F.chat.type == "private")
async def private_message_handler(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    if message.text.startswith("/"):
        print(f"[USER] Unknown command received: {message.text}")
        return

    await handle_search(message, bot)

# هندلر دکمه‌های انتخاب زبان
@router.callback_query(F.data.startswith("set_lang_"))
async def language_callback_handler(callback_query: CallbackQuery):
    await process_language_callback(callback_query, bot)

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
