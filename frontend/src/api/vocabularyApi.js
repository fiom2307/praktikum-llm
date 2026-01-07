import { API_BASE_URL } from "./config";

export async function generateWordAndClues(cityKey = null) {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/generate_word_and_clues`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({userId: userId, cityKey: cityKey}),
    });
    const data = await response.json();
    return data;
};

export async function checkWord(word, clues, exerciseId, answer, attempt) {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/check_word`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId: userId, word: word, exerciseId: exerciseId, clues: clues, answer: answer, attempt: attempt}),
    });
    const data = await response.json();
    return data;
};

export async function getLastVocabularyEntry() {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/vocabulary/last/${userId}`);

    if (!response.ok) {
        return null;
    }

    const data = await response.json();
    return data;
}

export async function getLastVocabularyEntryFromCity(cityKey) {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/vocabulary/last/${cityKey}/${userId}`);

    if (!response.ok) {
        return null;
    }

    const data = await response.json();
    return data;
}