import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import { useUser } from "../context/UserContext";

// Görselleri ekliyoruz
import italyImg from "../assets/italy.png";
import Mascot from "../components/MascotOutfit";

function MainPage() {
  const navigate = useNavigate();
  const { currentCostumeId } = useUser();
  

  return (
    <div className="min-h-screen flex flex-col text-black">
      <Header />

      <main className="flex-1 flex flex-col lg:flex-row items-stretch justify-center gap-8 px-6 lg:px-16 py-10">

        {/* STORY MODE CARD */}
        <div
          onClick={() => navigate("/story")}
          className="flex-1 bg-[#faf3e0] rounded-3xl shadow-lg p-8 flex flex-col items-center cursor-pointer transition-all hover:scale-[1.01] hover:shadow-2xl"
        >
          <h2 className="text-3xl font-extrabold mb-3">Modalità storia</h2>

          <img
            src={italyImg}
            alt="Italy Map"
            className="w-80 h-auto mt-12 mb-12 drop-shadow-lg"
          />

          <p className="text-lg text-gray-700 text-center max-w-md">
            Parti dal nord e viaggia città per città. 
            Completa le attività per sbloccare la prossima città.
          </p>

          <p className="mt-8 text-sm text-gray-500 italic">
            Clicca sulla scheda per iniziare il viaggio.
          </p>
        </div>

        {/* FREE MODE CARD */}
        <div
          onClick={() => navigate("/free")}
          className="flex-1 bg-[#faf3e0] rounded-3xl shadow-lg p-8 flex flex-col items-center cursor-pointer transition-all hover:scale-[1.01] hover:shadow-2xl"
        >
          <h2 className="text-3xl font-extrabold mb-3">Modalità libera</h2>

          <Mascot costumeId={currentCostumeId} alt="Free Mode" className="w-64 h-auto mt-2 mb-6 drop-shadow-lg" ></Mascot>

          <p className="text-lg text-gray-700 text-center max-w-md">
            Usa liberamente lettura, vocabolario e 
            produzione scritta senza seguire l&apos;ordine delle città.
          </p>

          <p className="mt-8 text-sm text-gray-500 italic">
            Clicca sulla scheda per esplorare liberamente.
          </p>
        </div>

      </main>
    </div>
  );
}

export default MainPage;