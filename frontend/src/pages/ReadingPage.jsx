import Header from "../components/Header";
import { correctAnswers, createReadingText } from "../api/readingApi";
import { useState } from "react";
import LoadingOverlay from "../components/LoadingOverlay";
import ActionButton from "../components/ActionButton";
import ReactMarkdown from "react-markdown";


function ReadingPage() {
    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [generatedText, setGeneratedText] = useState("");
    const [loading, setLoading] = useState(false);

    const handleCorrect = async () => {
        setLoading(true);
        try {
            const corrected = await correctAnswers(userText, generatedText);
            setCorrectedText(corrected);
        } catch (error) {
            console.error("Error executing action:", error);
            setCorrectedText("Something went wrong, please try again.");
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
            console.error("Error executing action:", error);
            setGeneratedText("Something went wrong, please try again.");
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
                📚 Reading
            </h1>

            {/* Main */}
            <div>
                <h3 className="font-semibold">Aufgabe</h3>
                <div className="prose mt-0.5 bg-white rounded-xl shadow-sm p-5 w-[40rem] h-[12rem] overflow-x-auto leading-relaxed">
                    <ReactMarkdown>{generatedText}</ReactMarkdown>
                </div>
                <br />
                <ActionButton onClick={handleReadingText}>Generate</ActionButton>
            </div>

            <div className="flex gap-20">
                <div>
                    <h3>Your Text</h3>
                    <textarea
                        value={userText}
                        onChange={(e) => setUserText(e.target.value)}
                        className="mt-0.5 resize-none rounded-xl shadow-sm p-3 w-96 h-56 focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                    <br />
                    <ActionButton onClick={handleCorrect}>Correct</ActionButton>
                </div>
                <div>
                    <h3 className="font-semibold">Corrected by AI</h3>
                    <div className="prose mt-0.5 bg-white rounded-xl shadow-sm p-3 w-96 h-56 overflow-y-auto leading-relaxed">
                        <ReactMarkdown>{correctedText}</ReactMarkdown>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ReadingPage;