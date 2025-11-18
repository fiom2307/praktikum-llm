import { API_BASE_URL } from "./config";

export async function generateWordAndClues() {
    const response = await fetch(`${API_BASE_URL}/generate_word_and_clues`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
    });
    const data = await response.json();
    return data;
};

export async function checkWord(username, word, clues, answer) {
    const response = await fetch(`${API_BASE_URL}/check_word`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, word: word, clues: clues, answer: answer}),
    });
    const data = await response.json();
    return data;
};

export async function getCurrentVocabulary(username) {
  const response = await fetch(`${API_BASE_URL}/get_current_vocabulary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  });
  return response.json();
}

export async function saveCurrentVocabulary(username, word, clues, attempts, completed) {
  const response = await fetch(`${API_BASE_URL}/save_current_vocabulary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, word, clues, attempts, completed })
  });
  return response.json();
}