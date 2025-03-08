import os
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.songs_db import load_songs

CHANNEL_1111 = int(os.getenv("CHANNEL_1111"))

async def send_nightly_songs(client):
    songs = load_songs()

    if len(songs) < 3:
        print("[NIGHTLY JOB] Not enough songs in the database to send.")
        return

    selected_songs = random.sample(songs, 3)

    for song in selected_songs:
        try:
            message = await client.get_messages(song["channel_id"], ids=song["message_id"])
            if message and message.media:
                await client.send_file(
                    CHANNEL_1111,
                    file=message.media,
                    caption=f'{song["title"]} - {song["singer"]}'
                )
                print(f"[NIGHTLY JOB] Sent song: {song['title']}")
            else:
                print(f"[NIGHTLY JOB] No media found in message {song['message_id']}")
        except Exception as e:
            print(f"[NIGHTLY JOB] Error retrieving song {song['title']}: {e}")


def start_nightly_job(client):
    scheduler = AsyncIOScheduler(timezone="Asia/Tehran")

    scheduler.add_job(
        send_nightly_songs,
        trigger="cron",
        hour=23,
        minute=11,
        args=[client],
        id="nightly_songs_job"
    )

    scheduler.start()
