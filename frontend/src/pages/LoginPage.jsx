import { useState } from "react";
import { loginUser } from "../api/backendApi";

function LoginPage() {

    const [username, setUsername] = useState("");

    const handleLogin = async () => {
        const data = await loginUser(username);
        if (data.exists) {
            alert(`yey ${data.user.username}`);
            console.log(data.user)
            console.log(data.exists)
        } else {
            alert("error");
        }
    };
    
    return (
        <div className="flex flex-col px-20">
            <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="border my-4"
            />

            <button
                onClick={handleLogin}
                className="bg-blue-400"
            >
                Enter
            </button>
        </div>
    );
}

export default LoginPage;