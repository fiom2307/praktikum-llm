export async function loginUser(username, password) {
    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password }),
    });

    if (response.status === 401 || response.status === 400) {
        return { exists: false, ...await response.json() }
    }

    return response.json();
}

export async function correctText(userText) {
    const response = await fetch("http://127.0.0.1:5000/correct_text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userText }),
    });
    const data = await response.json();
    return data.corrected_text;
};

export async function correctAnswers(userText, aiGeneratedText) {
    const response = await fetch("http://127.0.0.1:5000/correct_answers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userText, generatedText: aiGeneratedText }),
    });
    const data = await response.json();
    return data.corrected_answers;
};

export async function createReadingText() {
    const response = await fetch("http://127.0.0.1:5000/create_reading_text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
    });
    const data = await response.json();
    return data.reading_text;
};