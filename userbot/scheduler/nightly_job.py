import os
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.songs_db import load_songs

CHANNEL_1111 = os.getenv("CHANNEL_1111")

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

async def handle_nightly_command(event, client):
    """ اجرای دستی نایتلی جاب با دستور /nightly """
    if event.sender_id == int(os.getenv("ADMIN_ID")):
        await event.reply("Running nightly job now...")
        await send_nightly_songs(client)
    else:
        await event.reply("You are not authorized to use this command.")

def start_nightly_job(client):
    scheduler = AsyncIOScheduler(timezone="Asia/Tehran")
    
    # ارسال ۳ آهنگ رندوم در ساعت ۱۱:۱۱ شب
    scheduler.add_job(
        send_nightly_songs,
        trigger="cron",
        hour=23,
        minute=11,
        args=[client],
        id="nightly_songs_job"
    )

    scheduler.start()
