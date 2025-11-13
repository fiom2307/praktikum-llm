from services.user_service import load_users

def authenticate_user(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                return user
            else:
                return None
            
    return None


