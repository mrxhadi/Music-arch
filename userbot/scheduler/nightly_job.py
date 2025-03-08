import os
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.songs_db import load_songs

CHANNEL_1111 = -1002444680520  # آیدی عددی چنل
DB_PATH = "songs.json"

async def send_nightly_songs(client):
    songs = load_songs()

    if len(songs) < 3:
        print("[NIGHTLY JOB] Not enough songs in the database to send.")
        return

    try:
        # تست ارسال پیام ساده برای بررسی دسترسی به چنل
        await client.send_message(CHANNEL_1111, "[NIGHTLY JOB] Test message before sending songs.")
        print("[NIGHTLY JOB] Successfully sent test message. Channel is accessible.")

        selected_songs = random.sample(songs, 3)

        for song in selected_songs:
            try:
                await client.send_file(
                    CHANNEL_1111,
                    file=song["file_id"],
                    caption=f'{song["title"]} - {song["singer"]}'
                )
                print(f"[NIGHTLY JOB] Successfully sent song: {song['title']}")
            except Exception as e:
                print(f"[NIGHTLY JOB] Error sending song {song['title']}: {e}")

    except Exception as e:
        print(f"[NIGHTLY JOB] Cannot access channel {CHANNEL_1111}: {e}")


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
