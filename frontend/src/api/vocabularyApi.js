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

export async function checkWord(word, clues, answer, attempt) {
  const userId = localStorage.getItem("userId");

  const response = await fetch(`${API_BASE_URL}/check_word`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userId: userId, word: word, clues: clues, answer: answer, attempt: attempt}),
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