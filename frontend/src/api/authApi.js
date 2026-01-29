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

export async function checkUsername(username) {
    const response = await fetch(`${API_BASE_URL}/check_username/${username}`);
    return response.json(); 
}

export async function registerUser(username, password) {
    const response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    return response.json();
}

export async function resetOwnPassword(username, oldPassword, newPassword) {
  const response = await fetch(`${API_BASE_URL}/user/reset-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username,
      old_password: oldPassword,
      new_password: newPassword,
    }),
  });

  return response.json();
}