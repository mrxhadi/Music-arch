import json
import difflib

DB_PATH = "songs.json"

def load_songs():
    """Load songs from the database."""
    with open(DB_PATH, "r", encoding="utf-8") as db_file:
        return json.load(db_file)

def find_best_matches(query, items, key, limit=5, threshold=0.7):
    """Find best matching items from a list using similarity ratio."""
    matches = []
    
    for item in items:
        similarity = difflib.SequenceMatcher(None, query.lower(), item[key].lower()).ratio()
        if similarity >= threshold:
            matches.append((item, similarity))
    
    matches.sort(key=lambda x: x[1], reverse=True)  # Sort by highest similarity
    
    return [match[0] for match in matches[:limit]]

def search_songs(query, search_by="title"):
    """Search for songs by title or artist."""
    songs = load_songs()
    
    if search_by == "title":
        results = find_best_matches(query, songs, "title")
    else:
        results = find_best_matches(query, songs, "singer")
    
    return results
