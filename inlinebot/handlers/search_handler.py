from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.user_db import get_user_language
from utils.search import search_songs

router = Router()

# تعریف استیت‌های مورد نیاز برای FSM
class SearchStates(StatesGroup):
    awaiting_search_query = State()
    awaiting_category_selection = State()
    awaiting_song_selection = State()

@router.message(F.text == "/search")
async def search_command_handler(message: Message, state: FSMContext):
    """Handle the /search command."""
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    texts = {
        "en": "Send the name of a song or artist:",
        "fa": "نام آهنگ یا خواننده را ارسال کنید:"
    }

    await message.answer(texts.get(lang, texts["en"]))
    await state.set_state(SearchStates.awaiting_search_query)

@router.message(F.text, StateFilter(SearchStates.awaiting_search_query))
async def process_search_query(message: Message, state: FSMContext):
    """Process the search query and return results."""
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    query = message.text.strip()

    texts = {
        "en": {
            "select_category": "Choose a category:",
            "artists": "Artists",
            "songs": "Songs",
            "no_results": "No results found.",
        },
        "fa": {
            "select_category": "دسته‌بندی مورد نظر را انتخاب کنید:",
            "artists": "خواننده‌ها",
            "songs": "آهنگ‌ها",
            "no_results": "نتیجه‌ای یافت نشد.",
        }
    }

    song_results = search_songs(query, search_by="title")
    artist_results = search_songs(query, search_by="singer")

    if not song_results and not artist_results:
        await message.answer(texts[lang]["no_results"])
        return

    await state.update_data(song_results=song_results, artist_results=artist_results)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{texts[lang]['songs']} ✅", callback_data="search_songs")],
            [InlineKeyboardButton(text=texts[lang]['artists'], callback_data="search_artists")]
        ]
    )

    await message.answer(texts[lang]["select_category"], reply_markup=keyboard)
    await state.set_state(SearchStates.awaiting_category_selection)

@router.callback_query(F.data.in_(["search_songs", "search_artists"]), StateFilter(SearchStates.awaiting_category_selection))
async def category_selection_callback(call: CallbackQuery, state: FSMContext):
    """Handle category selection."""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    data = await state.get_data()

    texts = {
        "en": {
            "choose_song": "Select a song:",
            "choose_artist": "Select an artist:",
            "no_results": "No results available.",
        },
        "fa": {
            "choose_song": "یک آهنگ انتخاب کنید:",
            "choose_artist": "یک خواننده انتخاب کنید:",
            "no_results": "نتیجه‌ای در دسترس نیست.",
        }
    }

    if call.data == "search_songs":
        results = data.get("song_results", [])
        prompt_text = texts[lang]["choose_song"]
    else:
        results = data.get("artist_results", [])
        prompt_text = texts[lang]["choose_artist"]

    if not results:
        await call.message.answer(texts[lang]["no_results"])
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=song["title"], callback_data=f"song_{song['message_id']}")]
                         for song in results]
    )

    await call.message.answer(prompt_text, reply_markup=keyboard)
    await state.set_state(SearchStates.awaiting_song_selection)

@router.callback_query(F.data.startswith("song_"), StateFilter(SearchStates.awaiting_song_selection))
async def song_selection_callback(call: CallbackQuery, state: FSMContext):
    """Send the selected song to the user."""
    message_id = call.data.replace("song_", "")
    user_id = call.from_user.id
    lang = get_user_language(user_id)

    texts = {
        "en": "Here is your requested song:",
        "fa": "آهنگ درخواستی شما:",
    }

    songs = search_songs("", search_by="title")
    song = next((s for s in songs if str(s["message_id"]) == message_id), None)

    if not song:
        await call.message.answer(texts[lang] + " ❌")
        return

    await call.message.answer_audio(song["file_id"], caption=f"{song['title']} - {song['singer']}")
    await state.clear()
