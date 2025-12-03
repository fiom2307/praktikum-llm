import { useNavigate } from "react-router-dom";
import italyMap from "../assets/italy.png";
import ActionButton from "../components/ActionButton";
import { useUser } from "../context/UserContext";


function MainPage() {
  const { pizzaCount } = useUser();
  const username = localStorage.getItem("username");
  
  const navigate = useNavigate();  

  const handleLogout = () => {

    localStorage.removeItem('authToken');

    navigate("/login")
  }

  const MapNode = ({ top, left, number, city }) => (
    <div
      className="absolute group z-10 cursor-pointer"
      style={{ top: top, left: left, transform: 'translate(-50%, -100%)' }}
      onClick={() => navigate(`/city/${city}`)}
    >
      {/* rotate-45 + rounded-br-none water drop shaped */}
      <div className="relative w-12 h-12 bg-red-500 border-4 border-white shadow-xl rounded-full rounded-br-none transform rotate-45 transition-all duration-300 group-hover:scale-110 group-hover:-translate-y-2 group-hover:bg-red-600 flex items-center justify-center">
        
        <span className="transform -rotate-45 text-white font-bold text-xl">
          {number}
        </span>

      </div>

      <div className="absolute -bottom-2 left-1/2 w-8 h-2 bg-black/30 blur-sm rounded-full transform -translate-x-1/2" />

      {/* show city label */}
      <div className="absolute -top-10 left-1/2 transform -translate-x-1/2 hidden group-hover:block bg-gray-900 text-white text-sm px-3 py-1 rounded-lg whitespace-nowrap shadow-md pointer-events-none transition-opacity">
        {city.charAt(0).toUpperCase() + city.slice(1)}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-900"></div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col items-center  text-black overflow-hidden">
      
      {/* Header */}
      <header className="w-full flex justify-between items-start p-6 z-20">
        <ActionButton onClick={() => navigate("/flashcards")}>Flashcards</ActionButton>

        <div className="text-right flex flex-col items-end gap-1">
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold">{username}</h2>
          </div>
          <p className="text-sm">
            🍕 <span className="font-semibold">Pizze:</span> {pizzaCount}
          </p>
          <div className="flex gap-2">
            <ActionButton onClick={handleLogout} className="bg-red-500 hover:bg-red-600">Esci</ActionButton>
            <ActionButton onClick={() => navigate("/shop")}>Shop</ActionButton>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex flex-col items-center justify-center w-full flex-grow relative pb-10">
        
        {/* Title */}
        <h1 className="text-4xl font-extrabold drop-shadow-md text-center mb-8 z-20">
          Maestri dell’Apprendimento Linguini
        </h1>

        {/*  Map Container */}
       
        <div className="relative w-full max-w-4xl flex justify-center">
          
          <img 
            src={italyMap} 
            alt="Map of Italy" 
            className="max-h-[70vh] w-auto object-contain drop-shadow-2xl" 
          />

          {/* 📍 Node 1: Torino */}
          <MapNode 
            top="27%"   
            left="32%" 
            number="1" 
            city="torino"
          />

          {/* 📍 Node 2: Venezia  */}
          <MapNode 
            top="24%" 
            left="48%" 
            number="2" 
            city="venezia"
          />

          {/* 📍 Node 3: Roma */}
          <MapNode 
            top="55%" 
            left="51%" 
            number="3" 
            city="roma"
          />
          
        </div>
        
        <p className="mt-4 text-gray-600 italic">Seleziona una città per iniziare (select a city to start)</p>
      </main>

    </div>
  );


}

export default MainPage;
