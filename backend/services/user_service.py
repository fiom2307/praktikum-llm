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