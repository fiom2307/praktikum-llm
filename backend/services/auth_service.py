import json, os
from models.user_model import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/users.json")

def load_users():
    with open(DATA_PATH, "r") as f:
        users_data = json.load(f)
    return [User.from_dict(u) for u in users_data]


def find_user(username):
    users = load_users()

    for user in users:
        if user.username == username:
            return user.to_dict()
    return None


