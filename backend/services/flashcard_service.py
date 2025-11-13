from services.user_service import get_user, update_user

def save_flashcard(username, word):
    user = get_user(username)
    if not user:
        return None
    
    if "flashcards" not in user or user["flashcards"] is None:
        user["flashcards"] = []

    # for duplicates
    for card in user["flashcards"]:
        if card["word"] == word:
            return card
    
    new_card = { "word": word }
    user["flashcards"].append(new_card)

    update_user(user)
    return new_card

def get_flashcards(username):
    user = get_user(username)
    if not user:
        return None
    return user.get("flashcards", [])