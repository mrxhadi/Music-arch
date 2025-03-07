import os
import json
from aiogram import types

DB_PATH = "songs.json"

def load_songs():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

async def handle_inline_query(query: types.InlineQuery):
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
