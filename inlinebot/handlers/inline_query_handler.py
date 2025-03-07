import json
from aiogram import types

DB_PATH = "songs.json"

def load_songs():
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

async def handle_inline_query(inline_query: types.InlineQuery, bot):
    query = inline_query.query.lower()
    songs = load_songs()

    if query:
        matched_songs = [
            song for song in songs
            if query in song["title"].lower() or query in song["singer"].lower()
        ][:10]  # حداکثر 10 نتیجه برای جستجو
    else:
        matched_songs = songs[:10]  # فقط 10 آهنگ اول دیتابیس اگر جستجو خالی بود

    print(f"[INLINEBOT] Inline query received: '{query}' - {len(matched_songs)} matches found.")

    results = [
        types.InlineQueryResultAudio(
            id=str(index),
            audio_file_id=song["file_id"],
            title=song["title"],
            performer=song["singer"],
            duration=song["duration"]
        )
        for index, song in enumerate(matched_songs)
    ]

    await bot.answer_inline_query(
        inline_query.id,
        results=results,
        cache_time=1  # کمترین کش برای تست سریع‌تر
    )
