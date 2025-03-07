import os
from dotenv import load_dotenv
from database.songs_db import load_songs
from handlers.rebuild_handler import rebuild_database

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DB_PATH = "songs.json"

async def handle_admin_commands(event, client):
    print(f"[USERBOT] Received command or file from {event.sender_id}")

    if event.sender_id != ADMIN_ID:
        await event.reply("You are not authorized.")
        return

    # بررسی ارسال فایل دیتابیس
    if event.document:
        if event.document.attributes and event.document.attributes[0].file_name == "songs.json":
            await event.download_media(file=DB_PATH)
            songs = load_songs()
            print(f"[USERBOT] Database updated with {len(songs)} songs.")
            await event.reply(f"Database updated with {len(songs)} songs.")
        else:
            await event.reply("Invalid file. Please send the 'songs.json' file.")
        return

    # دستور ارسال دیتابیس
    if event.text == "/list":
        print("[USERBOT] Processing '/list' command...")
        if os.path.exists(DB_PATH):
            await event.reply("Here is the songs database:", file=DB_PATH)
        else:
            print("[USERBOT] Database file not found.")
            await event.reply("Database file not found.")
        return

    # دستور بازسازی دیتابیس
    if event.text == "/rebuild":
        print("[USERBOT] Processing '/rebuild' command...")
        await event.reply("Rebuilding the database, please wait...")
        await rebuild_database(client, event)
        return

    # اگر نه فایل بود و نه دستور معتبر
    print("[USERBOT] Unknown command received.")
    await event.reply("Unknown command.")
