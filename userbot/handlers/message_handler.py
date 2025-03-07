import asyncio
import os
from telethon.tl.types import DocumentAttributeAudio
from database.songs_db import load_songs, add_song, remove_song

GROUP_ID = int(os.getenv("GROUP_ID"))

async def handle_new_song(event, client):
    message = event.message

    if not message.audio:
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

    file_id = audio.file_reference.hex()
    channel = await event.get_chat()
    channel_username = channel.username or "Private Channel"
    message_id = message.id

    songs = load_songs()
    duplicate = next((song for song in songs if song["title"] == title and song["channel"] == channel_username), None)

    if duplicate:
        print(f"[USERBOT] Duplicate found: {title}. Removing old message and updating database.")
        # حذف پیام قبلی از چنل اصلی
        try:
            await client.delete_messages(entity=event.chat_id, message_ids=duplicate["message_id"])
        except Exception as e:
            print(f"[USERBOT] Failed to delete old message: {e}")
        # حذف آهنگ قبلی از دیتابیس
        remove_song(duplicate["message_id"], channel_username)

    # فوروارد آهنگ بدون کپشن
    await client.send_file(
        entity=event.chat_id,
        file=message.media,
        caption="",
    )

    # حذف پیام اصلی
    await asyncio.sleep(0.5)
    await message.delete()

    # اگر آهنگ جدید بود، به گروه مشترک بفرست
    if not duplicate:
        await client.send_file(
            entity=GROUP_ID,
            file=message.media,
            caption=f"{title} - {singer}"
        )

    # ثبت در دیتابیس
    add_song(title, singer, file_id, duration, channel_username, message_id)
    print(f"[USERBOT] Song processed: {title} - {singer}")
