import { API_BASE_URL } from "./config";

const SHOP_API_URL = `${API_BASE_URL}/api/shop`;

/**
 * sending buying requests
 * @param {string} username 
 * @param {number} itemId 
 * @returns {Promise<object>} 
 */

export async function buyItem(username, itemId, itemCost) {
    const response = await fetch(`${SHOP_API_URL}/buy`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json" 
        }, 
        
        body: JSON.stringify({ 
            username: username,
            item_id: itemId, 
            item_cost: itemCost 
        }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Failed to complete purchase.");
    }
    
    return data;
}


export async function getInventory(username) {
    if (!username) return [];

    const response = await fetch(`${SHOP_API_URL}/inventory?username=${username}`, {
        method: "GET",
        headers: { 
            "Content-Type": "application/json" 
        },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch inventory");
    }

    const data = await response.json();
    return data.inventory || [];
}