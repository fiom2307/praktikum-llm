import Header from "../components/Header";
import { correctAnswers, createReadingText } from "../api/readingApi";
import { useState, useEffect } from "react";
import LoadingOverlay from "../components/LoadingOverlay";
import ActionButton from "../components/ActionButton";
import ReactMarkdown from "react-markdown";
import { useUser } from "../context/UserContext";
import { incrementPizzaCount } from "../api/pizzaApi";
import { useNavigate, useLocation } from "react-router-dom";
import HelpModal from "../components/HelpModal";
import MascotOverlay from "../components/MascotOverlay";
import { getCity } from "../api/cityApi";
import ProgressBar from "../components/ProgressBar";


function ReadingPage() {
    const username = localStorage.getItem("username");
    const { updatePizzaCount } = useUser();

    const { 
        currentCostumeId, 
        tutorialProgress, 
        completeTutorialContext 
    } = useUser();

    const [correctedText, setCorrectedText] = useState("");
    const [generatedText, setGeneratedText] = useState("");
    const [exerciseId, setExerciseId] = useState(0)
    const [completed, setCompleted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [showTutorial, setShowTutorial] = useState(false);

    const navigate = useNavigate();
    //
    const location = useLocation();
    const fromCity = location.state?.fromCity?.toLowerCase();
    const fromMode = location.state?.fromMode;

    const [city, setCity] = useState("");
    const [readTasksDone, setReadTasksDone] = useState(0);
    const [readPizzas, setReadPizzas] = useState(0);

    const initialText = `1. 
2. 
3. 
4. 
5. `;

    const hasRealContent = (text) => {
        const withoutPlaceholders = text.replace(/^\s*\d+\.\s*$/gm, "");

        return /[a-zA-ZàèéìòùÀÈÉÌÒÙ]/.test(withoutPlaceholders);
    };

    const [userText, setUserText] = useState(initialText);


    useEffect(() => {
        async function loadCity() {
            try {
                const data = await getCity(fromCity);
                setCity(data);

                setReadTasksDone(data.reading_tasks_done);
                setReadPizzas(data.reading_pizzas_earned);
            } catch (err) {
                
            }
        }

        loadCity();
    }, [fromCity]);

    // only shown in napoli and when napoli is first opened
    useEffect(() => {
        console.log("Checking Tutorial Logic:", fromCity, tutorialProgress);
        if (fromCity === "napoli" && tutorialProgress?.reading === false) {
            setShowTutorial(true);
        }
    }, [fromCity, tutorialProgress]);

    // 
    const readingTutorialDialogue = [
       "Benvenuto alla tua prima prova di Lettura!",
        "Clicca sul pulsante 'Genera' per visualizzare il testo. Troverai 5 domande a cui rispondere nel riquadro 'Il tuo testo'.",
        "Leggi con attenzione! Se rispondi correttamente a tutte le 5 domande, vincerai 5 Pizze!"
    ];

    //
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


    async function runAction(action, onSuccess, onError) {
        if (completed) {
            setCorrectedText("Hai già completato questo esercizio! Generane uno nuovo.");
            return;
        }
        setLoading(true);
        try {
            const result = await action();
            onSuccess(result);
        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
            onError("Qualcosa è andato storto, per favore riprova.");
        } finally {
            setLoading(false);
        }
    }

    const handleCorrect = async () => {
        if (!hasRealContent(userText)) {
            return;
        }
        if(!generatedText.trim()) {
            setCorrectedText("Genera prima un esercizio, poi rispondi.");
            return;
        }

        if (!userText.trim()) {
            setCorrectedText("Per favore, inserisci almeno una risposta prima di consegnare.");
            return;
        }
        
        if (completed) {
            setCorrectedText("Hai già completato questo esercizio! Generane uno nuovo.");
            return;
        }

        runAction(
            async () => {
                const result = await correctAnswers(userText, generatedText, exerciseId);
                
                setCorrectedText(result.corrected_answers);
                const res = await incrementPizzaCount(result.pizzas, "reading", fromCity);                
                updatePizzaCount(res.pizzaCount);
                setCompleted(true);

                if (fromCity) {
                    setReadPizzas(prev =>
                        Math.min(prev + result.pizzas, city.reading_pizza_goal)
                    );
                    setReadTasksDone(prev =>
                        Math.min(prev + 1, city.reading_task_count)
                    );
                }
                return result;
            },
            (result) => setCorrectedText(result.corrected_answers),
            (msg) => setCorrectedText(msg)
        );
    };

    const handleReadingText = async () => {
        if (!username) return alert("Per favore, accedi per inviare le risposte.");
        setCompleted(false);
        runAction(
            () => {
                    if (fromMode !== "free") {
                        return createReadingText(fromCity);
                    }
                    return createReadingText();
                },
            (result) => {
                if (result?.status === "done") {
                    handleBack();
                    return;
                }
                setExerciseId(result.exercise_id)
                setGeneratedText(result.reading_text)
                setUserText(`1. 
2. 
3. 
4. 
5. `)
                setCorrectedText("")
            },
            (msg) => setGeneratedText(msg)
        );
    };


    return (
        <div className="min-h-screen flex flex-col items-center text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}

            {/* 1. first time in napoli */}
            {showTutorial && (
                <MascotOverlay 
                    dialogues={readingTutorialDialogue}
                    onComplete={() => {
                        console.log("Tutorial completed for reading");
                        setShowTutorial(false);
                        completeTutorialContext("reading"); // mark as read
                    }}
                    currentImage={currentCostumeId}
                />
            )}

            {/* 2. Q&A helping button */}
            <div className="absolute right-5 top-2 z-20">
                <HelpModal costumeId={currentCostumeId} />
            </div>

            {/* Header */}
            <Header onBack={handleBack} />

            <div className="w-full pt-2 pb-14">
                <h1 className="text-3xl sm:text-4xl font-extrabold drop-shadow-md text-center">
                📚 Lettura
                </h1>
                <p className="mt-2 font-bold text-sm text-center">
                    Bitte keine persönliche Daten eingeben
                </p>
                {fromCity && city && (
                    <div className="sm:px-32 lg:px-40 xl:px-96">
                        <ProgressBar label={"Attività: "} earned={readTasksDone} required={city.reading_task_count} />

                        <ProgressBar label={"Pizze: "} earned={readPizzas} required={city.reading_pizza_goal}/>
                    </div>
                )}
            </div>
            

            {/* Main */}
            <div className="flex items-center justify-center flex-col mb-8 w-full">
                <h3 className="font-semibold mb-2">Esercizio</h3>

                <div className="
                    prose bg-white rounded-xl shadow-sm p-5 
                    w-full max-w-2xl 
                    h-60 sm:h-52 
                    overflow-y-auto leading-relaxed mb-3
                ">
                    <ReactMarkdown>{generatedText}</ReactMarkdown>
                </div>

                <ActionButton 
                    onClick={handleReadingText} 
                    className="bg-[#f8edd5] hover:bg-[#e7d9ba]"
                >
                    Genera
                </ActionButton>
            </div>

            <div className="
                flex flex-col lg:flex-row 
                gap-10 lg:gap-20 
                w-full max-w-5xl 
                items-center lg:items-start
            ">
                {/* User text */}
                <div className="flex items-center justify-center flex-col w-full max-w-md">
                    <h3 className="font-semibold">Il tuo testo</h3>

                    <textarea
                        value={userText}
                        onChange={(e) => setUserText(e.target.value)}
                        onPaste={(e) => e.preventDefault()}
                        className="
                            mt-1 mb-3 resize-none rounded-xl shadow-sm p-3 
                            w-full h-56 
                            focus:outline-none focus:ring-2 focus:ring-blue-400
                            font-mono
                        "
                    />

                    <ActionButton
                        onClick={handleCorrect}
                        disabled={!hasRealContent(userText)}
                        className="bg-[#f8edd5] hover:bg-[#e7d9ba]"
                    >
                        Correggi
                    </ActionButton>
                </div>


                {/* AI correction */}
                <div className="flex flex-col items-center w-full max-w-md">
                    <h3 className="font-semibold">Corretto dall’IA</h3>

                    <div className="
                        prose bg-white rounded-xl shadow-sm p-3 mt-1
                        w-full h-56 overflow-y-auto leading-relaxed
                    ">
                        <ReactMarkdown>{correctedText}</ReactMarkdown>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ReadingPage;
