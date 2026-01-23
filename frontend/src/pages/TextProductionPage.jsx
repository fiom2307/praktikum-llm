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
import { getCity } from "../api/cityApi";
import ProgressBar from "../components/ProgressBar";

function TextProductionPage() {
    const username = localStorage.getItem("username");
    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");

    const [loading, setLoading] = useState(false);
    const [completed, setCompleted] = useState(false);

    const [showTutorial, setShowTutorial] = useState(false);
    const [topic, setTopic] = useState("");
    const { 
        updatePizzaCount, 
        currentCostumeId, 
        tutorialProgress, 
        completeTutorialContext,
    } = useUser();
    const [exerciseId, setExerciseId] = useState(null); 

    const navigate = useNavigate();
    
    const location = useLocation();
    const fromCity = location.state?.fromCity?.toLowerCase();
    const fromMode = location.state?.fromMode;

    const [city, setCity] = useState("");
    const [writTasksDone, setWritTasksDone] = useState(0);
    const [writPizzas, setWritPizzas] = useState(0);
    const [generated, setGenerated] = useState(false);

    useEffect(() => {
        async function loadCity() {
            if (!fromCity || fromCity === "undefined") return;

            try {
                const data = await getCity(fromCity);
                setCity(data);

                setWritTasksDone(data.writing_tasks_done);
                setWritPizzas(data.writing_pizzas_earned);
            } catch (err) {
                
            }
        }

        loadCity();
    }, [fromCity]);

    useEffect(() => {
        console.log("Checking Tutorial Logic:", fromCity, tutorialProgress);
        if (fromCity === "napoli" && tutorialProgress?.writing === false) {
            setShowTutorial(true);
        }
    }, [fromCity, tutorialProgress, setShowTutorial]);

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
    }, [fromCity, tutorialProgress, setShowTutorial]);


    const loadTopic = async () => {
        if (!username) {
            alert("Per favore, accedi per inviare le risposte.");
            return;
        }

        setCompleted(false);
        setUserText("");       // 
        setCorrectedText("");  // 
        setLoading(true);

        try {
            let data;
            if (fromMode !== "free") {
                data = await createWritingText(fromCity);
            } else {
                data = await createWritingText("");
            }

            setTopic(data.text);
            setExerciseId(data.exerciseId);
            setGenerated(true);
        } catch (error) {
            console.error("Errore durante il caricamento del writing text:", error);
            setTopic("Qualcosa è andato storto, per favore riprova.");
        } finally {
            setLoading(false);
        }
    };

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
        if(!generated) return;

        if (completed) {
            setCorrectedText("Hai già completato questo esercizio! Generane uno nuovo.");
            return;
        }

        setLoading(true);

        try {
            let result = null;
            if (fromMode === "free") {
                result = await correctText(userText, 0, topic);
            }else {
                result = await correctText(userText, exerciseId, "");
            }

            let finalText = result.corrected_text;
            
            if(fromCity && city ) {
                const reachedMaxTasks =
                    writTasksDone + 1 >= city.writing_task_count;

                const reachedMaxPizzas =
                    writPizzas + result.pizzas >= city.writing_pizza_goal;

                if (reachedMaxTasks && reachedMaxPizzas) {
                    finalText +=
                        "\nHai completato tutti gli esercizi di scrittura di questa città! Torna alla pagina precedente per sbloccare il prossimo passo.";
                }
                setWritPizzas(prev =>
                    Math.min(prev + result.pizzas, city.writing_pizza_goal)
                );
                setWritTasksDone(prev =>
                    Math.min(prev + 1, city.writing_task_count)
                );
            }
            
            setCorrectedText(finalText);
            
            const res = await incrementPizzaCount(
                result.pizzas, 
                "writing", 
                fromCity || null 
            );      
            
            if (res && res.pizzaCount !== undefined) {
                updatePizzaCount(res.pizzaCount);
            }
            setCompleted(true);
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

            <div className="absolute right-5 top-2 z-20">
                <HelpModal costumeId={currentCostumeId} />
            </div>

            {/* Header */}
            <Header onBack={handleBack} />
            <div className="w-full pt-2 pb-14">
                <h1 className="text-3xl sm:text-4xl font-extrabold drop-shadow-md text-center">
                    📖 Produzione scritta
                </h1>
                {fromCity && city && (
                    <div className="sm:px-32 lg:px-40 xl:px-96">
                        <ProgressBar label={"Attività: "} earned={writTasksDone} required={city.writing_task_count} />

                        <ProgressBar label={"Pizze: "} earned={writPizzas} required={city.writing_pizza_goal}/>
                    </div>
                )}
            </div>

            {/* Exercise block */}
            <div className="flex items-center justify-center flex-col font-semibold mb-10 text-center">
                <h3 className="text-lg sm:text-xl font-bold">Esercizio:</h3>
                <p className="max-w-xl">
                    {topic}
                </p>
                <ActionButton onClick={loadTopic} className="bg-[#f8edd5] hover:bg-[#e7d9ba] mt-2">Genera</ActionButton>
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
