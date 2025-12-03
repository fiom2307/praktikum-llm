import { useState } from "react";
import { useNavigate, useParams , useLocation} from "react-router-dom";
import Header from "../components/Header"; 
import ActionButton from "../components/ActionButton";
import MascotOverlay from "../components/MascotOverlay";

function CityMenuPage() {
  const navigate = useNavigate();
  // (e.g. /city/torino -> cityName = "torino")
  const { cityName } = useParams();

  const location = useLocation();

  const isInitialEntry = location.state?.initialEntry === true;

  const [showMascot, setShowMascot] = useState(isInitialEntry);

  // Dialogue of each cities
  const cityDialogues = {
    torino: [
      "Ciao! Benvenuto a Torino!",
      "This is the first stop of our journey.",
      "Now is a good time to know about Italy!"
    ],
    venezia: [
      "Ciao! Eccoci a Venezia!",
      "Be careful of the water!",
      "Let's do something fun to get familiar with the city!"
    ],
    roma: [
      "Ciao! Finalmente a Roma!",
      "All roads leads to Rome.",
      "Rome is an amazing city! Enjoy!"
    ],
    // 
    default: [
      "Ciao! Welcome to Italy!",
      "Choose a task to start."
    ]
  };

  const currentDialogue = cityDialogues[cityName.toLowerCase()] || cityDialogues.default;

  // the topic of each city
  const cityConfig = {
    torino: { title: "Torino", level: "Livello 1" },
    venezia: { title: "Venezia", level: "Livello 2" },
    roma: { title: "Roma", level: "Livello 3" }
  };

  const currentCity = cityConfig[cityName.toLowerCase()] || { title: cityName, level: "Livello Base" };

  return (
    <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
      
      {/* showMascot */}
      {showMascot && (
        <MascotOverlay 
          dialogues={currentDialogue} 
          onComplete={() => setShowMascot(false)} 
        />
      )}

      {/* Head Components */}
      <Header />

      <div className="flex flex-col items-center mt-10 mb-12">
        <h1 className="text-5xl font-extrabold drop-shadow-md text-center capitalize">
          📍 {currentCity.title}
        </h1>
        <p className="text-xl mt-2 font-semibold text-gray-700">{currentCity.level}</p>
        <p className="text-lg mt-4 max-w-2xl text-center px-4">
          Benvenuto a {currentCity.title}! Scegli la tua sfida.
          <br/>
          (Welcome to {currentCity.title}！Please choose your task)
        </p>
      </div>

      {/* three function button of MainPage  */}
      <div className="flex flex-col gap-6 w-full max-w-md px-6">
        <button
          onClick={() => navigate("/reading", { state: { fromCity: cityName } })}
          className="bg-green-700 hover:bg-green-800 text-white text-2xl font-semibold py-6 rounded-2xl shadow-lg transition-transform hover:scale-105 flex items-center justify-center gap-4"
        >
          <span>📖</span> Lettura (Reading)
        </button>

        <button
          onClick={() => navigate("/vocabulary", { state: { fromCity: cityName } })}
          className="bg-white hover:bg-gray-200 text-black text-2xl font-semibold py-6 rounded-2xl shadow-lg transition-transform hover:scale-105 flex items-center justify-center gap-4"
        >
          <span>📒</span> Vocabolario (Vocabulary)
        </button>

        <button
          onClick={() => navigate("/textproduction", { state: { fromCity: cityName } })}
          className="bg-red-600 hover:bg-red-800 text-white text-2xl font-semibold py-6 rounded-2xl shadow-lg transition-transform hover:scale-105 flex items-center justify-center gap-4"
        >
          <span>✍️</span> Produzione scritta (Writing)
        </button>
      </div>

      <div className="mt-12 mb-10">
        <ActionButton onClick={() => navigate("/")} className="bg-gray-500 hover:bg-gray-600">
          ← Back to Map
        </ActionButton>
      </div>
    </div>
  );
}

export default CityMenuPage;