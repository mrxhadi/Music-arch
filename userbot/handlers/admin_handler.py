import os
from dotenv import load_dotenv
from database.songs_db import load_songs
from handlers.rebuild_handler import rebuild_database
from scheduler.nightly_job import send_nightly_songs  # ایمپورت تابع ارسال شبانه
from telethon.tl.types import DocumentAttributeFilename

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DB_PATH = "songs.json"

async def handle_admin_commands(event, client):
    print(f"[USERBOT] Received command or file from {event.sender_id}")

    if event.sender_id != ADMIN_ID:
        await event.reply("You are not authorized.")
        return

    # بررسی فایل و نام فایل
    if event.document:
        file_name = None
        for attr in event.document.attributes:
            if isinstance(attr, DocumentAttributeFilename):
                file_name = attr.file_name
                break

        if file_name == "songs.json":
            await event.download_media(file=DB_PATH)
            songs = load_songs()
            print(f"[USERBOT] Database updated with {len(songs)} songs.")
            await event.reply(f"Database updated with {len(songs)} songs.")
            return

    if event.text == "/list":
        print("[USERBOT] Processing '/list' command...")
        if os.path.exists(DB_PATH):
            await event.reply("Here is the songs database:", file=DB_PATH)
        else:
            print("[USERBOT] Database file not found.")
            await event.reply("Database file not found.")
        return

    if event.text == "/rebuild":
        print("[USERBOT] Processing '/rebuild' command...")
        await event.reply("Rebuilding the database, please wait...")
        await rebuild_database(client, event)
        return

    if event.text == "/nightly":
        print("[USERBOT] Manually triggering nightly job...")
        await event.reply("Running nightly job...")
        await send_nightly_songs(client)  # اجرای دستی ارسال شبانه
        return

    print("[USERBOT] Unknown command received.")
    await event.reply("Unknown command.")
