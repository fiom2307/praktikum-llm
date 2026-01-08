import { useNavigate, useParams, useLocation } from "react-router-dom";
import Header from "../components/Header";
import MascotOverlay from "../components/MascotOverlay";
import ProgressBar from "../components/ProgressBar";
import { useUser } from "../context/UserContext";
import vocImg from "../assets/vocabulary.png";
import readingImg from "../assets/reading.png";
import writingImg from "../assets/writing.png";
import { useEffect, useState, useMemo } from "react";
import { getCity } from "../api/cityApi";

import PassportOverlay from "../components/PassportOverlay";
import HelpModal from "../components/HelpModal";
import { FaRegAddressBook } from "react-icons/fa";

// City background images
import napoliBg from "../assets/cities/napoli.png";
import palermoBg from "../assets/cities/palermo.png";
import romaBg from "../assets/cities/roma.png";
import sienaBg from "../assets/cities/siena.png";
import veneziaBg from "../assets/cities/venezia.png";
import torinoBg from "../assets/cities/torino.png";

// Badges
import napoliBadge from "../assets/badges/Napoli.png";
import palermoBadge from "../assets/badges/Palermo.png";
import romaBadge from "../assets/badges/Roma.png";
import sienaBadge from "../assets/badges/Siena.png";
import veneziaBadge from "../assets/badges/Venezia.png";
import torinoBadge from "../assets/badges/Torino.png";

function CityMenuPage() {
  const [city, setCity] = useState("");
  const navigate = useNavigate();
  const { cityName } = useParams();
  const location = useLocation();

  const { currentCostumeId } = useUser();

  const cityKey = (cityName || "").toLowerCase();

  const isInitialEntry = location.state?.initialEntry === true;
  const [showMascot, setShowMascot] = useState(isInitialEntry);

  const [passportOpen, setPassportOpen] = useState(false);

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

  const currentDialogue = cityDialogues[cityKey] || cityDialogues.default;

  const cityBackgrounds = {
    napoli: napoliBg,
    palermo: palermoBg,
    roma: romaBg,
    siena: sienaBg,
    venezia: veneziaBg,
    torino: torinoBg
  };

  const selectedBg = cityBackgrounds[cityKey] || napoliBg;

  const CITY_BADGES = useMemo(
    () => ({
      napoli: napoliBadge,
      palermo: palermoBadge,
      roma: romaBadge,
      siena: sienaBadge,
      venezia: veneziaBadge,
      torino: torinoBadge
    }),
    []
  );

  const CITY_INFO = useMemo(
    () => ({
      napoli: [
        "Napoli è famosa per la pizza e la sua energia unica.",
        "Vista sul Vesuvio e un mare spettacolare.",
        "Centro storico pieno di vicoli e tradizioni."
      ],
      palermo: [
        "Palermo è nel cuore della Sicilia, ricca di storia e cultura.",
        "Mercati vivaci e street food incredibile.",
        "Un mix di influenze: araba, normanna e italiana."
      ],
      roma: [
        "Roma è la Città Eterna: storia in ogni angolo.",
        "Monumenti iconici e piazze meravigliose.",
        "Qui metti alla prova il tuo italiano come un vero imperatore!"
      ],
      siena: [
        "Siena è una gemma medievale in Toscana.",
        "Famosa per il Palio e le sue contrade.",
        "Perfetta per allenare la tua scrittura con calma e precisione."
      ],
      venezia: [
        "Venezia è una città sull’acqua: gondole e canali.",
        "Calli, ponti e un’atmosfera magica.",
        "Attento ai canali… e completa le tue missioni!"
      ],
      torino: [
        "Torino è elegante e piena di caffè storici.",
        "Città famosa per il cioccolato e l’architettura.",
        "È il momento di dimostrare tutto quello che hai imparato!"
      ],
      default: ["Scopri la città e completa le attività per guadagnare il badge."]
    }),
    []
  );

  const badgeSrc = CITY_BADGES[cityKey];
  const infoLines = CITY_INFO[cityKey] || CITY_INFO.default;
  useEffect(() => {
  async function loadCity() {
    try {
      const data = await getCity(cityName);
      setCity(data);
    } catch (err) {
      navigate("/story");
    }
  }

  loadCity();
}, [cityName, navigate]);

  const openPassport = () => setPassportOpen(true);
  const closePassport = () => setPassportOpen(false);

  const handleMascotComplete = () => {
    setShowMascot(false);
    setTimeout(() => {
      openPassport();
    }, 300);
  };

  const cityTitle = city?.name || (cityKey ? cityKey.charAt(0).toUpperCase() + cityKey.slice(1) : "");


  const isSectionCompleted = (tasksDone, tasksTotal, pizzasDone, pizzasTotal) => {
    return (
      tasksTotal > 0 &&
      pizzasTotal > 0 &&
      tasksDone >= tasksTotal &&
      pizzasDone >= pizzasTotal
    );
  };

  const readingCompleted = isSectionCompleted(
    city.reading_tasks_done,
    city.reading_task_count,
    city.reading_pizzas_earned,
    city.reading_pizza_goal
  );

  const vocabularyCompleted = isSectionCompleted(
    city.vocabulary_tasks_done,
    city.vocabulary_task_count,
    city.vocabulary_pizzas_earned,
    city.vocabulary_pizza_goal
  );

  const writingCompleted = isSectionCompleted(
    city.writing_tasks_done,
    city.writing_task_count,
    city.writing_pizzas_earned,
    city.writing_pizza_goal
  );

  return (
    <div
      className="min-h-screen flex flex-col items-center text-black relative bg-cover bg-center"
      style={{ backgroundImage: `url(${selectedBg})` }}
    >
      <div className="absolute inset-0 bg-black/35 backdrop-blur-[1px] z-0" />

      <PassportOverlay
        open={passportOpen}
        onClose={closePassport}
        cityTitle={cityTitle}
        badgeSrc={badgeSrc}
        infoLines={infoLines}
      />

      <div className="relative z-10 w-full flex flex-col items-center">
        {showMascot && (
          <MascotOverlay
            dialogues={currentDialogue}
            onComplete={handleMascotComplete}
            currentImage={currentCostumeId}
          />
        )}

        <button
          type="button"
          onClick={openPassport}
          className="fixed left-5 top-[92px] z-40 bg-white/90 hover:bg-white text-black rounded-2xl shadow-lg border border-black/10 px-3 py-2 flex items-center gap-2"
          title="Apri il passaporto"
        >
          <FaRegAddressBook className="text-xl" />
          <span className="text-sm font-semibold">Passaporto</span>
        </button>

        <HelpModal costumeId={currentCostumeId} />

        <Header onBack={() => navigate("/story")} />

      <div className="pb-14">
        {/* City title and info */}
        <div className="flex flex-col items-center mb-6">
          <h1 className="text-3xl sm:text-5xl font-extrabold drop-shadow-md text-center capitalize">
            📍 {city.name}
          </h1>
          <p className="text-lg sm:text-xl mt-2 font-semibold text-gray-700">
            Livello {city.level}
          </p>
          <p className="text-base sm:text-lg mt-4 max-w-2xl text-center px-4">
            Benvenuto a {city.name}! Scegli la tua sfida.
          </p>
        </div>

        {/* Reading / Vocabulary / Writing buttons */}
        <div className="w-full flex justify-center">
          <div
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center px-4 sm:px-10 lg:px-32">
            
            <div>
              <button
                disabled={readingCompleted}
                onClick={() =>
                  navigate("/reading", { state: { fromCity: cityName } })
                }
                className={`bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md
                  flex flex-col items-center justify-between p-3 transition-transform
                  ${
                    readingCompleted
                      ? "opacity-50 cursor-not-allowed"
                      : "hover:scale-105"
                  }`
                }>
                <img src={readingImg} alt="Reading" className="object-contain h-80" />
                Lettura
              </button>

              <ProgressBar label={"Tasks: "} earned={city.reading_tasks_done} required={city.reading_task_count} />

              <ProgressBar label={"Pizzas: "} earned={city.reading_pizzas_earned} required={city.reading_pizza_goal} />
            </div>
            
            <div>
              <button
                disabled={vocabularyCompleted}
                onClick={() =>
                  navigate("/vocabulary", { state: { fromCity: cityName } })
                }
                className={`bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md
                  flex flex-col items-center justify-between p-3 transition-transform
                  ${
                    vocabularyCompleted
                      ? "opacity-50 cursor-not-allowed"
                      : "hover:scale-105"
                  }`
                }
              >
                <img src={vocImg} alt="Vocabulary" className="object-contain h-80" />
                Vocabolario
              </button>

              <ProgressBar label={"Tasks: "} earned={city.vocabulary_tasks_done} required={city.vocabulary_task_count} />

              <ProgressBar label={"Pizzas: "} earned={city.vocabulary_pizzas_earned} required={city.vocabulary_pizza_goal} />
            </div>
            
            <div>
              <button
                disabled={writingCompleted}
                onClick={() =>
                  navigate("/textproduction", { state: { fromCity: cityName } })
                }
                className={`bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md
                  flex flex-col items-center justify-between p-3 transition-transform
                  ${
                    writingCompleted
                      ? "opacity-50 cursor-not-allowed"
                      : "hover:scale-105"
                  }`
                }
              >
                <img src={writingImg} alt="Writing" className="object-contain h-80" />
                Produzione scritta
              </button>

              <ProgressBar label={"Tasks: "} earned={city.writing_tasks_done} required={city.writing_task_count} />

              <ProgressBar label={"Pizzas: "} earned={city.writing_pizzas_earned} required={city.writing_pizza_goal} />
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}

export default CityMenuPage;