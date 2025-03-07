import os
import json

DB_PATH = "songs.json"

# ساخت دیتابیس اگر نبود
def create_db_if_not_exists():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as db_file:
            json.dump([], db_file, ensure_ascii=False, indent=4)
        print(f"[DB] Created a new database at {DB_PATH}")

# لود دیتابیس
def load_songs():
    create_db_if_not_exists()  # چک می‌کنیم که دیتابیس وجود داشته باشد
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

# افزودن آهنگ جدید
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

    print(f"[INLINEBOT] Song added to DB: {title} by {singer}")
