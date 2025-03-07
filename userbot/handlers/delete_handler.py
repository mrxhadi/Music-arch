from database.songs_db import remove_song

async def handle_deleted_message(event):
    if event.deleted_ids:
        chat = await event.get_chat()
        channel_username = chat.username or "Private Channel"

        for msg_id in event.deleted_ids:
            remove_song(msg_id, channel_username)
            print(f"Removed song with message_id {msg_id} from channel {channel_username}")
