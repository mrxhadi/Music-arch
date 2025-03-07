import os
from database.songs_db import load_songs

DB_PATH = "songs.json"

async def handle_admin_commands(event):
    if event.text == "/list":
        if os.path.exists(DB_PATH):
            await event.reply("Here is the songs database:", file=DB_PATH)
        else:
            await event.reply("Database file not found.")

    elif event.file and event.file.name == "songs.json":
        await event.download_media(file=DB_PATH)
        songs = load_songs()
        await event.reply(f"Database updated with {len(songs)} songs.")

    else:
        await event.reply("Unknown command.")
