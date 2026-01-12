import { useState } from "react";
import { loginUser } from "../api/authApi";
import { useNavigate } from "react-router-dom";
import ActionButton from "../components/ActionButton";
import { useUser } from "../context/UserContext";
import Modal from "../components/Modal";

import logo from "../assets/logo.png";
import wolf from "../assets/outfits/hello.png";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showError, setShowError] = useState(false);

  const navigate = useNavigate();
  const { loginUserContext } = useUser();

  const handleLogin = async () => {
    const data = await loginUser(username, password);

    if (data && data.exists) {
      loginUserContext(data);
      localStorage.setItem("userId", data.user.id);
      localStorage.setItem("username", data.user.username);
      localStorage.setItem("authToken", "logged_in_placeholder");
      navigate("/");
    } else {
      setShowError(true);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#60aac4] px-6">
      {/* relative wrapper */}
      <div className="relative w-full max-w-5xl flex justify-center">
        
        {/* LOGIN (CENTERED) */}
        <div className="flex flex-col items-center gap-4 w-full max-w-sm z-10">
          <img
            src={logo}
            alt="Maestri dell’Apprendimento Linguini"
            className="w-64 sm:w-72 md:w-80 mb-0"
          />

          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Inserisci il tuo nome utente"
            className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Inserisci la tua password"
            className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <ActionButton
            onClick={handleLogin}
            className="bg-[#f8edd5] hover:bg-[#e7d9ba] px-10 py-3"
          >
            Accedi
          </ActionButton>

          <p className="text-sm mt-2">
            Non hai un account?{" "}
            <span
              onClick={() => navigate("/register")}
              className="text-blue-700 underline cursor-pointer hover:text-blue-900"
            >
              Registrati ora!
            </span>
          </p>
        </div>
      </div>

      {showError && (
        <Modal
          title="Errore di accesso"
          message="Nome utente o password non validi."
          onClose={() => setShowError(false)}
        />
      )}
    </div>
  );
}

export default LoginPage;