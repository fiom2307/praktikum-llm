import { API_BASE_URL } from "./config";

export async function resetPassword(adminUsername, childUsername, newPassword) {
  const response = await fetch(`${API_BASE_URL}/admin/reset-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      admin_username: adminUsername,
      child_username: childUsername,
      new_password: newPassword,
    }),
  });

  const data = await response.json();

  // attach HTTP status awareness
  if (!response.ok) {
    return {
      success: false,
      message: data.message || "Server error",
    };
  }

  return data;
}