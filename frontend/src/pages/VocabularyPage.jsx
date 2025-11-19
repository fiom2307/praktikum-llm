import Header from "../components/Header";
import ActionButton from "../components/ActionButton";
import LoadingOverlay from "../components/LoadingOverlay";
import { useUser } from "../context/UserContext";
import { incrementPizzaCount } from "../api/pizzaApi";
import { saveFlashcard, getFlashcards } from "../api/flashcardApi";
import { generateWordAndClues, checkWord, getCurrentVocabulary, saveCurrentVocabulary } from "../api/vocabularyApi";
import { useState, useEffect } from "react";

function VocabularyPage() {
    const { updatePizzaCount , username} = useUser();

    const [loading, setLoading] = useState(false);
    const [clues, setClues] = useState([]);
    const [word, setWord] = useState("");
    const [attempts, setAttempts] = useState(0);
    const [answer, setAnswer] = useState("");
    const [msg, setMsg] = useState("");
    const [completed, setCompleted] = useState(false);
    const [flashcardSaved, setFlashcardSaved] = useState(false);


    useEffect(() => {
        async function loadProgress() {
            
            const progress = await getCurrentVocabulary(username);

            setWord(progress.word);
            setClues(progress.clues);
            setAttempts(progress.attempts);
            setCompleted(progress.completed);

            const cards = await getFlashcards(username);
            const exists = cards.some(card => card.word === progress.word);
            setFlashcardSaved(exists);
            
        }
        loadProgress();
    }, [username]);

    const handleGenerateWordAndClues = async () => {
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

            await saveCurrentVocabulary(username, data.word, data.clues, 0, false);
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
            const res = await checkWord(username, word, clues, answer);
            let isCompleted = completed;

            const newAttempts = attempts + 1;
            setAttempts(newAttempts);


            if (res.status === "almost") {
                setMsg("Your answer is almost correct. Here is a hint: " +  res.hint);
            } else if (res.status === "correct") {
                setMsg("Congratulations, your answer is correct. You get 1 pizza");
                isCompleted = true;
                setCompleted(true);
                const res = await incrementPizzaCount(username, 1);
                updatePizzaCount(res.pizzaCount);
            } else {
                setMsg("Your answer is incorrect. Try again");
            }

            await saveCurrentVocabulary(username, word, clues, newAttempts, isCompleted);

            if (newAttempts >= 3 && res.status !== "correct") {
                setMsg(`This was your last attempt. The correct answer was: ${word}`);
                await saveFlashcard(username, word);
            }

        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
        } finally {
            setLoading(false);
        }
    }

    const handleSaveFlashcard = async () => {
        if (flashcardSaved) return;
        await saveFlashcard(username, word);
        setFlashcardSaved(true);
        setMsg("Word added to flashcards!");
    };

    return (
        <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}
            
            {/* Header */}
            <Header />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                📒 Vocabolario
            </h1>

            
            {/* Main */}
            <div className="px-60 flex flex-col items-center">
                <ActionButton className="mb-2" onClick={handleGenerateWordAndClues}>Genera</ActionButton>
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