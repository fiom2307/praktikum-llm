import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import ActionButton from "./ActionButton";

export default function Header() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [pizzaCount, setPizzaCount] = useState(0);

  useEffect(() => {
    const storedUsername = localStorage.getItem("username") || "";
    const storedPizzaCount = Number(localStorage.getItem("pizzaCount")) || 0;

    setUsername(storedUsername);
    setPizzaCount(storedPizzaCount);
  }, []);

  return (
    <header className="w-full flex justify-between items-start p-6">

      {/* Back Button */}
      <ActionButton onClick={() => navigate("/")}>← Back</ActionButton>

      {/* Username + Pizza Count */}
      <div className="text-right flex flex-col items-end gap-1">
        <div className="flex items-center gap-2">
          <h2 className="text-xl font-bold">{username}</h2>
        </div>
        <p className="text-sm">
          🍕 <span className="font-semibold">Pizza count:</span> {pizzaCount}
        </p>
      </div>
    </header>
  );
}