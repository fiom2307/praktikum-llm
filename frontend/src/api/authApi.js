import { API_BASE_URL } from "./config";

export async function loginUser(username, password) {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password }),
    });

    if (response.status === 401 || response.status === 400) {
        return { exists: false, ...await response.json() }
    }

    return response.json();
}