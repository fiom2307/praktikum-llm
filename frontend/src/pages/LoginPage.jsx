import { useState } from "react";
import { loginUser } from "../api/authApi";
import { useNavigate } from "react-router-dom";
import pisaImg from "../assets/pisatower.png";
import ActionButton from "../components/ActionButton";
import { useUser } from "../context/UserContext";
import Modal from "../components/Modal"

function LoginPage() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { loginUserContext } = useUser();
    const [showError, setShowError] = useState(false);

    const handleLogin = async () => {
        const data = await loginUser(username, password);

        if (data && data.exists) {
          loginUserContext(data);

          localStorage.setItem('userId', data.user.id);
          localStorage.setItem('username', data.user.username);

          localStorage.setItem('authToken', 'logged_in_placeholder');
          
          navigate("/");
        } else {
          setShowError(true);
        }
    };
    
    return (
    <div className="min-h-screen flex flex-col justify-start items-center  text-black">
      <div className="flex flex-col items-center gap-4 w-full max-w-sm">
        <img
          src={pisaImg}
          alt="Tower of Pisa"
          className="w-45 h-45 object-contain -mb-6"
        />

        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Inserisci il tuo nome utente"
          className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="password" // type="password" to hide 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Inserisci la tua password"
          className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <ActionButton onClick={handleLogin} className="bg-[#f8edd5] hover:bg-[#e7d9ba] px-8 py-3">Accedi</ActionButton>

        {/* register */}
        <p className="mt-2 text-sm">
          Non hai un account?{" "}
          <span
            onClick={() => navigate("/register")}
            className="text-blue-600 underline cursor-pointer hover:text-blue-800">
              Registrati ora!
            </span>
        </p>
      </div>

      {/* MODAL */}
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