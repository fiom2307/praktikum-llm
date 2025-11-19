import Header from "../components/Header";
import { correctAnswers, createReadingText } from "../api/readingApi";
import { useState } from "react";
import LoadingOverlay from "../components/LoadingOverlay";
import ActionButton from "../components/ActionButton";
import ReactMarkdown from "react-markdown";
import { useUser } from "../context/UserContext";


function ReadingPage() {
    const { username } = useUser();
    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [generatedText, setGeneratedText] = useState("");
    const [loading, setLoading] = useState(false);

    const handleCorrect = async () => {
        if (!username) return alert("Please log in to submit answers.");
        
        setLoading(true);
        try {
            const corrected = await correctAnswers(username, userText, generatedText);
            setCorrectedText(corrected);
        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
            setCorrectedText("Qualcosa è andato storto, per favore riprova.");
        } finally {
            setLoading(false);
        }
    }

    const handleReadingText = async () => {
        setLoading(true);
        try {
            const readingText = await createReadingText();
            setGeneratedText(readingText);
        } catch (error) {
            console.error("Errore durante l’esecuzione dell’azione:", error);
            setGeneratedText("Qualcosa è andato storto, per favore riprova.");
        } finally {
            setLoading(false);
        }
    }
    
    return (
        <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
            {loading && <LoadingOverlay message="L’IA sta pensando…" />}

            {/* Header */}
            <Header />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                📚 Lettura
            </h1>

            {/* Main */}
            <div>
                <h3 className="font-semibold">Esercizio</h3>
                <div className="prose mt-0.5 bg-white rounded-xl shadow-sm p-5 w-[40rem] h-[12rem] overflow-x-auto leading-relaxed">
                    <ReactMarkdown>{generatedText}</ReactMarkdown>
                </div>
                <br />
                <ActionButton onClick={handleReadingText}>Genera</ActionButton>
            </div>

            <div className="flex gap-20">
                <div>
                    <h3>Il tuo testo</h3>
                    <textarea
                        value={userText}
                        onChange={(e) => setUserText(e.target.value)}
                        className="mt-0.5 resize-none rounded-xl shadow-sm p-3 w-96 h-56 focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                    <br />
                    <ActionButton onClick={handleCorrect}>Correggi</ActionButton>
                </div>
                <div>
                    <h3 className="font-semibold">Corretto dall’IA</h3>
                    <div className="prose mt-0.5 bg-white rounded-xl shadow-sm p-3 w-96 h-56 overflow-y-auto leading-relaxed">
                        <ReactMarkdown>{correctedText}</ReactMarkdown>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ReadingPage;