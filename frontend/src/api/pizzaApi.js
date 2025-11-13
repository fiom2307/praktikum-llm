import { API_BASE_URL } from "./config";

export async function incrementPizzaCount(username, inc) {
    const response = await fetch(`${API_BASE_URL}/increment_pizza_count`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, inc })
    });
    return response.json();
}