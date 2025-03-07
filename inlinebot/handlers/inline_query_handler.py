import json
from aiogram import types
from database.songs_db import load_songs

async def handle_inline_query(inline_query: types.InlineQuery, bot):
    query = inline_query.query.lower()
    results = []
    songs = load_songs()

    for idx, song in enumerate(songs):
        if query in song["title"].lower() or query in song["singer"].lower():
            results.append(
                types.InlineQueryResultCachedAudio(
                    id=str(idx),
                    audio_file_id=song["file_id"],
                    title=song["title"],
                    performer=song["singer"]
                )
            )

    await bot.answer_inline_query(
        inline_query.id,
        results=results[:50],  # حداکثر ۵۰ نتیجه
        cache_time=1
    )
