import json
import os

DB_PATH = "user_data.json"

def load_users():
    """بارگذاری دیتابیس کاربران از فایل JSON"""
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_users(users):
    """ذخیره دیتابیس کاربران در فایل JSON"""
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

def set_user_language(user_id: int, language: str):
    """تنظیم زبان انتخابی کاربر و ذخیره آن در دیتابیس JSON"""
    users = load_users()
    users[str(user_id)] = language  # کلید باید رشته باشد
    save_users(users)

def get_user_language(user_id: int) -> str:
    """دریافت زبان انتخابی کاربر، پیش‌فرض انگلیسی اگر انتخاب نکرده باشد"""
    users = load_users()
    return users.get(str(user_id), "en")  # پیش‌فرض انگلیسی
