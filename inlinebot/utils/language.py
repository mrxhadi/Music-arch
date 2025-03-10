import json
import os

LANG_DB_PATH = "language_settings.json"

messages = {
    "en": {
        "start": "Welcome! Choose a language:",
        "help": "/search - Search for a song or artist. After sending this command, send the song title or artist name to find relevant results.",
        "search_prompt": "Send the song name or artist:",
        "not_found": "No results found.",
    },
    "fa": {
        "start": "خوش آمدید! لطفاً زبان را انتخاب کنید:",
        "help": "/search - جستجوی آهنگ یا خواننده. پس از ارسال این دستور، نام آهنگ یا خواننده را ارسال کنید تا نتایج مرتبط نمایش داده شود.",
        "search_prompt": "نام آهنگ یا خواننده را ارسال کنید:",
        "not_found": "نتیجه‌ای یافت نشد.",
    }
}

def load_languages():
    """Load user language preferences from file."""
    if not os.path.exists(LANG_DB_PATH):
        return {}
    with open(LANG_DB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_languages(data):
    """Save user language preferences to file."""
    with open(LANG_DB_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_user_language(user_id):
    """Retrieve the preferred language of a user. Defaults to English."""
    languages = load_languages()
    return languages.get(str(user_id), "en")

def set_user_language(user_id, language_code):
    """Set the preferred language for a user."""
    languages = load_languages()
    languages[str(user_id)] = language_code
    save_languages(languages)

def get_message(key, lang="en"):
    """Returns the message in the selected language."""
    return messages.get(lang, messages["en"]).get(key, "Message not found.")
