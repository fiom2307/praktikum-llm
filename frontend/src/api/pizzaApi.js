import { API_BASE_URL } from "./config";

export async function incrementPizzaCount(inc) {
    const userId = localStorage.getItem("userId");

    const response = await fetch(`${API_BASE_URL}/pizza_count/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ inc })
    });

    return await response.json();
}