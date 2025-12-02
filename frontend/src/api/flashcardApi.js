import { API_BASE_URL } from "./config";

export async function saveFlashcard(word, definition = "") {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/flashcards/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ word, definition })
    });

    return response.json();
}

export async function getFlashcards() {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/flashcards/${userId}`);

    const data = await response.json();
    return data.flashcards;
}