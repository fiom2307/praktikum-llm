import { useNavigate } from "react-router-dom";
import ActionButton from "./ActionButton";
import { useUser } from "../context/UserContext";

export default function Header({ onBack }) {
  const navigate = useNavigate();

  const { pizzaCount } = useUser();
  const username = localStorage.getItem("username");

  const handleBackClick = () => {
    if (onBack) {
      // 
      onBack();
    } else {
      // back to main page
      navigate("/");
    }
  };

  const handleInventoryClick = () => {
        navigate("/inventory");
  };

  return (
    <header className="w-full flex justify-between items-start p-6">

      {/* Back Button */}
      <ActionButton onClick={handleBackClick}>← Indietro</ActionButton>

      {/* Username + Pizza Count */}
      <div className="text-right flex flex-col items-end gap-1">
        <div className="flex items-center gap-2">
          <ActionButton onClick={handleInventoryClick} className="mr-2">
              🎒My Backpack
          </ActionButton>
          <h2 className="text-xl font-bold">{username}</h2>
        </div>
        <p className="text-sm">
          🍕 <span className="font-semibold">Pizze:</span> {pizzaCount}
        </p>
      </div>
    </header>
  );
}