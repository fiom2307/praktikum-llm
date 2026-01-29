import { useState } from "react";
import { resetPassword } from "../api/adminApi";
import Header from "../components/Header";
import ActionButton from "../components/ActionButton";

export default function AdminPage() {
  const [childUsername, setChildUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [msg, setMsg] = useState("");

  const adminUsername = localStorage.getItem("username");

  const handleResetPassword = async () => {
    try {
      const res = await resetPassword(
        adminUsername,
        childUsername,
        newPassword
      );

      if (res.success) {
        setMsg("Password reset successfully!");
        setChildUsername("");
        setNewPassword("");
      } else {
        setMsg(res.message);
      }
    } catch {
      setMsg("Server is unreachable");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center text-black">
        <Header />
        
        <h1 className="text-4xl font-extrabold mt-0 mb-10 drop-shadow-md text-center">Reset Password</h1>

        <div className="flex flex-col gap-4 w-full max-w-md px-4">
            <input
                placeholder="Username of the kid"
                value={childUsername}
                onChange={e => setChildUsername(e.target.value)}
                className="border border-gray-400 rounded-xl px-8 py-3 text-center focus:outline-none focus:ring-2 focus:ring-[#3399bd] w-full sm:w-auto"
            />

            <input
                type="password"
                placeholder="New password"
                value={newPassword}
                onChange={e => setNewPassword(e.target.value)}
                className="border border-gray-400 rounded-xl px-8 py-3 text-center focus:outline-none focus:ring-2 focus:ring-[#3399bd] w-full sm:w-auto"
            />

            <ActionButton
                onClick={handleResetPassword}
                className="bg-[#f8edd5] hover:bg-[#e7d9ba] text-lg"
            >
                Reset password
            </ActionButton>

            {msg && <p>{msg}</p>}
        </div>
    </div>
  );
}
