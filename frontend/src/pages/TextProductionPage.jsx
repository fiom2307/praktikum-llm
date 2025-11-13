import { useState } from "react";
import { correctText } from "../api/writingApi";
import LoadingOverlay from "../components/LoadingOverlay";
import Header from "../components/Header";
import ReactMarkdown from "react-markdown";

function TextProductionPage() {
    const [userText, setUserText] = useState("");
    const [correctedText, setCorrectedText] = useState("");
    const [loading, setLoading] = useState(false);

    const handleCorrect = async () => {
        setLoading(true);
        try {
            const corrected = await correctText(userText);
            setCorrectedText(corrected);
        } catch (error) {
            console.error("Error correcting text:", error);
            setCorrectedText("Something went wrong, please try again.");
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="min-h-screen flex flex-col items-center bg-blue-200 text-black">
            {loading && <LoadingOverlay message="The AI is thinking..." />}

            {/* Header */}
            <Header />

            <h1 className="text-4xl font-extrabold mt-0 mb-8 drop-shadow-md text-center">
                📖 Text Production
            </h1>
            {/* Main */}
            <div className="flex gap-20">
                <div>
                    <h3 className="font-semibold">Your Text</h3>
                    <textarea
                        value={userText}
                        onChange={(e) => setUserText(e.target.value)}
                        className="mt-0.5 resize-none rounded-xl shadow-sm p-3 w-96 h-56 focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                    <br />
                    <button onClick={handleCorrect} class="bg-blue-400 hover:bg-blue-500 font-semibold px-3 py-1 rounded-xl shadow-md">Correct</button>
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

export default TextProductionPage;