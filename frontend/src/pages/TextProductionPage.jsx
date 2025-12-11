import { useState } from "react";
import { correctText } from "../api/writingApi";
import LoadingOverlay from "../components/LoadingOverlay";
import Header from "../components/Header";
import ReactMarkdown from "react-markdown";
import { useNavigate, useLocation } from "react-router-dom";
import ActionButton from "../components/ActionButton";

function TextProductionPage() {
    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();
    
    const location = useLocation();
    const fromCity = location.state?.fromCity; 
    const fromMode = location.state?.fromMode;

    const topics = [
        "Ferien",
        "Schule und Freizeit",
        "Identität und Zukunftspläne",
        "kulturelle Unterschiede zwischen Nord- und Süditalien",
        "Liebe und Freundschaft",
        "italienische Feste und Jugendkultur",
        "Lesen und Literatur",
        "italienische Feiertage und Traditionen"
    ];

    const randomTopic = topics[Math.floor(Math.random() * topics.length)];

    const handleBack = () => {
        if (fromMode === "free") {
            navigate("/free");
            return;
        }
        if (fromCity) {
            navigate(`/city/${fromCity}`);
            return;
        }
        navigate("/");
    };

    const handleCorrect = async () => {
        setLoading(true);
        try {
            const corrected = await correctText(userText);
            setCorrectedText(corrected);
        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
            setCorrectedText("Qualcosa è andato storto, per favore riprova.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}

            {/* Header */}
            <Header onBack={handleBack} />

            <h1 className="text-3xl sm:text-4xl font-extrabold mb-6 drop-shadow-md text-center">
                📖 Produzione scritta
            </h1>

            {/* Exercise block */}
            <div className="flex items-center justify-center flex-col font-semibold mb-10 text-center">
                <h3 className="text-lg sm:text-xl font-bold">Esercizio:</h3>
                <p className="max-w-xl">
                    Scrivi un testo di 50–150 parole sul tema: <span className="font-bold">{randomTopic}</span>.
                </p>
            </div>

            {/* Main content – responsive */}
            <div className="
                flex flex-col lg:flex-row 
                gap-10 lg:gap-20 
                w-full max-w-5xl
                items-center lg:items-start
            ">
                {/* Left side: user input */}
                <div className="flex items-center justify-center flex-col w-full max-w-md">
                    <h3 className="font-semibold">Il tuo testo</h3>
                    <textarea
                        value={userText}
                        onChange={(e) => setUserText(e.target.value)}
                        className="mt-1 resize-none rounded-xl shadow-sm p-3 w-full h-56 focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                    <br />
                    <ActionButton onClick={handleCorrect}className="bg-[#f8edd5] hover:bg-[#e7d9ba]">Correggi</ActionButton>
                </div>

                <div className="flex flex-col items-center w-full max-w-md">
                    <h3 className="font-semibold">Corretto dall’IA</h3>
                    <div className="prose mt-1 bg-white rounded-xl shadow-sm p-3 w-full h-56 overflow-y-auto leading-relaxed">
                        <ReactMarkdown>{correctedText}</ReactMarkdown>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default TextProductionPage;
