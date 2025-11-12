import { useNavigate } from "react-router-dom";
import italyMap from "../assets/italy.png";
import ActionButton from "../components/ActionButton";


function MainPage() {
  const pizzaCount = localStorage.getItem("pizzaCount");
  const username = localStorage.getItem("username");
  const navigate = useNavigate();  

  const handleLogout = () => {

    localStorage.removeItem('authToken');

    navigate("/login")
  }

  return (
    <div className="min-h-screen flex flex-col items-center bg-blue-200  text-black"
      style={{
        backgroundImage: `url(${italyMap})`,
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center 20px",
        backgroundSize: "42% auto",
      }}>
      
      {/* Header */}
      <header className="w-full flex justify-between items-start p-6">

        <ActionButton onClick={() => navigate("/flashcards")}>Flashcards</ActionButton>

        <div className="text-right flex flex-col items-end gap-1">
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold">{username}</h2>
          </div>
          <p className="text-sm">
            🍕 <span className="font-semibold">Pizza count:</span> {pizzaCount}
          </p>


          <ActionButton onClick={handleLogout} className="bg-red-500 hover:bg-red-600">Log out</ActionButton>
          
          <ActionButton onClick={() => navigate("/shop")}>Shop</ActionButton>

        </div>
      </header>

      {/* Main */}
      <main className="relative w-full min-h-screen flex items-center justify-center">
      {/* Title */}
      <div className="absolute top-[5%] left-[65%]">
        <h1 className="text-4xl font-extrabold drop-shadow-md text-center">
          Linguini Learning Masters
        </h1>
      </div>

      {/* Reading */}
      <div className="absolute top-[1%] left-[30%]">
        <button
          onClick={() => navigate("/reading")}
          className="bg-green-700 hover:bg-green-800 text-xl font-semibold px-12 py-6 rounded-2xl shadow-lg transition-transform hover:scale-110"
        >
          Reading
        </button>
      </div>

      {/* Vocabulary */}
      <div className="absolute top-[18%] left-[45%]">
        <button
          onClick={() => navigate("/vocabulary")}
          className="bg-white hover:bg-gray-300 text-xl font-semibold px-12 py-6 rounded-2xl shadow-lg transition-transform hover:scale-110"
        >
          Vocabulary
        </button>
      </div>

      {/* Text Production */}
      <div className="absolute top-[40%] left-[59.5%]">        
        <button
          onClick={() => navigate("/textproduction")}
          className="bg-red-600 hover:bg-red-800 text-xl font-semibold px-12 py-6 rounded-2xl shadow-lg transition-transform hover:scale-110"
        >
          Text Production
        </button>
      </div>
    </main>

    </div>
  );
}

export default MainPage;
