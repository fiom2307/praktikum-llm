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

// City background images
import napoliBg from "../assets/cities/napoli.png";
import palermoBg from "../assets/cities/palermo.png";
import romaBg from "../assets/cities/roma.png";
import sienaBg from "../assets/cities/siena.png";
import veneziaBg from "../assets/cities/venezia.png";
import torinoBg from "../assets/cities/torino.png";

function CityMenuPage() {
  const [city, setCity] = useState("");
  const [progress, setProgress] = useState(0);
  const navigate = useNavigate();
  const { cityName } = useParams();
  const location = useLocation();

  const { currentCostumeId } = useUser();

  const isInitialEntry = location.state?.initialEntry === true;
  const [showMascot, setShowMascot] = useState(isInitialEntry);

  // Dialogue of each city (simple Italian + small English hint)
  const cityDialogues = {
    napoli: [
      "Ciao! Benvenuto a Napoli, l'inizio del nostro viaggio!",
      "Napoli è la città del sole, del mare e, naturalmente, della pizza!",
      "Cominciamo qui a costruire le tue basi della lingua italiana."
    ],
    palermo: [
      "Benvenuto a Palermo, nel cuore della Sicilia!",
      "Questa città è un incrocio magico di culture e sapori antichi.",
      "Esploriamo la storia dell'isola mentre impariamo nuove parole!"
    ],
    roma: [
      "Eccoci a Roma, la Città Eterna!",
      "Tutte le strade portano qui. C'è così tanta storia in ogni angolo.",
      "Mettiti alla prova con sfide degne di un vero imperatore!"
    ],
    siena: [
      "Ciao! Benvenuto nella splendida Siena!",
      "Questa città medievale è famosa per il Palio e la sua architettura unica.",
      "Alleniamo la tua produzione scritta tra i vicoli della Toscana."
    ],
    venezia: [
      "Benvenuto a Venezia, la città sull'acqua!",
      "Qui non ci sono macchine, solo barche e gondole. Che magia!",
      "Fai attenzione ai canali mentre completi le tue missioni!"
    ],
    torino: [
      "Complimenti! Sei arrivato a Torino, l'ultima tappa!",
      "Torino è una città elegante, famosa per il cioccolato e i suoi caffè storici.",
      "È il momento di dimostrare tutto quello che hai imparato in questo viaggio!"
    ],
    default: [
      "Ciao! Welcome to Italy!",
      "Choose a task to start practicing your Italian.",
      "Ogni piccolo passo è importante – every small step counts!"
    ]
  };

  const currentDialogue =
    cityDialogues[cityName?.toLowerCase()] || cityDialogues.default;

  // City background mapping
  const cityBackgrounds = {
    napoli: napoliBg,
    palermo: palermoBg,
    roma: romaBg,
    siena: sienaBg,
    venezia: veneziaBg,
    torino: torinoBg
  };

  const selectedBg =
    cityBackgrounds[cityName?.toLowerCase()] || napoliBg;

  useEffect(() => {
    getCity(cityName).then((data) => {
      setCity(data);

      const earned = data.pizzas_earned;
      const required = data.min_pizzas_to_unlock;

      setProgress(Math.min(100, Math.round((earned / required) * 100)));
    });
  }, [cityName]);

  return (
    <div
      className="min-h-screen flex flex-col items-center text-black relative bg-cover bg-center"
      style={{ backgroundImage: `url(${selectedBg})` }}
    >
      {/* Dark overlay for readability */}
      <div className="absolute inset-0 bg-black/35 backdrop-blur-[1px] z-0" />

      {/* Content wrapper above background */}
      <div className="relative z-10 w-full flex flex-col items-center">
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
          <h1 className="text-3xl sm:text-5xl font-extrabold drop-shadow-md text-center capitalize text-white">
            📍 {city.name}
          </h1>

          <p className="text-lg sm:text-xl mt-2 font-semibold text-white/90">
            Livello {city.level}
          </p>

          <ProgressBar value={progress} />

          <p className="text-base sm:text-lg mt-4 max-w-2xl text-center px-4 text-white/95">
            Benvenuto a {city.name}! Scegli la tua sfida.
          </p>
        </div>

        {/* Reading / Vocabulary / Writing buttons */}
        <div className="w-full flex justify-center pb-10">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center px-4 sm:px-10 lg:px-32">
            <button
              onClick={() => navigate("/reading", { state: { fromCity: cityName } })}
              className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105"
            >
              <img src={readingImg} alt="Reading" className="object-contain" />
              Lettura
            </button>

            <button
              onClick={() => navigate("/vocabulary", { state: { fromCity: cityName } })}
              className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105"
            >
              <img src={vocImg} alt="Vocabulary" className="object-contain" />
              Vocabolario
            </button>

            <button
              onClick={() => navigate("/textproduction", { state: { fromCity: cityName } })}
              className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105"
            >
              <img src={writingImg} alt="Writing" className="object-contain" />
              Produzione scritta
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CityMenuPage;