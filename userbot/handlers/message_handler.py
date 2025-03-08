import asyncio
import os
from telethon.tl.types import DocumentAttributeAudio
from database.songs_db import load_songs, add_song, remove_song

GROUP_ID = int(os.getenv("GROUP_ID"))
CHANNEL_1111 = int(os.getenv("CHANNEL_1111"))  
EXCLUDED_CHANNELS = {GROUP_ID, CHANNEL_1111}  

async def handle_new_song(event, client):
    message = event.message
    channel_id = event.chat_id  # ذخیره کردن به‌عنوان channel_id

    if not message.audio:
        return  

    if channel_id in EXCLUDED_CHANNELS:
        print(f"[USERBOT] Ignoring message from excluded channel {channel_id}")
        return

    audio = message.document
    title = "Unknown Title"
    singer = "Unknown Singer"
    duration = 0

    for attr in audio.attributes:
        if isinstance(attr, DocumentAttributeAudio):
            title = attr.title or title
            singer = attr.performer or singer
            duration = attr.duration or duration

    message_id = message.id  

    songs = load_songs()
    duplicate = next(
        (song for song in songs if song["title"] == title and song["channel_id"] == channel_id),
        None
    )

    if duplicate:
        print(f"[USERBOT] Duplicate found in chat {channel_id}: {title}. Removing old message and updating database.")
        try:
            await client.delete_messages(channel_id, duplicate["message_id"])
            print(f"[USERBOT] Old message {duplicate['message_id']} deleted.")
        except Exception as e:
            print(f"[USERBOT] Failed to delete old message: {e}")
        remove_song(duplicate["message_id"], channel_id)

    await client.send_file(
        channel_id,
        message.media,
        caption=""
    )

    await asyncio.sleep(0.5)
    await message.delete()

    await client.send_file(
        GROUP_ID,
        file=message.media,
        caption=""
    )

    add_song(title, singer, None, duration, channel_id, message_id)  
    print(f"[USERBOT] Song processed and added to DB: {title} - {singer}")
