import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv
from database.songs_db import add_song, load_songs
from handlers.message_handler import handle_new_song
from handlers.admin_handler import handle_admin_commands
from handlers.delete_handler import handle_deleted_message
from scheduler.nightly_job import start_nightly_job
from handlers.rebuild_handler import rebuild_database

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
SESSION_STRING = os.getenv("SESSION_STRING")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


@client.on(events.NewMessage)
async def new_message_handler(event):
    await handle_new_song(event, client)


@client.on(events.NewMessage(from_users=ADMIN_ID))
async def admin_commands_handler(event):
    print(f"[USERBOT] Admin command received from {event.sender_id}")

    # بررسی ارسال فایل دیتابیس
    if event.document and event.file and event.file.name == "songs.json":
        await handle_admin_commands(event, client)
        return

    # بررسی دستورات متنی
    if event.text == "/list":
        await handle_admin_commands(event, client)
    elif event.text == "/rebuild":
        await rebuild_database(client, event)
    else:
        await event.reply("Unknown command.")


@client.on(events.MessageDeleted())
async def deleted_message_handler(event):
    await handle_deleted_message(event)


async def main():
    await client.start()
    print("Userbot is running...")
    start_nightly_job(client)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
