from datetime import datetime
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/users.json")

def load_users():
    with open(DATA_PATH, "r") as f:
        return json.load(f)
    
def save_users(users):
    with open(DATA_PATH, "w") as f:
        json.dump(users, f, indent=4)
    
def get_user(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None

def update_user(updated_user):
    users = load_users()
    for i, user in enumerate(users):
        if user["username"] == updated_user["username"]:
            users[i] = updated_user
            save_users(users)
            return updated_user
    return None

def add_history_entry(username: str, module: str, details: dict):
    """
    add the user history and save it in users.json。
    
    :param username: username
    :param module:  ('reading', 'vocabulary', 'writing')
    :param details: activity details
    """
    updated_user = get_user(username)
    if not updated_user:
        return False

    if "history" not in updated_user:
        updated_user["history"] = []
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "module": module,
        "details": details
    }
    
    updated_user["history"].append(entry)
    
    result = update_user(updated_user)
    return result is not None

def add_user(username, password):
    users = load_users()

    new_user = {
        "username": username,
        "password": password,
        "pizzaCount": 0,
        "history": [],
        "currentVocabulary": {
            "word": "",
            "clues": [],
            "attempts": 0,
            "completed": False
        },
        "flashcards": []
    }

    users.append(new_user)
    save_users(users)

    return new_user
