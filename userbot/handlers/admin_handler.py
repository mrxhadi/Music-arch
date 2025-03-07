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

    # اگر فایل ارسال شد
    if event.document:
        if event.document.file_name == "songs.json":
            await event.download_media(file=DB_PATH)
            songs = load_songs()
            print(f"[USERBOT] Database updated with {len(songs)} songs.")
            await event.reply(f"Database updated with {len(songs)} songs.")
        else:
            await event.reply("Invalid file. Please send only the 'songs.json' file.")
        return  # برگشت برای جلوگیری از ادامه اجرای کد

    # اگر متن پیام None بود (فقط فایل بود)، دیگه ادامه نده
    if not event.text:
        return

    # دستورات متنی
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

    print("[USERBOT] Unknown command received.")
    await event.reply("Unknown command.")
