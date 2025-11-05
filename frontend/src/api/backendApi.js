export async function loginUser(username) {
    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username }),
    });
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