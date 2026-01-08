import { API_BASE_URL } from "./config";

export async function getCityProgress() {
    const userId = localStorage.getItem("userId");
    const response = await fetch(
        `${API_BASE_URL}/cities/progress/${userId}`,
        {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
        }
    );

    const data = await response.json();
    return data.cities;
}

export async function getCity(cityKey) {
  const userId = localStorage.getItem("userId");

  const response = await fetch(
    `${API_BASE_URL}/cities/${cityKey}/${userId}`
  );

  if (!response.ok) {
    throw new Error("City locked or not found");
  }

  const data = await response.json();
  return data.city;
}
