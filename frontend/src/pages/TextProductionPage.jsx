import { useEffect, useState } from "react";
import { correctText } from "../api/writingApi";
import LoadingOverlay from "../components/LoadingOverlay";
import Header from "../components/Header";
import ReactMarkdown from "react-markdown";
import { useNavigate, useLocation } from "react-router-dom";
import ActionButton from "../components/ActionButton";
import { incrementPizzaCount } from "../api/pizzaApi";
import { useUser } from "../context/UserContext";
import { createWritingText } from "../api/writingApi";
import HelpModal from "../components/HelpModal";
import MascotOverlay from "../components/MascotOverlay";

function TextProductionPage() {
    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [loading, setLoading] = useState(false);
    const [completed, setCompleted] = useState(false);
    const { 
        updatePizzaCount, 
        currentCostumeId, 
        tutorialProgress, 
        completeTutorialContext 
    } = useUser();
    const [showTutorial, setShowTutorial] = useState(false);
    const [topic, setTopic] = useState("");
    const [exerciseId, setExerciseId] = useState(null); 
    const [refreshKey, setRefreshKey] = useState(0);

    const navigate = useNavigate();
    
    const location = useLocation();
    const fromCity = location.state?.fromCity?.toLowerCase();
    const fromMode = location.state?.fromMode;

    useEffect(() => {
        console.log("Checking Tutorial Logic:", fromCity, tutorialProgress);
        if (fromCity === "napoli" && tutorialProgress?.writing === false) {
            setShowTutorial(true);
        }
    }, [fromCity, tutorialProgress]);

    const writingTutorialDialogue = [
        "Benvenuto alla Produzione Scritta!",
        "Scrivi un testo tra 50 e 150 parole sul tema proposto. Puoi cliccare su 'Genera' per cambiare argomento quando vuoi!",
        "Usa la tua creatività! Io correggerò il tuo lavoro per aiutarti a migliorare.",
        "Se il tuo testo è eccellente, riceverai un premio speciale di 10 Pizze!"
    ];

    useEffect(() => {
        console.log("Checking Tutorial Logic:", fromCity, tutorialProgress);
        if (fromCity === "napoli" && tutorialProgress?.writing === false) {
            setShowTutorial(true);
        }
    }, [fromCity, tutorialProgress]);

    useEffect(() => {
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

        const loadTopic = async () => {
            if (fromCity) {
                try {
                    const data = await createWritingText(fromCity);
                    setTopic(data.text);
                    setExerciseId(data.exerciseId);
                } catch (err) {
                    console.error("Failed to load writing text:", err);
                }
            } else {
                const randomTopic =
                    topics[Math.floor(Math.random() * topics.length)];
                setTopic(randomTopic);
                setExerciseId(null);
            }

            setCompleted(false);
        };

        loadTopic();
    }, [fromCity, refreshKey]);




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

        try {
            const result = await correctText(userText, exerciseId);
            setCorrectedText(result.corrected_text);
            const res = await incrementPizzaCount(result.pizzas, "writing",fromCity);      
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
        setRefreshKey(prev => prev + 1);
    };



    return (
        <div className="min-h-screen flex flex-col items-center text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}

            {showTutorial && (
                <MascotOverlay 
                    dialogues={writingTutorialDialogue}
                    onComplete={() => {
                        setShowTutorial(false);
                        completeTutorialContext("writing"); 
                    }}
                    currentImage={currentCostumeId}
                />
            )}

            <div className="fixed right-5 top-[92px] z-40">
                <HelpModal costumeId={currentCostumeId} />
            </div>

            {/* Header */}
            <Header onBack={handleBack} />

            <h1 className="text-3xl sm:text-4xl font-extrabold mb-6 drop-shadow-md text-center">
                📖 Produzione scritta
            </h1>

            {/* Exercise block */}
            <div className="flex items-center justify-center flex-col font-semibold mb-10 text-center">
                <h3 className="text-lg sm:text-xl font-bold">Esercizio:</h3>
                <p className="max-w-xl">
                    {fromCity ? (
                        <>
                            {topic}
                        </>
                    ) : (
                        <>
                            Scrivi un testo di 50–150 parole sul tema:{" "}
                            <span className="font-bold">{topic}</span>.
                        </>
                    )}
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
