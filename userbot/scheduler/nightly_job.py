import os
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.songs_db import load_songs

CHANNEL_1111 = os.getenv("CHANNEL_1111")
INLINEBOT_ID = int(os.getenv("INLINEBOT_ID"))
DB_PATH = "songs.json"

async def send_nightly_songs(client):
    songs = load_songs()
    
    if len(songs) < 3:
        print("Not enough songs in the database to send.")
        return

    selected_songs = random.sample(songs, 3)

    for song in selected_songs:
        try:
            await client.send_file(
                CHANNEL_1111,
                file=song["file_id"],
                caption=f'{song["title"]} - {song["singer"]}'
            )
        except Exception as e:
            print(f"Error sending song {song['title']}: {e}")


async def send_database_to_inlinebot(client):
    try:
        await client.send_file(
            INLINEBOT_ID,
            DB_PATH,
            caption="Nightly updated songs.json database."
        )
        print("Nightly database sent successfully to Inlinebot.")
    except Exception as e:
        print(f"Error sending nightly database: {e}")


def start_nightly_job(client):
    scheduler = AsyncIOScheduler(timezone="Asia/Tehran")
    
    # ارسال ۳ آهنگ رندوم
    scheduler.add_job(
        send_nightly_songs,
        trigger="cron",
        hour=23,
        minute=11,
        args=[client],
        id="nightly_songs_job"
    )

    # ارسال دیتابیس برای بات توکن
    scheduler.add_job(
        send_database_to_inlinebot,
        trigger="cron",
        hour=23,
        minute=12,
        args=[client],
        id="nightly_database_job"
    )

    scheduler.start()
