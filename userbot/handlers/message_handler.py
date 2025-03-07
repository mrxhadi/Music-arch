import asyncio
import os
from telethon.tl.types import DocumentAttributeAudio
from database.songs_db import load_songs, add_song

GROUP_ID = int(os.getenv("GROUP_ID"))

async def handle_new_song(event, client):
    message = event.message

    if not message.audio:
        return  # اگر پیام آهنگ نبود، خروج

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

    # جلوگیری از تکراری بودن
    songs = load_songs()
    if any(song["message_id"] == message_id and song["channel"] == channel_username for song in songs):
        print(f"[USERBOT] Duplicate song ignored: {title}")
        return

    # فوروارد آهنگ بدون کپشن
    await client.send_file(
        entity=event.chat_id,
        file=message.media,
        caption="",
    )

    # حذف پیام اصلی
    await asyncio.sleep(0.5)
    await message.delete()

    # ارسال آهنگ به گروه مشترک برای استفاده Inlinebot
    await client.send_file(
        entity=GROUP_ID,
        file=message.media,
        caption=f"{title} - {singer}"
    )

    # ثبت در دیتابیس
    add_song(title, singer, file_id, duration, channel_username, message_id)
    print(f"[USERBOT] New song saved and forwarded: {title} - {singer}")
