import json
from aiogram import types
from aiogram.types import InlineQueryResultCachedAudio

DB_PATH = "songs.json"

async def handle_inline_query(inline_query: types.InlineQuery, bot):
    query = inline_query.query.strip()
    
    # بررسی حداقل ۳ حرف
    if len(query) < 3:
        await inline_query.answer(
            results=[],
            switch_pm_text="حداقل ۳ حرف وارد کنید.",
            switch_pm_parameter="start",
            cache_time=1
        )
        return

    # لود دیتابیس
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        songs = json.load(db_file)

    # فیلتر آهنگ‌ها
    matched_songs = [
        song for song in songs
        if query.lower() in song["title"].lower() or query.lower() in song["singer"].lower()
    ]

    # محدود به ۱۰ نتیجه
    results = []
    for idx, song in enumerate(matched_songs[:10]):
        try:
            results.append(
                InlineQueryResultCachedAudio(
                    id=str(idx),
                    audio_file_id=song["file_id"],
                    caption=f"{song['title']} - {song['singer']}"
                )
            )
        except Exception as e:
            print(f"[INLINEBOT] Skipped song '{song['title']}' due to error: {e}")

    # ارسال نتایج
    await inline_query.answer(
        results=results,
        cache_time=1
    )
