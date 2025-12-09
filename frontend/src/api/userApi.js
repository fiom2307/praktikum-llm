import { API_BASE_URL } from "./config";

export async function equipCostume(username, itemId) {
    const response = await fetch(`${API_BASE_URL}/user/equip`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            username: username,
            item_id: itemId 
        }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Failed to equip costume.");
    }
    return data; 
}