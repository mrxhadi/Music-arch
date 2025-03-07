import os
from dotenv import load_dotenv
from database.songs_db import load_songs
from handlers.rebuild_handler import rebuild_database

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DB_PATH = "songs.json"

async def handle_admin_commands(event, client):
    sender_id = event.sender_id
    print(f"[USERBOT] Received something from {sender_id}")

    if sender_id != ADMIN_ID:
        await event.reply("You are not authorized.")
        return

    # بررسی ارسال فایل دیتابیس
    if event.file:
        if event.file.name == "songs.json":
            await event.download_media(file=DB_PATH)
            songs = load_songs()
            print(f"[USERBOT] Database updated with {len(songs)} songs.")
            await event.reply(f"Database updated with {len(songs)} songs.")
        else:
            await event.reply("Invalid file. Please send only the 'songs.json' file.")
        return

    # بررسی متن دستورات
    text = event.raw_text.strip()
    print(f"[USERBOT] Command received: {text}")

    if text == "/list":
        print("[USERBOT] Processing '/list' command...")
        if os.path.exists(DB_PATH):
            await event.reply("Here is the songs database:", file=DB_PATH)
        else:
            await event.reply("Database file not found.")
        return

    if text == "/rebuild":
        print("[USERBOT] Processing '/rebuild' command...")
        await event.reply("Rebuilding the database, please wait...")
        await rebuild_database(client, event)
        return

    await event.reply("Unknown command.")
    print("[USERBOT] Unknown command received.")
