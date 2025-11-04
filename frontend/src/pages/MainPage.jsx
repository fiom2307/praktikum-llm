import { useNavigate } from "react-router-dom";

function MainPage() {
  const username = "CoolFrog74";
  const pizzaCount = 3;

  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
      {/* Header */}
      <header className="w-full flex justify-between items-start p-6">
        <button 
          onClick={() => navigate("/flashcards")}
          className="bg-blue-400 hover:bg-blue-500 font-semibold px-4 py-2 rounded-xl shadow-md">
          Flashcards
        </button>

        <div className="text-right flex flex-col items-end gap-1">
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold">{username}</h2>
          </div>
          <p className="text-sm">
            🍕 <span className="font-semibold">Pizza count:</span> {pizzaCount}
          </p>
          <button 
            onClick={() => navigate("/shop")}
            className="bg-blue-400 hover:bg-blue-500 font-semibold px-3 py-1 rounded-xl shadow-md">
            Shop
          </button>
        </div>
      </header>

      {/* Main */}
      <main className="w-full flex flex-col items-center mt-10">
        <h1 className="text-5xl font-extrabold mb-12 drop-shadow-md">
          Praktikum LLM
        </h1>

        <div className="flex gap-16">
          <button 
            onClick={() => navigate("/reading")}
            className="bg-green-700 hover:bg-green-800 text-xl font-semibold px-12 py-6 rounded-2xl shadow-lg transition-transform hover:scale-110">
            Reading
          </button>

          <button 
            onClick={() => navigate("/vocabulary")}
            className="bg-white hover:bg-gray-300 text-xl font-semibold px-12 py-6 rounded-2xl shadow-lg transition-transform hover:scale-110">
            Vocabulary
          </button>

          <button 
            onClick={() => navigate("/textproduction")}
            className="bg-red-600 hover:bg-red-800 text-xl font-semibold px-12 py-6 rounded-2xl shadow-lg transition-transform hover:scale-110">
            Text Production
          </button>
        </div>
      </main>
    </div>
  );
}

export default MainPage;
