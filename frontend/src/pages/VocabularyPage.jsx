import Header from "../components/Header";
import ActionButton from "../components/ActionButton";
import LoadingOverlay from "../components/LoadingOverlay";
import { useUser } from "../context/UserContext";
import { incrementPizzaCount } from "../api/pizzaApi";
import { saveFlashcard, getFlashcards } from "../api/flashcardApi";
import { generateWordAndClues, checkWord, getLastVocabularyEntry, getLastVocabularyEntryFromCity, addTaskCount } from "../api/vocabularyApi";
import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Mascot from "../components/MascotOutfit";
import HelpModal from "../components/HelpModal";
import MascotOverlay from "../components/MascotOverlay";
import { getCity } from "../api/cityApi";
import ProgressBar from "../components/ProgressBar";

function VocabularyPage() {
    const { 
        updatePizzaCount, 
        currentCostumeId, 
        tutorialProgress, 
        completeTutorialContext 
    } = useUser();

    const username = localStorage.getItem("username");

    const [loading, setLoading] = useState(false);
    const [clues, setClues] = useState([]);
    const [word, setWord] = useState("");
    const [attempts, setAttempts] = useState(0);
    const [answer, setAnswer] = useState("");
    const [msg, setMsg] = useState("");
    const [completed, setCompleted] = useState(false);
    const [flashcardSaved, setFlashcardSaved] = useState(false);
    const [canGenerate, setCanGenerate] = useState(true);
    const [exerciseId, setExerciseId] = useState(0);
    const [showTutorial, setShowTutorial] = useState(false);


    const navigate = useNavigate();
    const location = useLocation();
    const fromCity = location.state?.fromCity?.toLowerCase();
    const fromMode = location.state?.fromMode;
    
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

    useEffect(() => {
        console.log("Checking Tutorial Logic:", fromCity, tutorialProgress);
        if (fromCity === "napoli" && tutorialProgress?.vocabulary === false) {
            setShowTutorial(true);
        }
    }, [fromCity, tutorialProgress]);

    const vocTutorialDialogue = [
        "Benvenuto alla sfida del Vocabolario!",
        "Leggi con attenzione i tre indizi e prova a indovinare la parola nascosta. Hai 3 tentativi per ogni sfida.",
        "Clicca su 'Genera' per iniziare. Per ogni parola indovinata correttamente, riceverai 1 Pizza!",
        "Buona fortuna e arricchisci il tuo lessico!"
    ];

    const [city, setCity] = useState("");
    const [vocabTasksDone, setVocabTasksDone] = useState(0);
    const [vocabPizzas, setVocabPizzas] = useState(0);

    useEffect(() => {
        async function loadCity() {
            try {
                const data = await getCity(fromCity);
                setCity(data);

                setVocabTasksDone(data.vocabulary_tasks_done);
                setVocabPizzas(data.vocabulary_pizzas_earned);
            } catch (err) {
                
            }
        }

        loadCity();
    }, [fromCity]);


    useEffect(() => {
        async function loadProgress() {
            
            const result = fromCity
                ? await getLastVocabularyEntryFromCity(fromCity)
                : await getLastVocabularyEntry();

            if(!result || !result.exists) {
                setWord("");
                setClues([]);
                setAttempts(0);
                setCompleted(false);
                setFlashcardSaved(false);
                setCanGenerate(true);
                return;
            }

            const progress = result.history;

            if(progress.completed) {
                setWord("");
                setClues([]);
                setAttempts(0);
                setCompleted(false);
                setFlashcardSaved(false);
                setCanGenerate(true);
                return;
            }
            
            setWord(progress.word);
            setClues(progress.clues);
            fromCity ? setExerciseId(progress.exercise_id) : setExerciseId(0)
            setAttempts(progress.attempt_number);
            setCompleted(progress.completed);
            setCanGenerate(false);

            const cards = await getFlashcards();
            const exists = cards.some(card => card.word === progress.word);
            setFlashcardSaved(exists);
            
        }
        loadProgress();
    }, [username, fromCity]);

    const handleGenerateWordAndClues = async () => {
        if (!canGenerate) {
            setMsg("Completa primero la palabra actual prima di generarne una nuova.");
            return;
        }

        setLoading(true);
        try {
            const data = await generateWordAndClues(fromCity);

            // Reset attempts on new word
            setAttempts(0);
            setAnswer("");
            setFlashcardSaved(false);

            if (data?.status === "done") {
                setMsg("Hai completato tutti gli esercizi di questa città! Torna alla pagina precedente per sbloccare il prossimo passo.");
                setCanGenerate(false);
                return;
            }

            setClues(data.clues);
            setWord(data.word);
            setExerciseId(data.exercise_id);
            // Reset for new word
            setMsg("");
            setCompleted(false);
            setCanGenerate(true);
        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
        } finally {
            setLoading(false);
        }
    }

    const handleCheckWord = async () => {
        if (!word) {
            setMsg("Genera una parola prima di controllare la risposta.");
            return;
        }
        
        if (attempts >= 3) {
            setMsg(`Nessun altro tentativo. Genera una nuova parola.`);
            return;
        }
        if (completed) {
            setMsg("Hai già completato questa parola! Generane una nuova.");
            return;
        }
        setLoading(true);
        try {
            setCanGenerate(false);

            const newAttempts = attempts + 1;
            setAttempts(newAttempts);

            const res = await checkWord(word, clues, exerciseId, answer, newAttempts);

            if (res.status === "almost") {
                setMsg("La tua risposta è quasi corretta. Ecco un suggerimento: " +  res.hint);
            } else if (res.status === "correct") {
                setCompleted(true);
                const res = await incrementPizzaCount(1, "vocabulary", fromCity);                
                updatePizzaCount(res.pizzaCount);
                setMsg(`Congratulazioni, la tua risposta è corretta. Hai vinto 1 pizza`);
                setCanGenerate(true);

                if (fromCity) {
                    setVocabPizzas(prev =>
                        Math.min(prev + 1, city.vocabulary_pizza_goal)
                    );
                    setVocabTasksDone(prev =>
                        Math.min(prev + 1, city.vocabulary_task_count)
                    );
                }
                    
            } else {
                setMsg("La tua risposta è errata. Riprova.");
            }

            if (newAttempts >= 3 && res.status !== "correct") {
                setMsg(`Questo era il tuo ultimo tentativo. La risposta corretta era: ${word}`);
                setCanGenerate(true);
                
                await saveFlashcard(word);

                await addTaskCount(fromCity, "vocabulary");

                if(fromCity) {
                    setVocabTasksDone(prev =>
                        Math.min(prev + 1, city.vocabulary_task_count)
                    );
                }

            }

        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
        } finally {
            setLoading(false);
        }
    }

    const handleSaveFlashcard = async () => {
        if (flashcardSaved) return;
        await saveFlashcard(word);
        setFlashcardSaved(true);
        setMsg("Parola aggiunta alle flashcard!");
    };

    return (
        <div className="min-h-screen flex flex-col items-center text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}

            {showTutorial && (
                <MascotOverlay 
                    dialogues={vocTutorialDialogue}
                    onComplete={() => {
                        setShowTutorial(false);
                        completeTutorialContext("vocabulary"); 
                    }}
                    currentImage={currentCostumeId}
                />
            )}

            <div className="absolute right-5 top-2 z-20">
                <HelpModal costumeId={currentCostumeId} />
            </div>

            {/* Header */}
            <Header onBack={handleBack} />

            {/* Main container */}
            <main className="items-center justify-center flex flex-col w-full max-w-6xl px-4 sm:px-10 lg:px-32 xl:px-60">
                <div className="w-full pt-2 pb-14">
                    <h1 className="text-3xl sm:text-4xl font-extrabold drop-shadow-md text-center">
                        Vocabolario
                    </h1>
                    {fromCity && city && (
                        <div className="sm:px-32 lg:px-40 xl:px-32">
                            <ProgressBar label={"Attività: "} earned={vocabTasksDone} required={city.vocabulary_task_count} />

                            <ProgressBar label={"Pizze: "} earned={vocabPizzas} required={city.vocabulary_pizza_goal}/>
                        </div>
                    )}
                </div>
                    
                {/* Main content */}
                <div className=" w-full flex flex-col items-start gap-2">
                    <ActionButton
                        className="bg-[#3399bd] hover:bg-[#2992b7] text-lg mb-6"
                        onClick={handleGenerateWordAndClues}
                        disabled={!canGenerate}
                    >
                        Genera
                    </ActionButton>

                    <div className="mb-4">
                        <p className="text-2xl font-bold">INDIZI: </p>
                        <ul className="text-xl mt-2 leading-relaxed">
                            {(clues.length ? clues : ["indizio non ancora generato", "indizio non ancora generato", "indizio non ancora generato"]).map((clue, index) => (
                                <li key={index}>{index + 1}. {clue}</li>
                            ))}
                        </ul>
                    </div>

                    {/* Input + Button */}
                    <div className="flex flex-col sm:flex-row gap-4 sm:items-center">
                        <input
                            type="text"
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            placeholder="Inserisci la tua risposta"
                            disabled={!word}
                            className="border border-gray-400 rounded-xl px-8 py-3 text-center focus:outline-none focus:ring-2 focus:ring-[#3399bd] w-full sm:w-auto"
                        />

                        <ActionButton
                            onClick={handleCheckWord}
                            className="bg-[#f8edd5] hover:bg-[#e7d9ba] text-lg"
                            disabled={!word}
                        >
                            Controlla la risposta
                        </ActionButton>
                    </div>

                    {/* Attempts */}
                    <div className="flex mt-4 gap-2 text-xl">
                        <p className="font-bold">Tentativi:</p>
                        <p>{attempts}</p>
                    </div>

                    {/* Flashcard button */}
                    {completed && !flashcardSaved && (
                        <ActionButton
                            onClick={handleSaveFlashcard}
                            className="bg-[#f8edd5] hover:bg-[#e7d9ba]"
                        >
                            Aggiungi alle flashcard
                        </ActionButton>
                    )}

                    <div className={`absolute hidden lg:block right-60 ${fromCity ? "top-52" : "top-28"} w-[320px] h-[420px]`}>
                        {msg && (
                            <div className="absolute top-32 right-44 bg-white shadow-lg rounded-3xl px-5 py-3 text-lg leading-relaxed w-64 z-10 relative">
                                {msg}
                                <div className="absolute -right-2 top-6 w-0 h-0 border-l-8 border-l-white border-y-8 border-y-transparent"></div>
                            </div>
                        )}

                        <Mascot costumeId={currentCostumeId} alt="Mascotte" className="w-[300px] absolute left-2 top-10 z-0" style={{ transform: "scaleX(-1)" }}></Mascot>
                    </div>

                </div>
            </main>

            {/* Mascot for mobile (smaller, centered) */}
            <div className="lg:hidden mt-10 flex flex-col items-center">
                {msg && (
                    <div className="bg-white shadow-lg rounded-3xl px-5 py-3 text-lg leading-relaxed w-64 relative mb-4 text-center">
                        {msg}
                    </div>
                )}

                <Mascot costumeId={currentCostumeId} alt="Mascotte" className="w-48" style={{ transform: "scaleX(-1)" }}></Mascot>
            </div>
        </div>
    );
}

export default VocabularyPage;
