import { API_BASE_URL } from "./config";


export async function correctAnswers(username, userText, aiGeneratedText) {
    const response = await fetch(`${API_BASE_URL}/correct_answers`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({username: username, generatedText: aiGeneratedText, text: userText}),
    });
    const data = await response.json();
    return data.corrected_answers;
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