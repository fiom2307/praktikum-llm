// import { useEffect, useState } from "react";

function App() {
  const username = "CoolFrog74";
  const pizzaCount = 3;

  // const [backendMessage, setBackendMessage] = useState("");

  // useEffect(() => {
  //   fetch("http://127.0.0.1:5000/")
  //     .then((res) => res.json())
  //     .then((data) => setBackendMessage(data.message))
  //     .catch((err) => console.error("error:", err));
  // }, []);

  return (
    <div className="min-h-screen flex flex-col items-center">

      <header className="w-full flex justify-between items-start p-6">

        <button className="bg-blue-400 hover:bg-blue-500 text-white font-semibold px-4 py-2 rounded-lg">
          Flashcards
        </button>

        <div className="text-right">
          <h2 className="text-xl font-bold">{username}</h2>
        
          <p className="">
            🍕 Pizza Count: <span className="">{pizzaCount}</span>
          </p>
          <button className="bg-blue-400 hover:bg-blue-500 text-white font-semibold px-3 py-1 rounded-lg">
            Shop
          </button>
      
        </div>
      </header>

      <main className="w-full flex flex-col items-center mt-10">
        <h1 className="text-4xl font-bold mb-10">Praktikum LLM</h1>

        <div className="flex gap-6">
          <button className="bg-blue-400 hover:bg-blue-500 text-white text-lg font-semibold px-6 py-3 rounded-lg">
            Reading
          </button>
          <button className="bg-blue-400 hover:bg-blue-500 text-white text-lg font-semibold px-6 py-3 rounded-lg">
            Text Production
          </button>
          <button className="bg-blue-400 hover:bg-blue-500 text-white text-lg font-semibold px-6 py-3 rounded-lg">
            Vocabulary
          </button>
        </div>

        {/* <p>
          {backendMessage}
        </p> */}
      </main>
    </div>
  );
}

export default App;