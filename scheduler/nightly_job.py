import os
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from database.songs_db import load_songs
from dotenv import load_dotenv

load_dotenv()
CHANNEL_1111 = os.getenv("CHANNEL_1111")

async def send_nightly_songs(client):
    songs = load_songs()
    if len(songs) < 3:
        print("Not enough songs to send.")
        return

    selected_songs = random.sample(songs, 3)

    for song in selected_songs:
        await client.send_file(
            entity=CHANNEL_1111,
            file=song["file_id"],
        )

async def start_nightly_job(client):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_nightly_songs,
        "cron",
        hour=23,
        minute=11,
        args=[client]
    )
    scheduler.start()