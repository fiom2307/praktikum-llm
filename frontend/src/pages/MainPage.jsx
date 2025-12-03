import { useNavigate } from "react-router-dom";
import italyMap from "../assets/italy.png";
import Header from "../components/Header";


function MainPage() {  
  const navigate = useNavigate();

  const MapNode = ({ top, left, number, city }) => (
    <div
      className="absolute group z-10 cursor-pointer"
      style={{ top: top, left: left, transform: 'translate(-50%, -100%)' }}
      onClick={() => navigate(`/city/${city}`, { state: { initialEntry: true } })}
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
    <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black overflow-hidden">
      
      {/* Header */}
      <Header />

      {/* Main Content Area */}
      <main className="flex flex-col items-center justify-center w-full flex-grow relative pb-10">
        
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
