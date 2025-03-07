from telethon import events
from database.songs_db import load_songs

async def handle_inline_query(event):
    query = event.text.lower()
    results = []
    songs = load_songs()

    for song in songs:
        if query in song["title"].lower() or query in song["singer"].lower():
            results.append(
                {
                    "type": "article",
                    "title": song["title"],
                    "description": f"{song['singer']} - {song['duration']} sec",
                    "input_message_content": {
                        "message_text": f"{song['title']} by {song['singer']}"
                    }
                }
            )

    await event.answer(results, cache_time=1)
