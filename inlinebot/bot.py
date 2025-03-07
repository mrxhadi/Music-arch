import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ContentType
from aiogram.types import FSInputFile
from aiogram.filters import Command
from handlers.inline_query_handler import handle_inline_query
from handlers.database_handler import send_database, update_database

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.inline_query()
async def inline_query_handler(event: types.InlineQuery):
    await handle_inline_query(event)


@dp.message(Command("list"))
async def handle_list_command(message: types.Message):
    await send_database(message, bot)


@dp.message()
async def handle_database_update(message: types.Message):
    if message.document and message.document.file_name == "songs.json":
        await update_database(message, bot)


async def main():
    print("Inline Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
