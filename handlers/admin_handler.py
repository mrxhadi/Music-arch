import os
import logging
from database.songs_db import load_songs

# تنظیمات لاگینگ
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DB_PATH = "songs.json"

async def handle_admin_commands(event):
    logger.debug(f"Received message: {event.text}")  # چاپ پیام دریافتی

    if event.text == "/list":
        logger.debug("Processing '/list' command...")  # نمایش در حال پردازش دستور '/list'
        if os.path.exists(DB_PATH):
            logger.debug(f"Sending database: {DB_PATH}")  # چاپ مسیر دیتابیس
            await event.reply("Here is the songs database:", file=DB_PATH)
        else:
            logger.debug("Database file not found.")  # نمایش اگر فایل دیتابیس پیدا نشد
            await event.reply("Database file not found.")
    
    elif event.file and event.file.name == "songs.json":
        await event.download_media(file=DB_PATH)
        songs = load_songs()
        logger.debug(f"Database updated with {len(songs)} songs.")  # چاپ تعداد آهنگ‌های دیتابیس
        await event.reply(f"Database updated with {len(songs)} songs.")
    else:
        logger.debug("Unknown command received.")  # چاپ در صورت دریافت دستور ناشناخته
        await event.reply("Unknown command.")
