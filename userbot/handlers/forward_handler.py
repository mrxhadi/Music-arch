import os

X_ARCHIVE_CHANNEL_ID = int(os.getenv("X_ARCHIVE_CHANNEL_ID"))
INLINEBOT_ID = int(os.getenv("INLINEBOT_ID"))

async def handle_forward(event, client):
    # فقط پیام‌های کانال x_archive و فقط آهنگ‌ها
    if event.chat_id != X_ARCHIVE_CHANNEL_ID:
        return
    if not event.message.audio:
        return
    try:
        await client.send_message(
            INLINEBOT_ID,
            event.message
        )
        print(f"[FORWARD] Song {event.message.id} forwarded to Inlinebot.")
    except Exception as e:
        print(f"[ERROR] Failed to forward song {event.message.id}: {e}")
