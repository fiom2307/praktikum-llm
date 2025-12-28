import { useNavigate } from "react-router-dom";
import { FaLock } from "react-icons/fa";
import italyMap from "../assets/italy.png";
import Header from "../components/Header";
import { useEffect, useState } from "react";
import { getCityProgress } from "../api/cityApi";

const CITY_LAYOUT = [  
  { key: "napoli", label: "Napoli", top: "69%", left: "57%" },
  { key: "palermo", label: "Palermo", top: "89%", left: "53%" },
  { key: "roma", label: "Roma", top: "56%", left: "50%" },
  { key: "siena", label: "Siena", top: "44%", left: "46%" },
  { key: "venezia", label: "Venezia", top: "24%", left: "49%" },
  { key: "torino", label: "Torino", top: "28%", left: "36%" }
];

function StoryPage() {
  const navigate = useNavigate();
  const [cities, setCities] = useState([]);

  useEffect(() => {
    getCityProgress()
      .then((backendCities) => {
        const merged = CITY_LAYOUT.map((layoutCity) => {
          const backendCity = backendCities.find(
            (c) => c.key === layoutCity.key
          );

          return {
            ...layoutCity,
            unlocked: backendCity?.unlocked ?? false
          };
        });

        setCities(merged);
      })
      .catch((err) => {
        console.error("Error loading city progress", err);
      });
  }, []);


  const MapNode = ({ top, left, label, cityKey, unlocked }) => {
    const handleClick = () => {
      if (!unlocked) return;
      navigate(`/city/${cityKey}`, { state: { initialEntry: true } });
    };

    return (
      <div
        className={`absolute group z-20 ${
          unlocked ? "cursor-pointer" : "cursor-not-allowed opacity-60"
        }`}
        style={{ top, left, transform: "translate(-50%, -100%)" }}
        onClick={handleClick}
      >
        {/* PIN */}
        <div
          className={
            "relative w-12 h-12 border-4 border-white shadow-xl rounded-full rounded-br-none transform rotate-45 flex items-center justify-center " +
            (unlocked
              ? "bg-red-500 transition-transform duration-300 group-hover:scale-110 group-hover:-translate-y-2 group-hover:bg-red-600"
              : "bg-gray-400")
          }
        >
          {/* LOCK ICON (only for locked cities) */}
          {!unlocked && (
            <FaLock className="absolute text-yellow-300 text-xl transform -rotate-45" />
          )}
        </div>

        {/* Shadow */}
        <div className="absolute -bottom-2 left-1/2 w-8 h-2 bg-black/30 blur-sm rounded-full transform -translate-x-1/2" />

        {/* LABEL ONLY (no lock next to it) */}
        <div className="mt-3 flex items-center justify-center">
          <span className="px-3 py-1 bg-black/80 text-white text-xs rounded-full shadow-sm whitespace-nowrap">
            {label}
          </span>
        </div>
      </div>
    );
  };

  return (
    <div className="h-screen flex flex-col items-center text-black overflow-hidden">
      <Header />

      <main className="flex flex-col items-center justify-center w-full flex-1 relative">

        <div className="relative w-full max-w-[1400px] h-[72vh] flex justify-center items-center">

          {/* ROUTE LINES — now ABOVE the map */}
          <svg className="absolute top-0 left-0 w-full h-full pointer-events-none z-10">
            {/* Napoli -> Palermo */}
            <line x1="57%" y1="65%" x2="52%" y2="86%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            {/* Palermo -> Roma */}
            <line x1="52%" y1="86%" x2="50%" y2="52%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            {/* Roma -> Siena */}
            <line x1="50%" y1="52%" x2="46%" y2="40%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            {/* Siena -> Venezia */}
            <line x1="46%" y1="40%" x2="48%" y2="21%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            {/* Venezia -> Torino */}
            <line x1="48%" y1="21%" x2="36%" y2="24%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
          </svg>

          {/* MAP (now behind nodes & paths) */}
          <img
            src={italyMap}
            alt="Map of Italy"
            className="h-full w-auto object-contain drop-shadow-2xl z-0"
          />

          {/* NODES */}
          {cities.map((city) => (
            <MapNode
              key={city.key}
              cityKey={city.key}
              label={city.label}
              top={city.top}
              left={city.left}
              unlocked={city.unlocked}
            />
          ))}
        </div>

        <p className="mt-2 text-gray-600 italic text-sm">
          Select a city to start your story. Complete the current city to unlock the next one.
        </p>
      </main>
    </div>
  );
}

export default StoryPage;