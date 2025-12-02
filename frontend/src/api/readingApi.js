import { API_BASE_URL } from "./config";


export async function correctAnswers(userText, aiGeneratedText) {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/correct_answers`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({userId: userId, generatedText: aiGeneratedText, text: userText}),
    });
    const data = await response.json();
    return data;
};

export async function createReadingText() {
    const response = await fetch(`${API_BASE_URL}/create_reading_text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
    });
    const data = await response.json();
    return data.reading_text;
};