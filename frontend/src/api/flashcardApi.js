import { API_BASE_URL } from "./config";

export async function saveFlashcard(username, word) {
    const response = await fetch(`${API_BASE_URL}/save_flashcard`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, word })
    });
    return response.json();
}

export async function getFlashcards(username) {
    const response = await fetch(`${API_BASE_URL}/get_flashcards`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username})
    });
    return response.json();
}