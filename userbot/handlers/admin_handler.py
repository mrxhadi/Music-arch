import os
from handlers.rebuild_handler import rebuild_database
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def handle_admin_commands(event, client):
    print(f"Received command: {event.text}")  

    if event.sender_id != ADMIN_ID:
        await event.reply("You are not authorized.")
        return

    if event.text == "/list":
        print("Processing '/list' command...")
        if os.path.exists(DB_PATH):
            print(f"Sending database from: {DB_PATH}")
            await event.reply("Here is the songs database:", file=DB_PATH)
        else:
            print("Database file not found.")
            await event.reply("Database file not found.")
    
    elif event.text == "/rebuild":
        print("Processing '/rebuild' command...")
        await event.reply("Rebuilding the database, please wait...")
        await rebuild_database(client, event)

    elif event.file and event.file.name == "songs.json":
        await event.download_media(file=DB_PATH)
        songs = load_songs()
        print(f"Database updated with {len(songs)} songs.")
        await event.reply(f"Database updated with {len(songs)} songs.")
    else:
        print("Unknown command received.")
        await event.reply("Unknown command.")
