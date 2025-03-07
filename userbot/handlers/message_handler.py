import asyncio
import os
from telethon.tl.types import DocumentAttributeAudio
from database.songs_db import load_songs, add_song, remove_song

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
    chat_id = event.chat_id
    message_id = message.id

    songs = load_songs()
    duplicate = next(
        (song for song in songs if song["title"] == title and song["channel_id"] == chat_id),
        None
    )

    if duplicate:
        print(f"[USERBOT] Duplicate found in chat {chat_id}: {title}. Removing old message and updating database.")
        try:
            await client.delete_messages(
                entity=chat_id,
                message_ids=duplicate["message_id"]
            )
            print(f"[USERBOT] Old message {duplicate['message_id']} deleted.")
        except Exception as e:
            print(f"[USERBOT] Failed to delete old message: {e}")
        remove_song(duplicate["message_id"], chat_id)

    # فوروارد آهنگ بدون کپشن در چنل اصلی
    await client.send_file(
        entity=chat_id,
        file=message.media,
        caption="",
    )

    await asyncio.sleep(0.5)
    await message.delete()

    # ارسال آهنگ به گروه مشترک (بدون کپشن)
    await client.send_file(
        entity=GROUP_ID,
        file=message.media,
        caption=""
    )

    # ثبت آهنگ در دیتابیس
    add_song(title, singer, file_id, duration, chat_id, message_id)
    print(f"[USERBOT] Song processed and added to DB: {title} - {singer}")
