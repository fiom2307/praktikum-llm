import Header from "../components/Header";
import ActionButton from "../components/ActionButton";
import LoadingOverlay from "../components/LoadingOverlay";
import { useUser } from "../context/UserContext";
import { incrementPizzaCount } from "../api/pizzaApi";
import { saveFlashcard, getFlashcards } from "../api/flashcardApi";
import { generateWordAndClues, checkWord, getLastVocabularyEntry } from "../api/vocabularyApi";
import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

function VocabularyPage() {
    const { updatePizzaCount } = useUser();
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
    const handleBack = () => {
        if (fromCity) {
            // to city
            navigate(`/city/${fromCity}`);
        } else {
            // to main page
            navigate("/");
        }
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
                setMsg("Congratulations, your answer is correct. You get 1 pizza");
                setCompleted(true);
                const res = await incrementPizzaCount(1);
                updatePizzaCount(res.pizzaCount);
                setCanGenerate(true);
            } else {
                setMsg("Your answer is incorrect. Try again");
            }

            if (newAttempts >= 3 && res.status !== "correct") {
                setMsg(`This was your last attempt. The correct answer was: ${word}`);
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
        <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}
            
            {/* Header */}
            <Header onBack={handleBack} />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                📒 Vocabolario
            </h1>

            
            {/* Main */}
            <div className="px-60 flex flex-col items-center">
                <ActionButton 
                    className="mb-2" 
                    onClick={handleGenerateWordAndClues}
                    disabled={!canGenerate}
                >Genera</ActionButton>
                <div className="flex gap-10 mb-4">
                    <p className="font-bold">INDIZI: </p>
                    {clues.map((clue, index) => (
                        <p key={index} className="">
                            {clue}
                        </p>
                    ))}
                </div>
                <div className="flex">
                    <input
                        type="text"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        placeholder="Inserisci la tua risposta"
                        className="border-2 border-gray-400 rounded-xl px-4 py-3 mr-2 text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                    <ActionButton onClick={handleCheckWord}>Controlla la risposta</ActionButton>
                </div>
                
                <div className="text-center mt-4">
                    <p>Tentativi: {attempts}</p>
                    <p>{msg}</p>
                </div>

                {completed && !flashcardSaved && (
                    <ActionButton
                        onClick={handleSaveFlashcard}
                    >
                        Aggiungi alle flashcard
                    </ActionButton>
                )}
            </div>
        </div>
    );
}

export default VocabularyPage;