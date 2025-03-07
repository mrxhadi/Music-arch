import json
from aiogram import types

DB_PATH = "songs.json"

def load_songs():
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

async def handle_inline_query(inline_query: types.InlineQuery, bot):
    query = inline_query.query.strip().lower()  # حذف فاصله‌های اضافی

    if len(query) < 3:
        await bot.answer_inline_query(
            inline_query.id,
            results=[],
            cache_time=1,
            switch_pm_text="حداقل 3 حرف وارد کنید.",
            switch_pm_parameter="start"
        )
        return

    songs = load_songs()
    matched_songs = [
        song for song in songs
        if query in song["title"].lower() or query in song["singer"].lower()
    ]

    results = []
    for index, song in enumerate(matched_songs[:20]):  # محدود به 10 نتیجه
        try:
            results.append(
                types.InlineQueryResultAudio(
                    id=str(index),
                    audio_file_id=song["file_id"],
                    title=song["title"],
                    performer=song["singer"],
                    duration=song["duration"]
                )
            )
        except Exception as e:
            print(f"[INLINEBOT] Skipped song '{song['title']}' due to error: {e}")

    await bot.answer_inline_query(
        inline_query.id,
        results=results,
        cache_time=1
                )
