import os
from database.songs_db import load_songs

DB_PATH = "songs.json"

async def handle_admin_commands(event, client):
    print(f"Received command: {event.text}")  # پرینت برای مشاهده دستور دریافتی

    if event.text == "/list":
        print("Processing '/list' command...")  # پرینت وقتی که دستور '/list' پردازش میشه
        if os.path.exists(DB_PATH):
            print(f"Sending database from: {DB_PATH}")  # پرینت مسیر دیتابیس
            await event.reply("Here is the songs database:", file=DB_PATH)
        else:
            print("Database file not found.")  # پرینت وقتی که دیتابیس پیدا نمی‌شود
            await event.reply("Database file not found.")
    
    elif event.file and event.file.name == "songs.json":
        await event.download_media(file=DB_PATH)
        songs = load_songs()
        print(f"Database updated with {len(songs)} songs.")  # پرینت تعداد آهنگ‌های دیتابیس
        await event.reply(f"Database updated with {len(songs)} songs.")
    else:
        print("Unknown command received.")  # پرینت وقتی دستور ناشناخته دریافت می‌شود
        await event.reply("Unknown command.")
