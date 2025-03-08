import os
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.songs_db import load_songs
from telethon.errors import ChannelPrivateError, PeerIdInvalidError

CHANNEL_1111 = int(os.getenv("CHANNEL_1111"))

async def send_nightly_songs(client):
    songs = load_songs()

    if len(songs) < 3:
        print("[NIGHTLY JOB] Not enough songs in the database to send.")
        return

    selected_songs = random.sample(songs, 3)

    for song in selected_songs:
        try:
            channel_id = song["channel_id"]
            message_id = song["message_id"]

            # تست گرفتن اطلاعات چنل
            try:
                entity = await client.get_entity(channel_id)
            except (ValueError, PeerIdInvalidError):
                print(f"[NIGHTLY JOB] Failed to get entity for channel {channel_id}. Refreshing cache...")
                await client.get_dialogs()  # ریفرش لیست چنل‌ها
                await asyncio.sleep(2)  # تاخیر کوتاه برای جلوگیری از ریکوئست زیاد
                try:
                    entity = await client.get_entity(channel_id)
                except Exception:
                    print(f"[NIGHTLY JOB] Still cannot get entity for {channel_id}. Skipping...")
                    continue

            # دریافت پیام آهنگ
            try:
                message = await client.get_messages(entity, ids=message_id)
            except ChannelPrivateError:
                print(f"[NIGHTLY JOB] Channel {channel_id} is private. Skipping song {song['title']}.")
                continue
            except Exception as e:
                print(f"[NIGHTLY JOB] Error retrieving song {song['title']}: {e}")
                continue

            if not message or not message.audio:
                print(f"[NIGHTLY JOB] Message {message_id} in {channel_id} is not an audio. Skipping...")
                continue

            await client.send_file(
                CHANNEL_1111,
                file=message.media,
                caption=f'{song["title"]} - {song["singer"]}'
            )
            print(f"[NIGHTLY JOB] Successfully sent {song['title']}.")

        except Exception as e:
            print(f"[NIGHTLY JOB] Unexpected error sending song {song['title']}: {e}")

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
