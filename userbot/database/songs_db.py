import os
import json
import asyncio

DB_PATH = "songs.json"
INLINEBOT_ID = int(os.getenv("INLINEBOT_ID"))

# ساخت دیتابیس اگر نبود
def create_db_if_not_exists():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as db_file:
            json.dump([], db_file, ensure_ascii=False, indent=4)

# لود دیتابیس
def load_songs():
    if not os.path.exists(DB_PATH):
        create_db_if_not_exists()
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

# افزودن آهنگ جدید و ارسال دیتابیس بعد از 30 دقیقه
def add_song(title, singer, file_id, duration, channel, message_id, client):
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

    # راه‌اندازی تایمر ارسال دیتابیس
    asyncio.create_task(delayed_send_db(client))


async def delayed_send_db(client):
    await asyncio.sleep(1800)  # 1800 ثانیه = 30 دقیقه
    try:
        await client.send_file(
            INLINEBOT_ID,
            DB_PATH,
            caption="Updated songs.json database."
        )
        print("Database sent to Inlinebot successfully.")
    except Exception as e:
        print(f"Error sending database to Inlinebot: {e}")


# حذف آهنگ از دیتابیس با message_id و channel
def remove_song(message_id, channel):
    songs = load_songs()
    updated_songs = [song for song in songs if not (song["message_id"] == message_id and song["channel"] == channel)]
    with open(DB_PATH, "w", encoding="utf-8") as db_file:
        json.dump(updated_songs, db_file, ensure_ascii=False, indent=4)
    print(f"Song with message_id {message_id} from channel {channel} removed from database.")
