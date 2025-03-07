import os
import json
from aiogram import Bot, Dispatcher, executor, types

# متغیرهای محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = "songs.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# لود دیتابیس
def load_songs():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

# هندلر اینلاین مود
@dp.inline_handler()
async def inline_query_handler(query: types.InlineQuery):
    search_text = query.query.lower()
    songs = load_songs()

    results = []
    for index, song in enumerate(songs):
        if search_text in song["title"].lower() or search_text in song["singer"].lower():
            results.append(
                types.InlineQueryResultCachedAudio(
                    id=str(index),
                    audio_file_id=song["file_id"],
                    caption=f'{song["title"]} - {song["singer"]}'
                )
            )

    if results:
        await query.answer(results, cache_time=1)
    else:
        await query.answer([], switch_pm_text="No songs found.", switch_pm_parameter="start")

if __name__ == "__main__":
    print("Inline Bot is running...")
    executor.start_polling(dp, skip_updates=True)
