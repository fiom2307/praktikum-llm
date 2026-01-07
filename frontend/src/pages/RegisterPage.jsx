import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ActionButton from "../components/ActionButton";
import Modal from "../components/Modal";
import { useToast } from "../context/ToastContext";
import { checkUsername, registerUser } from "../api/authApi";
import { FiRefreshCw } from "react-icons/fi";
import logo from "../assets/logo.png";

function RegisterPage() {
  const ANIMALI = [
    "Gatto", "Cane", "Lupo", "Tigre", "Leone",
    "Volpe", "Orso", "Aquila", "Delfino", "Cavallo",
    "Panda", "Koala", "Serpente", "Gufo", "Cervo",
    "Falco", "Balena", "Squalo", "Coniglio", "Riccio", "Drago"
  ];

  const AGGETTIVI = [
    "Felice", "Coraggioso", "Gentile", "Forte", "Incredibile",
    "Fantastico", "Brillante", "Simpatico", "Audace", "Creativo",
    "Energico", "Leale", "Curioso", "Intelligente", "Veloce",
    "Magico", "Positivo", "Calmo", "Divertente", "Straordinario"
  ];
  const navigate = useNavigate();

  const [username, setUsername] = useState(generateRandomUsername());
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // Validation states
  const [usernameExists, setUsernameExists] = useState(false);
  const [passwordTooShort, setPasswordTooShort] = useState(false);
  const [passwordTooLong, setPasswordTooLong] = useState(false);
  const [passwordNoUppercase, setPasswordNoUppercase] = useState(false);
  const [passwordNoSpecial, setPasswordNoSpecial] = useState(false);
  const [passwordMismatch, setPasswordMismatch] = useState(false);


  const [showValidationModal, setShowValidationModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const { showToast } = useToast();



  function generateRandomUsername() {
    const animale =
      ANIMALI[Math.floor(Math.random() * ANIMALI.length)];

    const aggettivo =
      AGGETTIVI[Math.floor(Math.random() * AGGETTIVI.length)];

    const numero = String(Math.floor(Math.random() * 100)).padStart(2, "0");

    return `${animale}${aggettivo}${numero}`;
  }

  const handleRegenerateUsername = () => {
    setUsername(generateRandomUsername());
  };


  // Username check (database)
  useEffect(() => {
    if (username.trim().length > 0) {
      checkUsername(username).then((res) => {
        setUsernameExists(res.exists);
      });
    } else {
      setUsernameExists(false);
    }
  }, [username]);

  // Password rules check
  useEffect(() => {
    setPasswordTooShort(password.length > 0 && password.length < 6);
    setPasswordTooLong(password.length > 16);

    setPasswordNoUppercase(password.length > 0 && !/[A-Z]/.test(password));
    setPasswordNoSpecial(
      password.length > 0 && !/[!@#$%^&*()_\-+=.?]/.test(password)
    );
  }, [password]);

  // Confirm password match
  useEffect(() => {
    setPasswordMismatch(
      confirmPassword.length > 0 && password !== confirmPassword
    );
  }, [password, confirmPassword]);

  // Register handler
  const handleRegister = async () => {
    // Prevent submission if errors exist
    if (
      usernameExists ||
      passwordTooShort ||
      passwordTooLong ||
      passwordNoUppercase ||
      passwordNoSpecial ||
      passwordMismatch
    ) {
      setShowValidationModal(true);
      return;
    }

    const result = await registerUser(username, password);

    if (result.success) {
      showToast({
        title: "Account creato",
        message: "Il tuo account è stato creato con successo!",
      });

      navigate("/login");
    } else {
      setErrorMessage(result.message || "Registrazione fallita.");
      setShowErrorModal(true);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center text-black">
      <div className="flex flex-col items-center gap-4 w-full max-w-sm pb-4">

        <img
          src={logo}
          alt="Maestri dell’Apprendimento Linguini"
          className="w-64 sm:w-72 md:w-80 mb-0"
        />

        {/* Username */}
        <div className="flex items-center w-full gap-2">
          <input
            type="text"
            value={username}
            readOnly
            className="flex-1 border-2 border-gray-400 rounded-xl px-4 py-3 text-center bg-gray-100 cursor-not-allowed"
          />

          <button
            onClick={handleRegenerateUsername}
            className="flex items-center justify-center w-12 h-12 rounded-xl border-2 border-gray-400 bg-white hover:bg-gray-100 transition"
            title="Rigenera nome"
          >
            <FiRefreshCw size={20} />
          </button>
        </div>

        {usernameExists && (
          <p className="text-red-600 text-sm -mt-2">
            Questo nome utente esiste già!
          </p>
        )}

        {/* Password */}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Crea una password"
          className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        {/* Password validation messages */}
        {passwordTooShort && (
          <p className="text-red-600 text-sm -mt-2">
            La password deve avere almeno 6 caratteri!
          </p>
        )}
        {passwordTooLong && (
          <p className="text-red-600 text-sm -mt-2">
            La password non può superare 16 caratteri!
          </p>
        )}
        {passwordNoUppercase && (
          <p className="text-red-600 text-sm -mt-2">
            La password deve contenere almeno una lettera maiuscola (A–Z)!
          </p>
        )}
        {passwordNoSpecial && (
          <p className="text-red-600 text-sm -mt-2">
            La password deve contenere almeno un carattere speciale (!@#$%^&*…)
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

        {/* Submit */}
        <ActionButton
          onClick={handleRegister}
          className="bg-[#f8edd5] hover:bg-[#e7d9ba] px-8 py-3 mt-2"
        >
          Crea Account
        </ActionButton>

        {/* Back to login */}
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

      {/* MODALS */}
      {showValidationModal && (
        <Modal
          title="Errore di validazione"
          message="Per favore, correggi gli errori prima di creare un account."
          onClose={() => setShowValidationModal(false)}
        />
      )}

      {showErrorModal && (
        <Modal
          title="Errore"
          message={errorMessage}
          onClose={() => setShowErrorModal(false)}
        />
      )}
    </div>
  );
}

export default RegisterPage;