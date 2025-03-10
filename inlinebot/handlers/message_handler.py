from aiogram import types
from database.songs_db import add_song

async def handle_new_song(message: types.Message):
    if message.audio:
        title = message.audio.title or "Unknown Title"
        singer = message.audio.performer or "Unknown Singer"
        duration = message.audio.duration or 0
        file_id = message.audio.file_id
    elif message.document:
        if 'audio' in message.document.mime_type:
            attr = message.document.attributes[0]
            title = getattr(attr, "title", "Unknown Title")
            singer = getattr(attr, "performer", "Unknown Singer")
            duration = getattr(attr, "duration", 0)
            file_id = message.document.file_id
        else:
            print("[GROUP] Non-audio document ignored.")
            return
    else:
        print("[GROUP] Message is not audio or document.")
        return

    channel_username = message.chat.username or "Private Group"
    message_id = message.message_id

    add_song(title, singer, file_id, duration, channel_username, message_id)
    print(f"[GROUP] New song added: {title} by {singer}")
    
