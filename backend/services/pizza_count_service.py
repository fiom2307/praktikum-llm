from services.user_service import load_users, save_users

def increment_pizza_count(username, inc):
    users = load_users()

    for u in users:
        if u["username"] == username:
            u["pizzaCount"] = u.get("pizzaCount", 0) + inc
            save_users(users)
            return u["pizzaCount"]

    return None
