import { useState } from "react";
import { resetOwnPassword } from "../api/authApi";
import Header from "../components/Header";
import ActionButton from "../components/ActionButton";

export default function ChangePasswordPage() {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [msg, setMsg] = useState("");

  const username = localStorage.getItem("username");

  const handleChangePassword = async () => {
    try {
      const res = await resetOwnPassword(
        username,
        oldPassword,
        newPassword
      );

      if (res.success) {
        setMsg("Password aggiornata con successo!");
        setOldPassword("");
        setNewPassword("");
      } else {
        setMsg(res.message);
      }
    } catch {
      setMsg("Il server non è raggiungibile");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center text-black">
      <Header />

      <h1 className="text-4xl font-extrabold mt-0 mb-10 drop-shadow-md text-center">
        Cambia password
      </h1>

      <div className="flex flex-col gap-4 w-full max-w-md px-4">
        <input
          type="password"
          placeholder="Password attuale"
          value={oldPassword}
          onChange={e => setOldPassword(e.target.value)}
          className="border border-gray-400 rounded-xl px-8 py-3 text-center focus:outline-none focus:ring-2 focus:ring-[#3399bd] w-full sm:w-auto"
        />

        <input
          type="password"
          placeholder="Nuova password"
          value={newPassword}
          onChange={e => setNewPassword(e.target.value)}
          className="border border-gray-400 rounded-xl px-8 py-3 text-center focus:outline-none focus:ring-2 focus:ring-[#3399bd] w-full sm:w-auto"
        />

        <ActionButton
          onClick={handleChangePassword}
          className="bg-[#f8edd5] hover:bg-[#e7d9ba] text-lg"
        >
          Salva password
        </ActionButton>

        {msg && <p className="text-center">{msg}</p>}
      </div>
    </div>
  );
}
