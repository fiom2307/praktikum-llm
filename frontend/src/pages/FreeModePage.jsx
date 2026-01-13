import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import vocImg from "../assets/vocabulary.png";
import readingImg from "../assets/reading.png";
import writingImg from "../assets/writing.png";

import HelpModal from "../components/HelpModal";
import { useUser } from "../context/UserContext";

function FreeModePage() {
  const navigate = useNavigate();

  const { currentCostumeId } = useUser();

  return (
    <div className="min-h-screen flex flex-col items-center text-black">
      <Header />

      <div className="absolute right-5 top-2 z-20">
        <HelpModal costumeId={currentCostumeId} />
      </div>

      <div className="flex flex-col items-center mb-6">
        <h1 className="text-5xl font-extrabold drop-shadow-md text-center">
          Modalità libera
        </h1>
        <p className="text-lg mt-4 max-w-2xl text-center px-4">
          Scegli liberamente se esercitarti con la lettura, il vocabolario o la
          produzione scritta.
        </p>
      </div>

      <div className="px-4 md:px-32 w-full">
        <div className="flex flex-col md:flex-row gap-6 md:gap-8 justify-center">
          <button
            onClick={() =>
              navigate("/reading", { state: { fromMode: "free" } })
            }
            className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-4 transition-transform hover:scale-105"
          >
            <img src={readingImg} alt="Lettura" className="object-contain" />
            Lettura
          </button>

          <button
            onClick={() =>
              navigate("/vocabulary", { state: { fromMode: "free" } })
            }
            className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-4 transition-transform hover:scale-105"
          >
            <img src={vocImg} alt="Vocabolario" className="object-contain" />
            Vocabolario
          </button>

          <button
            onClick={() =>
              navigate("/textproduction", { state: { fromMode: "free" } })
            }
            className="bg-[#faf3e0] text-2xl font-semibold rounded-3xl shadow-md flex flex-col items-center justify-between p-4 transition-transform hover:scale-105"
          >
            <img src={writingImg} alt="Produzione scritta" className="object-contain" />
            Produzione scritta
          </button>
        </div>
      </div>
    </div>
  );
}

export default FreeModePage;