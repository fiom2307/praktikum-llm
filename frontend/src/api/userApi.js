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

export const getCurrentMultiplier = async (username) => {
    const res = await fetch(
        `${API_BASE_URL}/user/${username}/multiplier`
    );

    if (!res.ok) {
        throw new Error("Failed to fetch current multiplier");
    }

    return res.json();
};
