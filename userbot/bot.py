import asyncio
import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from database.songs_db import add_song, load_songs
from handlers.message_handler import handle_new_song
from handlers.admin_handler import handle_admin_commands
from scheduler.nightly_job import start_nightly_job

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

client = TelegramClient('bot', API_ID, API_HASH)

@client.on(events.NewMessage)
async def new_message_handler(event):
    await handle_new_song(event, client)

@client.on(events.NewMessage(from_users=ADMIN_ID))
async def admin_commands_handler(event):
    await handle_admin_commands(event, client)

async def main():
    await client.start()
    print("Userbot is running...")
    start_nightly_job(client)  # اصلاح شده: بدون await
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
