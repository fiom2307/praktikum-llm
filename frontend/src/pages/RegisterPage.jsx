import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import pisaImg from "../assets/pisatower.png";
import ActionButton from "../components/ActionButton";
import { checkUsername, registerUser } from "../api/authApi";

function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [usernameExists, setUsernameExists] = useState(false);
  const [passwordTooShort, setPasswordTooShort] = useState(false);
  const [passwordMismatch, setPasswordMismatch] = useState(false);

  useEffect(() => {
    if (username.trim().length > 0) {
      checkUsername(username).then((res) => {
        setUsernameExists(res.exists);
      });
    } else {
      setUsernameExists(false);
    }
  }, [username]);

  useEffect(() => {
    setPasswordTooShort(password.length > 0 && password.length < 6);
  }, [password]);

  useEffect(() => {
    setPasswordMismatch(
      confirmPassword.length > 0 && password !== confirmPassword
    );
  }, [password, confirmPassword]);

  const handleRegister = async () => {
    if (usernameExists || passwordTooShort || passwordMismatch) {
      alert("Per favore, correggi gli errori prima di creare un account.");
      return;
    }

    const result = await registerUser(username, password);

    if (result.success) {
      alert("Account creato con successo!");
      navigate("/login");
    } else {
      alert(result.message || "Registrazione fallita.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-start items-center bg-blue-200 text-black">
      <div className="flex flex-col items-center gap-4 w-full max-w-sm">

        <img
          src={pisaImg}
          alt="Tower of Pisa"
          className="w-45 h-45 object-contain -mb-6"
        />

        {/* Username input */}
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Crea un nome utente"
          className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        {usernameExists && (
          <p className="text-red-600 text-sm -mt-2">
            Questo nome utente esiste già!
          </p>
        )}

        {/* Password input */}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Crea una password"
          className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        {passwordTooShort && (
          <p className="text-red-600 text-sm -mt-2">
            La password deve avere almeno 6 caratteri!
          </p>
        )}

        {/* Confirm password */}
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Ripeti la password"
          className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        {passwordMismatch && (
          <p className="text-red-600 text-sm -mt-2">
            Le password non coincidono!
          </p>
        )}

        {/* Submit button */}
        <ActionButton onClick={handleRegister} className="px-8 py-3 mt-2">
          Crea Account
        </ActionButton>

        {/* Link back to login */}
        <p className="mt-2 text-sm">
          Hai già un account?{" "}
          <span
            onClick={() => navigate("/login")}
            className="text-blue-600 underline cursor-pointer hover:text-blue-800"
          >
            Accedi
          </span>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
