import Header from "../components/Header";
import ActionButton from "../components/ActionButton";
import LoadingOverlay from "../components/LoadingOverlay";
import { useUser } from "../context/UserContext";
import { incrementPizzaCount } from "../api/pizzaApi";
import { saveFlashcard, getFlashcards } from "../api/flashcardApi";
import { generateWordAndClues, checkWord, getLastVocabularyEntry } from "../api/vocabularyApi";
import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Mascot from "../components/MascotOutfit";

function VocabularyPage() {
    const { updatePizzaCount, activeMultiplier, setActiveMultiplier } = useUser();
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


    const navigate = useNavigate();
    const location = useLocation();
    const fromCity = location.state?.fromCity;
    const fromMode = location.state?.fromMode;
    const { currentCostumeId } = useUser();
    
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
        async function loadProgress() {
            
            const result = await getLastVocabularyEntry();

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
            setAttempts(progress.attempt);
            setCompleted(progress.completed);
            setCanGenerate(false);

            const cards = await getFlashcards();
            const exists = cards.some(card => card.word === progress.word);
            setFlashcardSaved(exists);
            
        }
        loadProgress();
    }, [username]);

    const handleGenerateWordAndClues = async () => {
        if (!canGenerate) {
            setMsg("Completa primero la palabra actual prima di generarne una nuova.");
            return;
        }

        setLoading(true);
        try {
            const data = await generateWordAndClues();

            setClues(data.clues);
            setWord(data.word);

            // Reset attempts on new word
            setAttempts(0);
            setAnswer("");
            setMsg("");
            setCompleted(false);
            setFlashcardSaved(false)

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
            setMsg(`No more attempts. Generate a new word.`);
            return;
        }
        if (completed) {
            setMsg("You already completed this word! Generate a new one.");
            return;
        }
        setLoading(true);
        try {
            setCanGenerate(false);

            const newAttempts = attempts + 1;
            setAttempts(newAttempts);

            const res = await checkWord(word, clues, answer, newAttempts);

            if (res.status === "almost") {
                setMsg("Your answer is almost correct. Here is a hint: " +  res.hint);
            } else if (res.status === "correct") {
                setCompleted(true);
                let reward = 1;
                if (activeMultiplier) {
                    reward = reward * activeMultiplier.value;
                    setActiveMultiplier(null);
                }
                const res = await incrementPizzaCount(reward);                
                updatePizzaCount(res.pizzaCount);
                setMsg(`Congratulations, your answer is correct. You get ${reward} pizza`);
                setCanGenerate(true);
            } else {
                setMsg("Your answer is incorrect. Try again");
            }

            if (newAttempts >= 3 && res.status !== "correct") {
                setMsg(`This was your last attempt. The correct answer was: ${word}`);
                setActiveMultiplier(null);
                setCanGenerate(true);
                await saveFlashcard(word);
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
        setMsg("Word added to flashcards!");
    };

    return (
        <div className="min-h-screen flex flex-col items-center text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}
            {/* Header */}
            <Header onBack={handleBack} />

            {/* Main container */}
            <main className="items-center justify-center flex flex-col w-full max-w-6xl px-4 sm:px-10 lg:px-32 xl:px-60 relative lg:pr-[280px] overflow-visible">
                <h1 className="text-3xl sm:text-4xl font-extrabold my-10 drop-shadow-md text-left">
                    Vocabolario
                </h1>

                {/* Main content */}
                <div className="flex flex-col items-start gap-2">
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
                </div>
            </main>

            <div className="absolute hidden lg:block right-60 top-48 w-[320px] h-[420px]">
                {msg && (
                    <div className="absolute top-10 right-36 bg-white shadow-lg rounded-3xl px-5 py-3 text-lg leading-relaxed w-64 z-10 relative">
                        {msg}
                        <div className="absolute -right-2 top-6 w-0 h-0 border-l-8 border-l-white border-y-8 border-y-transparent"></div>
                    </div>
                )}

                <Mascot costumeId={currentCostumeId} alt="Mascotte" className="w-[300px] absolute left-20 bottom-0 z-0" style={{ transform: "scaleX(-1)" }}></Mascot>
            </div>

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
