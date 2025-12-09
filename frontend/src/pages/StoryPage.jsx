import { useNavigate } from "react-router-dom";
import { FaLock } from "react-icons/fa";
import italyMap from "../assets/italy.png";
import Header from "../components/Header";

function StoryPage() {
  const navigate = useNavigate();

  // Story configuration: only Torino unlocked for now
  const cities = [
    { key: "torino", label: "Torino", top: "30%", left: "36%", unlocked: true },
    { key: "milano", label: "Milano", top: "23%", left: "42%", unlocked: false },
    { key: "venezia", label: "Venezia", top: "24%", left: "49%", unlocked: false },
    { key: "firenze", label: "Firenze", top: "40%", left: "47%", unlocked: false },
    { key: "cagliari", label: "Cagliari", top: "79%", left: "39.5%", unlocked: false },
    { key: "roma", label: "Roma", top: "56%", left: "50%", unlocked: false },
    { key: "pescara", label: "Pescara", top: "51%", left: "55.5%", unlocked: false },
    { key: "napoli", label: "Napoli", top: "69%", left: "57%", unlocked: false }
  ];

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
            <line x1="36%" y1="26.5%" x2="41%" y2="19%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            <line x1="42%" y1="19%" x2="48%" y2="20%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            <line x1="48%" y1="20%" x2="46.5%" y2="34%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            <line x1="46.5%" y1="35%" x2="39%" y2="75%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            <line x1="39%" y1="75%" x2="50%" y2="50%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            <line x1="50%" y1="50%" x2="55%" y2="47%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
            <line x1="55%" y1="47%" x2="56.5%" y2="65%" stroke="#ffcc00" strokeWidth="4" strokeDasharray="8 8" />
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