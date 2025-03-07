import os
from telethon import events
from database.songs_db import load_songs, save_songs

DB_PATH = "songs.json"

async def handle_admin_commands(event):
    if event.text == "/list":
        await event.reply(file=DB_PATH)

    elif event.file and event.file.name == "songs.json":
        path = await event.download_media(file=DB_PATH)
        songs = load_songs()
        await event.reply(f"Database updated with {len(songs)} songs.")

    else:
        await event.reply("Unknown command.")