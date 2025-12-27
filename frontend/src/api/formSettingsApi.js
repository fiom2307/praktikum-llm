import { API_BASE_URL } from "./config";

export async function getFormSettings() {

    const response = await fetch(`${API_BASE_URL}/form_settings`);

    return response.json();
}