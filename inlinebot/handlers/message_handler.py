import os
from aiogram import types
from database.songs_db import load_songs, add_song

GROUP_ID = int(os.getenv("GROUP_ID"))

async def handle_new_song(message: types.Message):
    if message.chat.id != GROUP_ID:
        return

    document = message.document
    if not document:
        return  # اگر پیام اصلاً داکیومنت نبود، خروج

    # بررسی اینکه داکیومنت، آهنگ است
    audio_attr = next(
        (attr for attr in document.attributes if attr.type == "audio"),
        None
    )
    if not audio_attr:
        return  # اگه داکیومنت، آهنگ نبود خروج

    title = audio_attr.title or "Unknown Title"
    singer = audio_attr.performer or "Unknown Singer"
    duration = audio_attr.duration or 0
    file_id = document.file_id

    # جلوگیری از ثبت تکراری بر اساس file_id
    songs = load_songs()
    if any(song["file_id"] == file_id for song in songs):
        print(f"[INLINEBOT] Duplicate song ignored: {title}")
        return

    add_song(title, singer, file_id, duration)
    print(f"[INLINEBOT] New song added to database: {title} - {singer}")
