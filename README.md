
# **Looking for me?**  
## **Find me here: [t.me/@Im_Solaire](https://t.me/Im_Solaire)**  

---

# **Userbot & InlineBot Song Archiver**

A complete Telegram bot system designed to manage, archive, and serve songs across multiple channels using both a **Userbot (Telethon)** and an **InlineBot (Aiogram)**.

---

## **Features**

### Userbot (Telethon):
- Automatically detects and processes new songs in specific channels.
- Removes duplicate songs based on title and channel.
- Forwards new songs to a shared group for inline access.
- Supports `/list` command to send the latest database.
- Supports `/rebuild` command to rebuild the entire database from all joined channels (excluding the shared group).
- Deletes songs from the database when removed from original channels.

### InlineBot (Aiogram):
- Allows users to search songs via inline queries.
- Provides instant access to archived songs from the database.
- Supports `/list` command to get the latest database file.
- Supports manual database updates via file upload (`songs.json`).

---

## **Tech Stack**
- **Userbot**: [Telethon](https://github.com/LonamiWebs/Telethon)
- **InlineBot**: [Aiogram v3](https://github.com/aiogram/aiogram)
- **Database**: JSON (`songs.json`)

---

## **Installation**

### 1. Clone the repository:
```bash
git clone https://github.com/YourUsername/YourRepo.git
cd YourRepo
```

### 2. Install dependencies:
For **Userbot**:
```bash
pip install -r requirements_userbot.txt
```
For **InlineBot**:
```bash
pip install -r requirements_inlinebot.txt
```

---

## **Environment Variables**

Set the following environment variables in your **Railway** project:

#### Userbot:
```env
API_ID=your_api_id
API_HASH=your_api_hash
ADMIN_ID=your_admin_id
GROUP_ID=-100xxxxxxxxxx
SESSION_STRING=your_generated_string
```

#### InlineBot:
```env
BOT_TOKEN=your_bot_token
ADMIN_ID=your_admin_id
GROUP_ID=-100xxxxxxxxxx
```

---

## **How to Generate SESSION_STRING**

Run this in your local environment (like Termux or any Python environment):

```python
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
```

---

## **Database Structure (`songs.json`)**
```json
[
  {
    "title": "Song Name",
    "singer": "Artist",
    "file_id": "FILE_ID_HERE",
    "duration": 240,
    "channel_id": -1001234567890,
    "message_id": 123
  }
]
```

---

## **Notes**
- **Userbot** uses `SESSION_STRING` to avoid file-based sessions.
- Database is shared between **Userbot** and **InlineBot**.
- The shared group (`GROUP_ID`) acts as the media source for the inline mode.
- Duplicate handling is based on **title** and **channel_id**.
- Remove sensitive files (`.session`, `songs.json`, etc.) before making the repo public.

---

# **Looking for me?**  
## **Find me here: [t.me/@Im_Solaire](https://t.me/Im_Solaire)**  
