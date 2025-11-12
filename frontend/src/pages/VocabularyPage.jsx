import Header from "../components/Header";
import ActionButton from "../components/ActionButton";
import LoadingOverlay from "../components/LoadingOverlay";
import { generateWordAndClues, checkWord } from "../api/backendApi";
import { useState } from "react";

function VocabularyPage() {
    const [loading, setLoading] = useState(false);
    const [clues, setClues] = useState([]);
    const [word, setWord] = useState("");
    const [answer, setAnswer] = useState("");
    const [status, setStatus] = useState("");
    const [hint, setHint] = useState("");

    const handleGenerateWordAndClues = async () => {
        setLoading(true);
        try {
            const data = await generateWordAndClues();            
            setClues(data.clues);
            setWord(data.word);
        } catch (error) {
            console.error("Error executing action:", error);
        } finally {
            setLoading(false);
        }
    }

    const handleCheckWord = async () => {
        setLoading(true);
        try {
            const res = await checkWord(word, clues, answer);
            if (res.status === "almost") {
                setStatus("Your answer is almost correct. Here is a hint: ");
            } else if (res.status === "correct") {
                setStatus("Congratulations, your answer is correct");
            } else {
                setStatus("Your answer is incorrect. Try again");
            }
            
            setHint(res.hint)
        } catch (error) {
            console.error("Error executing action:", error);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
            {loading && <LoadingOverlay message="The AI is thinking..." />}
            
            {/* Header */}
            <Header />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                📒 Vocabulary
            </h1>

            
            {/* Main */}
            <div className="px-80 flex flex-col items-center">
                <ActionButton className="mb-2" onClick={handleGenerateWordAndClues}>Generate</ActionButton>
                <div className="flex gap-10 mb-4">
                    <p className="font-bold">CLUES: </p>
                    {clues.map((clue, index) => (
                        <p key={index} className="">
                            {clue}
                        </p>
                    ))}
                </div>
                <input
                    type="text"
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Enter your answer"
                    className="border-2 border-gray-400 rounded-xl px-4 py-3 mb-2 w-full text-center focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
                <ActionButton onClick={handleCheckWord}>Check Answer</ActionButton>
                <div className="text-center mt-4">
                    <p>{status}</p>
                    <p>{hint}</p>
                </div>
            </div>
        </div>
    );
}

export default VocabularyPage;