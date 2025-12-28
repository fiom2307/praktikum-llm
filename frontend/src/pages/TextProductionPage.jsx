import { useState } from "react";
import { correctText } from "../api/writingApi";
import LoadingOverlay from "../components/LoadingOverlay";
import Header from "../components/Header";
import ReactMarkdown from "react-markdown";
import { useNavigate, useLocation } from "react-router-dom";
import ActionButton from "../components/ActionButton";
import { incrementPizzaCount } from "../api/pizzaApi";
import { useUser } from "../context/UserContext";

function TextProductionPage() {
    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [loading, setLoading] = useState(false);
    const [completed, setCompleted] = useState(false);
    const { updatePizzaCount, activeMultiplier, setActiveMultiplier } = useUser();

    const navigate = useNavigate();
    
    const location = useLocation();
    const fromCity = location.state?.fromCity; 
    const fromMode = location.state?.fromMode;

    const topics = [
        "Vacanze",
        "Scuola e tempo libero",
        "Identità e progetti per il futuro",
        "Differenze culturali tra il Nord e il Sud Italia",
        "Amore e amicizia",
        "Feste italiane e cultura giovanile",
        "Lettura e letteratura",
        "Feste e tradizioni italiane"
    ];


    const [topic, setTopic] = useState(() =>
        topics[Math.floor(Math.random() * topics.length)]
    );


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
        if (completed) {
            setCorrectedText("Hai già completato questo esercizio! Generane uno nuovo.");
            return;
        }

        setLoading(true);

        if (completed) {
            setCorrectedText("Hai già completato questo esercizio! Generane uno nuovo.");
            return;
        }

        try {
            const result = await correctText(userText);
            setCorrectedText(result.corrected_text);

            let reward = result.pizzas;
            if (activeMultiplier) {
                if(activeMultiplier.value === 10) {
                    if (reward >= 7){
                        reward *= 10;
                    }
                } else {
                    reward = reward * activeMultiplier.value;
                }
                
                setActiveMultiplier(null);
            }
            const res = await incrementPizzaCount(reward, fromCity);                
            updatePizzaCount(res.pizzaCount);

            setCompleted(true)
        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
            setCorrectedText("Qualcosa è andato storto, per favore riprova.");
        } finally {
            setLoading(false);
        }
    };

    const changeTopic = () => {
        setTopic(prevTopic => {
            let newTopic;
            do {
                newTopic = topics[Math.floor(Math.random() * topics.length)];
            } while (newTopic === prevTopic);
            setCompleted(false);
            return newTopic;
        });
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
                    Scrivi un testo di 50–150 parole sul tema: <span className="font-bold">{topic}</span>.
                </p>
                <ActionButton onClick={changeTopic} className="bg-[#f8edd5] hover:bg-[#e7d9ba] mt-2">Genera</ActionButton>
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
