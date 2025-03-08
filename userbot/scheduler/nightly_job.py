import os
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.songs_db import load_songs

CHANNEL_1111 = os.getenv("CHANNEL_1111")  # آیدی عددی کانال
DB_PATH = "songs.json"
FALLBACK_USERNAME = "elevenhtg"  # یوزرنیم کانال در صورت مشکل با آیدی عددی

async def send_nightly_songs(client):
    songs = load_songs()

    if len(songs) < 3:
        print("[NIGHTLY JOB] Not enough songs in the database to send.")
        return

    selected_songs = random.sample(songs, 3)

    for song in selected_songs:
        try:
            # تست دریافت آیدی عددی
            try:
                entity = await client.get_input_entity(CHANNEL_1111)
            except Exception as e:
                print(f"[NIGHTLY JOB] Failed to get entity by ID {CHANNEL_1111}, trying username... Error: {e}")
                entity = await client.get_input_entity(FALLBACK_USERNAME)

            print(f"[NIGHTLY JOB] Sending to channel: {entity}")

            await client.send_file(
                entity,
                file=song["file_id"],
                caption=f'{song["title"]} - {song["singer"]}'
            )
        except Exception as e:
            print(f"[NIGHTLY JOB] Error sending song {song['title']}: {e}")


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

    scheduler.start()
