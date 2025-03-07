from database.songs_db import remove_song

async def handle_deleted_message(event):
    if event.deleted_ids:
        chat_id = event.chat_id
        for msg_id in event.deleted_ids:
            remove_song(msg_id, chat_id)
            print(f"[USERBOT] Removed song with message_id {msg_id} from chat_id {chat_id}")
