import os
from aiogram import Bot, Dispatcher, executor, types
from handlers.inline_query_handler import handle_inline_query

# متغیر محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# هندلر اینلاین مود
@dp.inline_handler()
async def inline_query_handler(query: types.InlineQuery):
    await handle_inline_query(query)

if __name__ == "__main__":
    print("Inline Bot is running...")
    executor.start_polling(dp, skip_updates=True)
