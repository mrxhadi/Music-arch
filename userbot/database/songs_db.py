import os
import json

DB_PATH = "songs.json"

def create_db_if_not_exists():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as db_file:
            json.dump([], db_file, ensure_ascii=False, indent=4)

def load_songs():
    if not os.path.exists(DB_PATH):
        create_db_if_not_exists()
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

def add_song(title, singer, file_id, duration, channel_id, message_id):
    songs = load_songs()
    songs.append({
        "title": title,
        "singer": singer,
        "file_id": file_id,
        "duration": duration,
        "channel_id": channel_id,
        "message_id": message_id
    })
    with open(DB_PATH, "w", encoding="utf-8") as db_file:
        json.dump(songs, db_file, ensure_ascii=False, indent=4)
    print(f"[DB] Song added: {title} - {singer}")

def remove_song(message_id, channel_id):
    songs = load_songs()
    updated_songs = [song for song in songs if not (song["message_id"] == message_id and song["channel_id"] == channel_id)]
    with open(DB_PATH, "w", encoding="utf-8") as db_file:
        json.dump(updated_songs, db_file, ensure_ascii=False, indent=4)
    print(f"[DB] Song with message_id {message_id} from channel_id {channel_id} removed.")
