import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import pisaImg from "../assets/pisatower.png";
import ActionButton from "../components/ActionButton";
import Modal from "../components/Modal";
import { useToast } from "../context/ToastContext";
import { checkUsername, registerUser } from "../api/authApi";

function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
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
    <div className="min-h-screen flex flex-col justify-start items-center text-black">
      <div className="flex flex-col items-center gap-4 w-full max-w-sm pb-4">

        <img
          src={pisaImg}
          alt="Tower of Pisa"
          className="w-45 h-45 object-contain -mb-6"
        />

        {/* Username */}
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