import os
import json

DB_PATH = "songs.json"

# ساخت دیتابیس اگر وجود نداشت
def create_db_if_not_exists():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as db_file:
            json.dump([], db_file, ensure_ascii=False, indent=4)

# بارگذاری دیتابیس
def load_songs():
    if not os.path.exists(DB_PATH):
        create_db_if_not_exists()
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

# افزودن آهنگ جدید به دیتابیس
def add_song(title, singer, file_id, duration, channel, message_id):
    songs = load_songs()
    songs.append({
        "title": title,
        "singer": singer,
        "file_id": file_id,
        "duration": duration,
        "channel": channel,
        "message_id": message_id
    })
    with open(DB_PATH, "w", encoding="utf-8") as db_file:
        json.dump(songs, db_file, ensure_ascii=False, indent=4)
