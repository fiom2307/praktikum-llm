import { useState } from "react";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import Header from "../components/Header";
import MascotOverlay from "../components/MascotOverlay";
import { useUser } from "../context/UserContext";
import vocImg from "../assets/vocabulary.png";
import readingImg from "../assets/reading.png";
import writingImg from "../assets/writing.png";

// mascot outfits
import defaultMascot from "../assets/hello.png"; 
import darthVaderImg from "../assets/darthVader.png";
import gladiatorImg from "../assets/gladiator.png";
import chefImg from "../assets/chef.png";          
import godfatherImg from "../assets/godfather.png"; 
import maradonaImg from "../assets/maradona.png";   
import ferrariImg from "../assets/ferrari.png";     

function CityMenuPage() {
  const navigate = useNavigate();
  const { cityName } = useParams();
  const location = useLocation();

  const { currentCostumeId } = useUser();

  const isInitialEntry = location.state?.initialEntry === true;
  const [showMascot, setShowMascot] = useState(isInitialEntry);

  const COSTUME_MAP = {
    0: defaultMascot,  // default: hello
    1: darthVaderImg,  // ID 1: Darth Vader
    2: gladiatorImg,    // ID 2: Gladiator
    3: chefImg,      // ID 3 -> Chef
    4: godfatherImg, // ID 4 -> Godfather
    5: maradonaImg,  // ID 5 -> Maradona
    6: ferrariImg    // ID 6 -> Ferrari
  };

  const currentMascotImg = COSTUME_MAP[currentCostumeId] || defaultMascot;

  // Dialogue of each cities
  // Dialogue of each city (simple Italian + small English hint)
  const cityDialogues = {
    torino: [
      "Ciao! Benvenuto a Torino!",
      "This is the first stop of our journey through Italy.",
      "Now is a good time to get to know Italian culture and language!"
    ],
    milano: [
      "Ciao! Benvenuto a Milano!",
      "Milano è famosa per la moda e il Duomo.",
      "Let’s practice Italian while exploring this modern city!"
    ],
    venezia: [
      "Ciao! Eccoci a Venezia!",
      "Attento all’acqua e ai canali, non ci sono macchine qui.",
      "Let’s do something fun to get familiar with this magical city on the water!"
    ],
    firenze: [
      "Ciao! Benvenuto a Firenze!",
      "Firenze è la città del Rinascimento, piena di arte e storia.",
      "Use this stop to build your Italian skills step by step, like an artist."
    ],
    cagliari: [
      "Ciao! Benvenuto a Cagliari, in Sardegna!",
      "Qui trovi mare, sole e una cultura molto speciale.",
      "Let’s learn Italian with a relaxed island mood!"
    ],
    roma: [
      "Ciao! Benvenuto a Roma!",
      "All roads lead to Rome – tutte le strade portano a Roma.",
      "Rome is an amazing city full of history. Enjoy your Italian practice here!"
    ],
    pescara: [
      "Ciao! Benvenuto a Pescara!",
      "Una città sul mare Adriatico, perfetta per una pausa.",
      "Let’s keep going – ogni esercizio ti porta più vicino alla fluency!"
    ],
    napoli: [
      "Ciao! Benvenuto a Napoli!",
      "Napoli è famosa per la pizza e il Vesuvio.",
      "This is a great place to celebrate what you’ve learned so far!"
    ],
    // Fallback
    default: [
      "Ciao! Welcome to Italy!",
      "Choose a task to start practicing your Italian.",
      "Ogni piccolo passo è importante – every small step counts!"
    ]
  };

  const currentDialogue =
    cityDialogues[cityName.toLowerCase()] || cityDialogues.default;

  // Level / title config for each city
  const cityConfig = {
    torino: { title: "Torino", level: "Livello 1" },
    milano: { title: "Milano", level: "Livello 2" },
    venezia: { title: "Venezia", level: "Livello 3" },
    firenze: { title: "Firenze", level: "Livello 4" },
    cagliari: { title: "Cagliari", level: "Livello 5" },
    roma: { title: "Roma", level: "Livello 6" },
    pescara: { title: "Pescara", level: "Livello 7" },
    napoli: { title: "Napoli", level: "Livello 8" }
  };

  const currentCity =
    cityConfig[cityName.toLowerCase()] || {
      title: cityName,
      level: "Livello base"
    };

  return (
    <div className="min-h-screen flex flex-col items-center text-black">
      {/* Mascot overlay (first entry only) */}
      {showMascot && (
        <MascotOverlay 
          dialogues={currentDialogue} 
          onComplete={() => setShowMascot(false)} 
          currentImage={currentMascotImg}
        />
      )}

      {/* Header */}
      <Header onBack={() => navigate("/story")} />

      {/* City title and info */}
      <div className="flex flex-col items-center mb-6">
        <h1 className="text-3xl sm:text-5xl font-extrabold drop-shadow-md text-center capitalize">
          📍 {currentCity.title}
        </h1>
        <p className="text-lg sm:text-xl mt-2 font-semibold text-gray-700">
          {currentCity.level}
        </p>
        <p className="text-base sm:text-lg mt-4 max-w-2xl text-center px-4">
          Benvenuto a {currentCity.title}! Scegli la tua sfida.
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
