import json
import os

DB_PATH = "songs.json"

def load_songs():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as db_file:
            json.dump([], db_file)
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

def save_songs(songs):
    with open(DB_PATH, "w", encoding="utf-8") as db_file:
        json.dump(songs, db_file, indent=4, ensure_ascii=False)

def add_song(title, singer, file_id, duration, channel, message_id):
    songs = load_songs()
    song_data = {
        "title": title,
        "singer": singer,
        "file_id": file_id,
        "duration": duration,
        "channel": channel,
        "message_id": message_id
    }
    songs.append(song_data)
    save_songs(songs)