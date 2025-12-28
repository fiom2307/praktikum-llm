import { API_BASE_URL } from "./config";

export async function incrementPizzaCount(amount, cityKey = null) {
  const userId = localStorage.getItem("userId");

  const body = {
    user_id: userId,
    amount
  };

  if (cityKey) {
    body.city_key = cityKey;
  }

  const response = await fetch(`${API_BASE_URL}/pizza_count`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  return await response.json();
}