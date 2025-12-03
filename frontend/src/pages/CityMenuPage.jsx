import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Header from "../components/Header"; 
import MascotOverlay from "../components/MascotOverlay";
import vocImg from "../assets/vocabulary.png";
import readingImg from "../assets/reading.png"
import writingImg from "../assets/writing.png"

function CityMenuPage() {
  const navigate = useNavigate();
  // (e.g. /city/torino -> cityName = "torino")
  const { cityName } = useParams();

  const [showMascot, setShowMascot] = useState(true);

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
    <div className="min-h-screen flex flex-col items-center text-black">
      
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
      <div className="px-32">
        <div className="flex flex-row gap-4 px-10 justify-center grid-cols-3">
        <button
          onClick={() => navigate("/reading")}
          className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105"
          >
          <img
          src={readingImg}
          alt="Flashcards"
          className="object-contain"
          />
          Lettura
        </button>

        <button
          onClick={() => navigate("/vocabulary")}
          className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105">
          <img
          src={vocImg}
          alt="Flashcards"
          className="object-contain"
          />
          Vocabolario
        </button>

        <button
          onClick={() => navigate("/textproduction")}
          className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-3 transition-transform hover:scale-105">
          <img
          src={writingImg}
          alt="Flashcards"
          className="object-contain"
          />
          Produzione scritta
        </button>
      </div>
      </div>

     <br />
    </div>
  );
}

export default CityMenuPage;