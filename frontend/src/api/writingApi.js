import { API_BASE_URL } from "./config";

export async function correctText(userText) {
    const response = await fetch(`${API_BASE_URL}/correct_text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userText }),
    });
    const data = await response.json();
    return data.corrected_text;
};