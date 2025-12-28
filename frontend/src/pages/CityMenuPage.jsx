import { useNavigate, useParams, useLocation } from "react-router-dom";
import Header from "../components/Header";
import MascotOverlay from "../components/MascotOverlay";
import ProgressBar from "../components/ProgressBar";
import { useUser } from "../context/UserContext";
import vocImg from "../assets/vocabulary.png";
import readingImg from "../assets/reading.png";
import writingImg from "../assets/writing.png";
import { useEffect, useState } from "react";
import { getCity } from "../api/cityApi";

function CityMenuPage() {
  const [city, setCity] = useState("");
  const [progress, setProgress] = useState(0);
  const navigate = useNavigate();
  const { cityName } = useParams();
  const location = useLocation();

  const { currentCostumeId } = useUser();

  const isInitialEntry = location.state?.initialEntry === true;
  const [showMascot, setShowMascot] = useState(isInitialEntry);

  // Dialogue of each cities
  // Dialogue of each city (simple Italian + small English hint)
  const cityDialogues = {
    palermo: [
      "Ciao! Benvenuto a Palermo!",
      "Palermo è in Sicilia, un luogo ricco di storia e cultura.",
      "Iniziamo il nostro viaggio imparando l’italiano con calma e curiosità."
    ],

    napoli: [
      "Ciao! Benvenuto a Napoli!",
      "Napoli è famosa per la pizza e il Vesuvio.",
      "Qui puoi mettere in pratica quello che hai già imparato!"
    ],

    roma: [
      "Ciao! Benvenuto a Roma!",
      "Tutte le strade portano a Roma.",
      "Questa città è piena di storia: continuiamo il nostro viaggio linguistico!"
    ],

    siena: [
      "Ciao! Benvenuto a Siena!",
      "Siena è una città medievale nel cuore della Toscana.",
      "Qui possiamo migliorare il nostro italiano passo dopo passo."
    ],

    venezia: [
      "Ciao! Benvenuto a Venezia!",
      "Attento ai canali: qui non ci sono macchine!",
      "Impariamo l’italiano in una delle città più magiche del mondo."
    ],

    torino: [
      "Ciao! Benvenuto a Torino!",
      "Torino è una città elegante e storica del nord Italia.",
      "Sei arrivato lontano: usiamo tutto quello che hai imparato!"
    ],

    // Fallback
    default: [
      "Ciao! Welcome to Italy!",
      "Choose a task to start practicing your Italian.",
      "Ogni piccolo passo è importante – every small step counts!"
    ]
  };

  useEffect(() => {
    getCity(cityName).then((data) => {
      setCity(data);

      const earned = data.pizzas_earned;
      const required = data.min_pizzas_to_unlock;

      setProgress(Math.min(100, Math.round((earned / required) * 100)));
    });
  }, [cityName]);

  const currentDialogue =
    cityDialogues[cityName.toLowerCase()] || cityDialogues.default;

  return (
    <div className="min-h-screen flex flex-col items-center text-black">
      {/* Mascot overlay (first entry only) */}
      {showMascot && (
        <MascotOverlay 
          dialogues={currentDialogue} 
          onComplete={() => setShowMascot(false)} 
          currentImage={currentCostumeId}
        />
      )}

      {/* Header */}
      <Header onBack={() => navigate("/story")} />

      {/* City title and info */}
      <div className="flex flex-col items-center mb-6">
        <h1 className="text-3xl sm:text-5xl font-extrabold drop-shadow-md text-center capitalize">
          📍 {city.name}
        </h1>
        <p className="text-lg sm:text-xl mt-2 font-semibold text-gray-700">
          Livello {city.level}
        </p>

        <ProgressBar value={progress} />

        <p className="text-base sm:text-lg mt-4 max-w-2xl text-center px-4">
          Benvenuto a {city.name}! Scegli la tua sfida.
        </p>
      </div>

      {/* Reading / Vocabulary / Writing buttons */}
      <div className="w-full flex justify-center">
        <div
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center px-4 sm:px-10 lg:px-32">
          <button
            onClick={() =>
              navigate("/reading", { state: { fromCity: cityName } })
            }
            className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105"
          >
            <img src={readingImg} alt="Reading" className="object-contain" />
            Lettura
          </button>

          <button
            onClick={() =>
              navigate("/vocabulary", { state: { fromCity: cityName } })
            }
            className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105"
          >
            <img src={vocImg} alt="Vocabulary" className="object-contain" />
            Vocabolario
          </button>

          <button
            onClick={() =>
              navigate("/textproduction", { state: { fromCity: cityName } })
            }
            className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105"
          >
            <img src={writingImg} alt="Writing" className="object-contain" />
            Produzione scritta
          </button>
        </div>
      </div>
    </div>
  );

}

export default CityMenuPage;
