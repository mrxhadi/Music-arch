import json
from aiogram import types
from aiogram.types import InlineQueryResultAudio

DB_PATH = "songs.json"

async def handle_inline_query(inline_query: types.InlineQuery, bot):
    query = inline_query.query.lower()
    print(f"[INLINE] Inline query received: {query}")

    if not query:
        await inline_query.answer([], cache_time=1)
        return

    songs = json.load(open(DB_PATH, "r", encoding="utf-8"))
    results = []

    for song in songs:
        if query in song["title"].lower() or query in song["singer"].lower():
            results.append(
                InlineQueryResultAudio(
                    id=str(song["message_id"]),
                    audio_file_id=song["file_id"],
                    title=song["title"],
                    performer=song["singer"],
                    duration=song["duration"]
                )
            )

    await inline_query.answer(results, cache_time=1)
