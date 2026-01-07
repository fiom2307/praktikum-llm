import { API_BASE_URL } from "./config";

export async function correctText(userText, exerciseId) {
    const userId = localStorage.getItem("userId");
    
    const response = await fetch(`${API_BASE_URL}/correct_text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId: userId, text: userText , exerciseId: exerciseId}),
    });
    const data = await response.json();
    return data;
};

export async function createWritingText(cityKey = null) {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/fetch_writing_text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            userId: userId,
            cityKey: cityKey,
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to create writing text");
    }

    const data = await response.json();
    return data;
}

