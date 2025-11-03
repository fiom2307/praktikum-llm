import { useState } from "react";
import { loginUser } from "../api/backendApi";
import { useNavigate } from "react-router-dom";
import pisaImg from "../assets/pisatower.png";

function LoginPage() {

    const [username, setUsername] = useState("");
    const navigate = useNavigate();

    const handleLogin = async () => {
        const data = await loginUser(username);
        if (data.exists) {
            navigate("/");
        } else {
            alert("error");
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

        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
          className="border-2 border-gray-400 rounded-xl px-4 py-3 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <button
          onClick={handleLogin}
          className="bg-blue-400 hover:bg-blue-500 text-black font-semibold px-8 py-3 rounded-xl shadow-md transition-transform hover:scale-105"
        >
          Enter
        </button>
      </div>
    </div>
    );
}

export default LoginPage;