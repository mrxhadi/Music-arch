import os
import json
import asyncio
from telethon.tl.types import DocumentAttributeAudio

GROUP_ID = int(os.getenv("GROUP_ID"))

async def rebuild_database(client, event):
    print("[USERBOT] Starting database rebuild...")
    songs = []

    dialogs = await client.get_dialogs()
    
    for dialog in dialogs:
        if not dialog.is_channel:
            continue
        if dialog.entity.id == GROUP_ID:
            print(f"[USERBOT] Skipping group ID: {GROUP_ID}")
            continue

        print(f"[USERBOT] Processing channel ID: {dialog.entity.id}")

        async for message in client.iter_messages(dialog.id, limit=1000):
            if message.audio:
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
                channel_id = dialog.entity.id
                message_id = message.id

                songs.append({
                    "title": title,
                    "singer": singer,
                    "file_id": file_id,
                    "duration": duration,
                    "channel": channel_id,  # اینجا به جای "channel_id"
                    "message_id": message_id
                })

                await asyncio.sleep(0.2)

        await asyncio.sleep(2)

    with open("songs.json", "w", encoding="utf-8") as db_file:
        json.dump(songs, db_file, ensure_ascii=False, indent=4)

    await event.reply(f"Database rebuild complete! {len(songs)} songs added.")
    print(f"[USERBOT] Database rebuild complete with {len(songs)} songs.")
