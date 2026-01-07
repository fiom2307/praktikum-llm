import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import { FaUserCircle, FaArrowLeft } from "react-icons/fa";

export default function Header({ onBack }) {
  const navigate = useNavigate();
  const location = useLocation();

  const { pizzaCount, updatePizzaCount } = useUser();
  const username = localStorage.getItem("username");
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef(null);

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
  }

  useEffect(() => {
    // Close dropdown when clicking outside of the menu
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    // Clear session info and send user to login
    localStorage.removeItem("authToken");
    localStorage.removeItem("userId");
    localStorage.removeItem("username");
    localStorage.removeItem("pizzaCount");
    updatePizzaCount(0);
    navigate("/login");
  };

  const handleNavigate = (path) => {
    navigate(path);
    setIsMenuOpen(false);
  };

  return (
    <header className="w-full flex justify-between items-center px-6 py-4 mb-8 bg-[#3399bd] text-white relative z-30">

      {location.pathname === "/" ? (
        <p className="font-bold text-lg">Maestri dell’Apprendimento Linguini</p>
      ) : (
        <button onClick={handleBackClick} className="text-2xl">
          <FaArrowLeft />
        </button>
      )}

      <div className="flex items-center gap-6 text-lg">
        
        {/* pizza amount */}
        <span className="">Pizze: 🍕{pizzaCount}</span>

        <div className="h-4 w-[2px] bg-white/60"></div>

        <div className="relative" ref={menuRef}>
          {/* username/click */}
          <button
            type="button"
            className="flex gap-2 items-center focus:outline-none"
            onClick={() => setIsMenuOpen((prev) => !prev)}
          >
            <span className="font-bold">{username}</span>
            <FaUserCircle className="text-3xl" />
          </button>

          {/*(Dropdown) */}
          {isMenuOpen && (
            <div className="absolute right-0 mt-3 w-44 bg-white text-black rounded-xl shadow-lg py-2 border border-gray-200 z-40">
              
              {/* Backpack button */}
              <button
                className={`w-full text-left px-4 py-2 hover:bg-gray-100 ${location.pathname === "/inventory" ? "text-gray-400 cursor-default pointer-events-none" : ""}`}
                onClick={handleInventoryClick}
              >
                Il mio zaino
              </button>

              {/* Flashcard button */}
              <button
                className={`w-full text-left px-4 py-2 hover:bg-gray-100 ${location.pathname === "/flashcards" ? "text-gray-400 cursor-default pointer-events-none" : ""}`}
                onClick={() => handleNavigate("/flashcards")}
              >
                Flashcard
              </button>

              {/* Shop button */}
              <button
                className={`w-full text-left px-4 py-2 hover:bg-gray-100 ${location.pathname === "/shop" ? "text-gray-400 cursor-default pointer-events-none" : ""}`}
                onClick={() => handleNavigate("/shop")}
              >
                Negozio
              </button>
              
              <div className="my-2 h-px bg-gray-200"></div>
              
              {/* Log out button */}
              <button
                className="w-full text-left px-4 py-2 text-red-600 hover:bg-gray-100"
                onClick={handleLogout}
              >
                Esci
              </button>
            </div>
          )}
        </div>
          
      </div>
    </header>
  );
}

